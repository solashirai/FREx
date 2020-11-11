from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject


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
