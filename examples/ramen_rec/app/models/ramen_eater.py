from typing import NamedTuple
from FREx.models import DomainObject


class RamenEater(DomainObject, NamedTuple):
    likesRamenFrom: str
    likesRamenStyle: str
