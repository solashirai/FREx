from frex.models import Candidate, Explanation
from frex.models.constraints import ConstraintSolution
from examples.ramen_rec.app.models import Ramen, RamenEaterContext, RamenContext
from typing import Union
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class RamenMealPlanCandidate(Candidate):
    """
    A fake 'meal plan' of ramens to eat, based on an underlying constraint solution.
    """

    context: Union[RamenContext, RamenEaterContext]
    domain_object: ConstraintSolution
