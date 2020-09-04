from pathlib import Path
from src.stores.graph.local_graph import LocalGraph


def run_example():
    SRC_ROOT = Path(__file__).parent.parent
    DATA_DIR = (SRC_ROOT / 'data').resolve()
    data_files = [
        (DATA_DIR / 'ramen-ratings.ttl').resolve(),
        (DATA_DIR / 'ramen-users.ttl').resolve()
    ]

    ramen_graph = LocalGraph(file_paths=data_files)



if __name__ == '__main__':
    run_example()
