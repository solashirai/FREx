from pathlib import Path


class RamenUtils:
    SRC_ROOT = Path(__file__).parent.parent.parent
    DATA_DIR = (SRC_ROOT / 'data').resolve()
