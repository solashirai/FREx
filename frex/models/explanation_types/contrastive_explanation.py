from frex.models import Explanation
from typing import Any
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class ContrastiveExplanation(Explanation):
    """
    An Explanation based on making a contrast between factors that influenced the system producing
    one recommendation over another.

    E.g., if an explanation is being produced to answer a question like "Why recommendation A instead
    of recommendation B?", then the contrastive explanation should describe a factor that positively
    influenced choosing recommendation A and a factor that negatively influenced choosing B.
    """

    based_on_fact: Any
    based_on_foil: Any
