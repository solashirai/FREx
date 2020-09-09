from typing import NamedTuple
from frex.models import DomainObject


class RamenEater(DomainObject, NamedTuple):
    likesRamenFrom: str
    likesRamenStyle: str
