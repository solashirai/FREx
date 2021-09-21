from frex.models import Explanation
from typing import Any
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class ContextualExplanation(Explanation):
    """
    An Explanation based on the context in which a recommendation was produced.
    """

    based_on_context: Any
