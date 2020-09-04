from FREx.models import Context
from examples.ramen_rec.app.models.ramen_eater import RamenEater
from typing import NamedTuple


class RamenEaterContext(NamedTuple, Context):
    ramen_eater_profile: RamenEater
