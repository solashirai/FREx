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
            # print(c.name, c.is_a, c.equivalent_to)
            # print("+++++++++++++++++++++++++++++++++++")
            if isinstance(c, owlready2.ThingClass):
                print(f'============{c.name}===========')
                print(f'is_a: {c.is_a}')
                print(f'eq_t: {c.equivalent_to}')
                print(f'ind_eq_t: {c.INDIRECT_equivalent_to}')
                python_rep_string = self.convert_to_py_class(c)
                file_name = self.to_snake_case(c.name)+".py"
                file_to_class[file_name] = str(c.name)

            with open((self.save_dir / file_name).resolve(), 'w') as f:
                f.write(python_rep_string)
            # print(file_name)
            # print(python_rep_string)
            # print("+++++++++++++++++++++++++++++++++++")
            # testnum -= 1
            # if testnum <= 0:
            #     break
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

    def get_property_names_and_types(self, c: owlready2.ThingClass) -> List[Tuple[str, Any, str]]:
        properties = []
        for p in c.is_a+c.equivalent_to:
            if isinstance(p, owlready2.class_construct.Restriction):
                # if a namespace isn't properly specified, the property is just a string instead of having a namespace.
                if isinstance(p.property, str):
                    prop_name = p.property.split("/")[-1]
                    prop_iri = str(p.property)
                else:
                    prop_name = p.property.name
                    prop_iri = str(p.property.iri)
                # TODO: currently only supporting str and int data types
                if p.value == str:
                    prop_type = "str"
                elif p.value == int:
                    prop_type = "int"
                else:
                    prop_type="URIRef"
                # only does not necessarily mean the property exists, so add a default value (None) for the property
                if p.type == owlready2.ONLY or p.cardinality == 0:
                    properties.append((prop_name, prop_type+" = None", prop_iri))
                elif p.type == owlready2.SOME or p.cardinality == 1:
                    # add new properties to the beginning to ensure that properties with default values are at the end
                    # dataclasses require that fields with default values are left to the end.
                    properties.insert(0, (prop_name, prop_type, prop_iri))
                else:
                    print(p, 'NOT FULLY IMPLEMENTED YET',  type(p), 'NOT FULLY IMPLEMENTED YET', p.type)
            elif isinstance(p, owlready2.class_construct.And):
                # print(f'2 {p.property}, {p.value}, {type(p)}, {p.property.iri}')
                # properties.append((p.property.name, "URIRef", str(p.property.iri)))
                print(f'333 {p.is_a}') # --------- {p.property} ============ {p.value}')

                for v in p.is_a:
                     print(f'4444 {type(v)} {v}')
                # TODO: Or
                # TODO: OneOf
                # TODO: finish implementing AND fully

        return properties

    def populate_template(self, *, name: str,
                          subclasses: List[owlready2.ThingClass],
                          properties: List[Tuple[str, Any, str]]) -> str:
        write_string = f"from {str(self.save_dir.name).replace('/', '.')} import *\n"
        write_string += BASIC_CLASS_TEMPLATE
        write_string += f"class {name}(DomainObject"
        for sc in subclasses:
            write_string += f",{str(sc.name)}"
        write_string += "):"

        property_to_uri_dict = {}

        # default to using 4 spaces for indentation
        for (p, t, iri) in properties:
            write_string += f"\n    {p}: {t}"
            property_to_uri_dict[str(p)] = iri
        write_string += "\n\n"
        write_string += "    prop_to_uri = {\n"
        for k,v in property_to_uri_dict.items():
            write_string += f"        URIRef(\"{v}\"): '{k}',\n"
        write_string += "    }\n"
        return write_string

    def convert_to_py_class(self, c: owlready2.ThingClass) -> str:
        # print("====================")
        #
        # print(c.equivalent_to)
        # print(c.is_a)
        # print(c.namespace)
        # print(c.name)
        # print(c.iri)
        #
        # print("====================")
        subclasses = self.get_subclasses(c)
        properties = self.get_property_names_and_types(c)
        write_string = self.populate_template(name=str(c.name), subclasses=subclasses, properties=properties)

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
