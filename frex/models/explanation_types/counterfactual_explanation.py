from frex.models import Explanation, DomainObject
from typing import Any
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class CounterfactualExplanation(Explanation):
    """
    An Explanation pertaining to how the recommendation output would be different if
    the inputs to the system were changed.
    """

    alternative_input: Any
    alternative_output: DomainObject
