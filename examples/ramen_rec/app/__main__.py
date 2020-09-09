from pathlib import Path
from frex.models import Explanation, Candidate, Context
from frex.stores import LocalGraph
from frex.pipelines import PipelineExecutor, CandidateScorer, CandidateFilterer, CandidateRanker
from examples.ramen_rec.app.services import SimilarRamenCandidateGenerator, RamenQueryService
from examples.ramen_rec.app.models import RamenContext, FilterSameBrand, ScoreRamenStyle, ScoreRamenRating
from rdflib import URIRef


def run_example():
    SRC_ROOT = Path(__file__).parent.parent
    DATA_DIR = (SRC_ROOT / 'data').resolve()
    data_files = [
        (DATA_DIR / 'ramen-ratings.ttl').resolve(),
        (DATA_DIR / 'ramen-users.ttl').resolve()
    ]

    ramen_graph = LocalGraph(file_paths=data_files)
    ramen_q = RamenQueryService(queryable=ramen_graph)

    ramen_rec_pipe = PipelineExecutor(stages=(
        SimilarRamenCandidateGenerator(ramen_vector_file=(DATA_DIR / 'ramen-vectors.pkl').resolve(),
                                       ramen_query_service=ramen_q),

        CandidateScorer(scoring_function=ScoreRamenRating(),
                        scoring_explanation=Explanation('This ramen has a high rating score.')),

        CandidateScorer(scoring_function=ScoreRamenStyle(),
                        scoring_explanation=Explanation('This ramen is the same style as the target ramen.')),

        CandidateFilterer(filter_function=FilterSameBrand(),
                          filter_explanation=Explanation('This ramen is from a different brand than the target ramen')),

        CandidateRanker()
    ))

    target_ramen_uri = URIRef('http://www.erf.com/examples/ramen/101')
    print(f'get recommendations for ramen with URI {target_ramen_uri}')
    target_ramen = ramen_q.get_ramen_by_uri(ramen_uri=target_ramen_uri)
    recommend_for_context = RamenContext(target_ramen=target_ramen)

    output_candidates = ramen_rec_pipe.execute(context=recommend_for_context)

    best_candidates = output_candidates[:5]

    print(len(output_candidates))
    print("top 5 candidates")
    for c in best_candidates:
        print(c)


if __name__ == '__main__':
    run_example()
