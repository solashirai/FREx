from frex.models import Context
from examples.ramen_rec.app.models.ramen import Ramen
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class RamenContext(Context):
    target_ramen: Ramen
