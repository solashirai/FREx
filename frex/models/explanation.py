from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Explanation:
    """
    An Explanation in its most simple form consists of a string.

    More complex explanations can be defined by subclassing this Explanation class.
    """

    explanation_string: str
