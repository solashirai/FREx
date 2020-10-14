from frex.models import Candidate, Explanation
from examples.ramen_rec.app.models import Ramen, RamenEaterContext, RamenContext
from typing import Union
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class RamenCandidate(Candidate):
    """
    RamenCandidates are created for either a ramen context (for recommending similar ramens) or a ramen eater
    context (for recommending ramens to a particular ramen eater).
    """

    context: Union[RamenContext, RamenEaterContext]
    domain_object: Ramen
