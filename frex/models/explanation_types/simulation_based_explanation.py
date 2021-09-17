from frex.models import Explanation
from typing import Any
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class SimulationBasedExplanation(Explanation):
    """
    An Explanation that describes the results that would emerge if a given recommendation
    or procedure were followed.
    """

    simulation_inputs: Any
    simulation_result: Any
