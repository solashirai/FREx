from FREx.models import Candidate, Explanation
from examples.ramen_rec.app.models.ramen import Ramen
from typing import List, NamedTuple


class RamenCandidate(Candidate):
    domain_object: Ramen
