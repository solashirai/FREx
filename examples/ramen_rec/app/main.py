from pathlib import Path
from FREx.models import Explanation, Candidate, Context
from FREx.stores import LocalGraph
from FREx.services import PipelineExecutorService, ScoringService, FilterService
from examples.ramen_rec.app.services.similar_ramen_candidate_generator_service import SimilarRamenCandidateGeneratorService
from examples.ramen_rec.app.models.ramen_context import RamenContext
from examples.ramen_rec.app.models.ramen_candidate import RamenCandidate
from examples.ramen_rec.app.services.ramen_query_service import RamenQueryService
from rdflib import URIRef


def score_ramen_rating(context: Context, candidate: Candidate) -> float:
    if not isinstance(candidate, RamenCandidate):
        raise TypeError
    return candidate.domain_object.rating / 5.0


def score_similar_style(context: Context, candidate: Candidate) -> float:
    if not isinstance(context, RamenContext) or not isinstance(candidate, RamenCandidate):
        raise TypeError
    if context.target_ramen.style == candidate.domain_object.style:
        return 1
    else:
        return 0


def filter_same_brand(context: Context, candidate: Candidate) -> bool:
    if not isinstance(context, RamenContext) or not isinstance(candidate, RamenCandidate):
        raise TypeError
    return context.target_ramen.brand == candidate.domain_object.brand


def run_example():
    SRC_ROOT = Path(__file__).parent.parent
    DATA_DIR = (SRC_ROOT / 'data').resolve()
    data_files = [
        (DATA_DIR / 'ramen-ratings.ttl').resolve(),
        (DATA_DIR / 'ramen-users.ttl').resolve()
    ]

    ramen_graph = LocalGraph(file_paths=data_files)
    ramen_q = RamenQueryService(queryable=ramen_graph)

    ramen_rec_pipe = PipelineExecutorService(stages=(
        SimilarRamenCandidateGeneratorService(ramen_vector_file=(DATA_DIR / 'ramen-vectors.pkl').resolve(),
                                              ramen_query_service=ramen_q),

        ScoringService(scoring_function=score_ramen_rating,
                       scoring_explanation=Explanation('This ramen has a high rating score.')),

        ScoringService(scoring_function=score_similar_style,
                       scoring_explanation=Explanation('This ramen is the same style as the target ramen.')),

        FilterService(filter_function=filter_same_brand,
                      filter_explanation=Explanation('This ramen is from a different brand than the target ramen'))
    ))

    target_ramen_uri = URIRef('http://www.erf.com/examples/ramen/101')
    print(f'get recommendations for ramen with URI {target_ramen_uri}')
    target_ramen = ramen_q.get_ramen_by_uri(ramen_uri=target_ramen_uri)
    recommend_for_context = RamenContext(target_ramen=target_ramen)

    output_context, output_candidates = ramen_rec_pipe.execute(context=recommend_for_context)

    best_candidates = output_candidates[:5]

    print(output_context)
    print(len(output_candidates))
    print("top 5 candidates")
    for c in best_candidates:
        print(c)


if __name__ == '__main__':
    run_example()
