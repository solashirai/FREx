from pathlib import Path
from src.stores.graph.local_graph import LocalGraph
from src.services.pipeline_executor_service import PipelineExecutorService
from examples.ramen_rec.app.services.ramen_candidate_generator_service import RamenCandidateGeneratorService


def run_example():
    SRC_ROOT = Path(__file__).parent.parent
    DATA_DIR = (SRC_ROOT / 'data').resolve()
    data_files = [
        (DATA_DIR / 'ramen-ratings.ttl').resolve(),
        (DATA_DIR / 'ramen-users.ttl').resolve()
    ]

    ramen_graph = LocalGraph(file_paths=data_files)

    ramen_rec_pipe = PipelineExecutorService(stages=(
        RamenCandidateGeneratorService(),
    ))

    output_context, output_candidates = ramen_rec_pipe.execute()

if __name__ == '__main__':
    run_example()
