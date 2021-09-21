from frex.models import Explanation, DomainObject
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class CaseBasedExplanation(Explanation):
    """
    An Explanation based on a prior case that is similar to the current case for which an
    explanation is being produced.
    """

    based_on_case: DomainObject
