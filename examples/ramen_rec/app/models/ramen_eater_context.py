from examples.ramen_rec.app.models.ramen_eater import RamenEater
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class RamenEaterContext:
    """
    A context wrapper for recommending ramens for a particular RamenEater.
    Currently only contains a reference to the ramen eater.
    """
    ramen_eater_profile: RamenEater
