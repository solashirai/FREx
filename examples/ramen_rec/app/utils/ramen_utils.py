from pathlib import Path
from rdflib import Namespace


class RamenUtils:
    SRC_ROOT = Path(__file__).parent.parent.parent
    DATA_DIR = (SRC_ROOT / "data").resolve()
    ex_ns = Namespace("http://www.frex.com/examples/")
    ramen_ns = Namespace("http://www.frex.com/examples/ramen/")
    ramen_onto_ns = Namespace("http://www.frex.com/examples/ramenOnto/")
