from FREx.models import Context
from examples.ramen_rec.app.models.ramen import Ramen
from typing import NamedTuple


class RamenContext(NamedTuple, Context):
    target_ramen: Ramen
