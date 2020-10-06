from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class Explanation:
    """
    An Explanation currently simply consists of a string.
    More complex explanation types may be integrated into the framework at a later point, if it makes sense to use
    them in a general way.
    """
    explanation_string: str
