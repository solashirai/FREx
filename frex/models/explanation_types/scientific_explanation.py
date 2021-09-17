from frex.models import Explanation
from typing import Any
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class ScientificExplanation(Explanation):
    """
    An Explanation based on the results of some rigorous scientific methods or evidence in literature.
    """

    based_on_evidence: Any
