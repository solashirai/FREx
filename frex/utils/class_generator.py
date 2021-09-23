import owlready2.class_construct
from owlready2 import *
from pathlib import Path
from typing import List, Tuple, Any
import argparse
import json
from rdflib import URIRef


BASIC_CLASS_TEMPLATE = """from dataclasses import dataclass
from dataclasses_json import dataclass_json
from rdflib import URIRef
from frex.models import DomainObject


@dataclass_json
@dataclass(frozen=True)
"""


class ClassGenerator:
    def __init__(self, *, onto_file: str, save_dir: Path):
        self.onto = get_ontology(f'file://{onto_file}').load()
        self.save_dir = save_dir

    def to_snake_case(self, name: str) -> str:
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        name = re.sub('__([A-Z])', r'_\1', name)
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
        return name.lower()

    def generate(self):
        file_to_class = {}
        for c in self.onto.classes():
            if isinstance(c, owlready2.ThingClass):
                python_rep_string = self.convert_to_py_class(c)
                file_name = self.to_snake_case(c.name)+".py"
                file_to_class[file_name] = str(c.name)

                with open((self.save_dir / file_name).resolve(), 'w') as f:
                    f.write(python_rep_string)
        init_file_contents = ""
        for k,v in file_to_class.items():
            init_file_contents += f"from .{k[:-3]} import {v}\n"
        with open((self.save_dir / "__init__.py").resolve(), 'w') as f:
            f.write(init_file_contents)

    def get_subclasses(self, c: owlready2.ThingClass) -> List[owlready2.ThingClass]:
        subclasses = []
        for subcl in c.is_a:
            if isinstance(subcl, owlready2.ThingClass) and subcl in self.onto.classes():
                subclasses.append(subcl)
        return subclasses

    def add_restriction(self, *, p: owlready2.class_construct.Restriction, properties: List):
        # if a namespace isn't properly specified, the property is just a string instead of having a namespace.
        if isinstance(p.property, str):
            prop_name = p.property.split("/")[-1]
            prop_iri = str(p.property)
        else:
            prop_name = p.property.name
            prop_iri = str(p.property.iri)
        # TODO: currently only supporting str and int data types for specific type hints
        if p.value == str:
            prop_type = "str"
        elif p.value == int:
            prop_type = "int"
        else:
            prop_type = "URIRef"
        properties.insert(0, (prop_name, prop_type, prop_iri))

    def get_inner_restrictions(self, *, p: owlready2.class_construct, properties: List):
        for v in p.Classes:
            if isinstance(v, owlready2.class_construct.Restriction):
                self.add_restriction(p=v, properties=properties)
            else:
                self.get_inner_restrictions(p=v, properties=properties)

    def get_property_names_and_types(self, c: owlready2.ThingClass) -> List[Tuple[str, Any, str]]:
        properties = []
        for p in c.is_a+c.equivalent_to:
            if isinstance(p, owlready2.class_construct.Restriction):
                self.add_restriction(p=p, properties=properties)
            elif isinstance(p, owlready2.class_construct.LogicalClassConstruct):
                # AND and OR -type class constructions
                self.get_inner_restrictions(p=p, properties=properties)

        return properties

    def populate_template(self, *, name: str,
                          supclasses: List[owlready2.ThingClass],
                          properties: List[Tuple[str, Any, str]]) -> str:
        write_string = f"from {str(self.save_dir.name).replace('/', '.')} import *\n"
        write_string += BASIC_CLASS_TEMPLATE
        write_string += f"class {name}(DomainObject"
        for sc in supclasses:
            write_string += f", {str(sc.name)}"
        write_string += "):"

        property_to_uri_dict = {}

        # default to using 4 spaces for indentation

        # using default values (e.g. = None) for properties can cause significant issues when
        # handling inheritance, since if any super class has a default value, all subsequent
        # properties in subclasses must all have default values.
        # the current compromise for this situation is to just make all classes have no default values.
        property_lines = []
        for (p, t, iri) in properties:
            p_str = f"\n    {p}: {t}"
            if p_str not in property_lines:
                property_lines.append(p_str)
            property_to_uri_dict[str(p)] = iri
        for l in property_lines:
            write_string += l

        write_string += "\n\n"
        write_string += "    prop_to_uri = {\n"
        for k,v in property_to_uri_dict.items():
            write_string += f"        URIRef(\"{v}\"): '{k}',\n"
        write_string += "    }\n"
        for sup_cls in supclasses:
            write_string += f"    prop_to_uri.update({str(sup_cls.name)}.prop_to_uri)\n"
        return write_string

    def convert_to_py_class(self, c: owlready2.ThingClass) -> str:
        subclasses = self.get_subclasses(c)
        properties = self.get_property_names_and_types(c)
        write_string = self.populate_template(name=str(c.name), supclasses=subclasses, properties=properties)

        return write_string


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Specify an ontology, either from the web or stored locally, "
                                                 "to use to generate Python classes.")
    parser.add_argument('--onto', type=str, help='The URL or local directory for the target ontology')
    parser.add_argument('--local', dest='onto_local', action='store_true',
                        help='Specify that the onto string refers to a local directory (default true)')
    parser.add_argument('--remote', dest='onto_local', action='store_false',
                        help='Specify that the onto string refers to a URL.')
    parser.set_defaults(onto_local=True)
    parser.add_argument('--save_dir', type=str, help='The directory to save the generated Python classes')
    args = parser.parse_args()

    onto_file = args.onto
    if args.onto_local:
        onto_file = str(Path(onto_file).resolve())
    Path(args.save_dir).mkdir(parents=True, exist_ok=True)
    save_dir = Path(args.save_dir).resolve()
    cg = ClassGenerator(onto_file=onto_file, save_dir=save_dir)
    cg.generate()
