from frex.models import Explanation
from typing import Any
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class StatisticalExplanation(Explanation):
    """
    An Explanation based on data about the likelihood of an occurrence or situation.
    """

    based_on_numerical_evidence_value: float
    based_on_numerical_evidence_target: Any
