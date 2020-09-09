from pathlib import Path

SRC_ROOT = Path(__file__).parent
DATA_DIR = (SRC_ROOT / 'data').resolve()
data_files = [
    (DATA_DIR / 'ramen-ratings.ttl').resolve(),
    (DATA_DIR / 'ramen-users.ttl').resolve()
]
