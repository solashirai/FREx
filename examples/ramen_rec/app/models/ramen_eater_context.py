from examples.ramen_rec.app.models.ramen_eater import RamenEater
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class RamenEaterContext:
    ramen_eater_profile: RamenEater
