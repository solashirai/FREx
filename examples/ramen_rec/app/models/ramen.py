from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject
from examples.ramen_rec.app.utils import RamenUtils
from rdflib.namespace import RDFS


@dataclass_json
@dataclass(frozen=True)
class Ramen(DomainObject):
    """
    Ramen have a label, brand, country, style, and rating.
    Rating is in increments of 0.5, from 0 to 5.
    Labels are fairly arbitrary, but brand, country, and style are limited to several common strings.
    """

    label: str
    brand: str
    country: str
    style: str
    rating: float
    price: float

    # prop_to_uri reflects how automatically generated classes, produced by the ClassGenerator util,
    # would output information necessary to help the DomainKgQueryService convert queried results into
    # python objects. This is not necessary to implement if a query service, like the GraphRamenQueryService,
    # are implemented - this simply serves as an example / enabling unit testing, since testing code generation
    # isn't trivial.
    prop_to_uri = {
        RDFS["label"]: "label",
        RamenUtils.ramen_onto_ns["brand"]: "brand",
        RamenUtils.ramen_onto_ns["country"]: "country",
        RamenUtils.ramen_onto_ns["style"]: "style",
        RamenUtils.ramen_onto_ns["rating"]: "rating",
        RamenUtils.ramen_onto_ns["price"]: "price",
    }
