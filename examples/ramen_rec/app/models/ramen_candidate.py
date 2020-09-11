from frex.models import Candidate, Explanation
from examples.ramen_rec.app.models.ramen import Ramen
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class RamenCandidate(Candidate):
    domain_object: Ramen
