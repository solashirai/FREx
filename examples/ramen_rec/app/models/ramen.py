from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject


@dataclass_json
@dataclass(frozen=True)
class Ramen(DomainObject):
    label: str
    brand: str
    country: str
    style: str
    rating: float
