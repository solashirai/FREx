from examples.ramen_rec.app.models.ramen import Ramen
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class RamenContext:
    """
    A context wrapper for recommending similar ramens.
    Currently just contains a target ramen.
    """

    target_ramen: Ramen
