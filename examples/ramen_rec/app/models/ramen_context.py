from frex.models import Context
from examples.ramen_rec.app.models.ramen import Ramen
from typing import NamedTuple


class RamenContext(Context, NamedTuple):
    target_ramen: Ramen
