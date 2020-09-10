from frex.models import Explanation, Context
from frex.stores import LocalGraph
from frex.pipelines import PipelineExecutor
from frex.pipeline_stages.scorers import CandidateRanker
from examples.ramen_rec.app import *
from rdflib import URIRef
from typing import List
import sys


def run_and_display(*, pipe: PipelineExecutor, context: Context):

    print("Retrieving top 5 recommended ramens using demo pipeline...")
    print("")

    output_candidates = list(pipe.execute(context=context))

    best_candidates = output_candidates[:5]

    print("Top 5 Ramens and the explanations applied:")
    for c in best_candidates:
        print("--")
        print(c.domain_object.to_json())
        print(f"Scores -- Explanations:")
        for expl_ind, expl in enumerate(c.applied_explanations):
            print(f'Score {float(c.applied_scores[expl_ind]):4.3} -- {expl.explanation_string}')


def demo_similar_ramens(*, ramen_uri: URIRef):
    data_files = [
        (RamenUtils.DATA_DIR / "ramen-ratings.ttl").resolve(),
    ]

    ramen_graph = LocalGraph(file_paths=data_files)
    ramen_q = GraphRamenQueryService(queryable=ramen_graph)

    print(f"Demo retrieve 'recommendations' for ramens similar to {ramen_uri}")
    try:
        target_ramen = ramen_q.get_ramen_by_uri(ramen_uri=ramen_uri)
    except DomainObjectNotFoundException:
        print(f"Target ramen with URI {ramen_uri} not found.")
        sys.exit(2)
    print("Target ramen content: ")
    print(target_ramen.to_json())
    print("")

    ramen_rec_pipe = PipelineExecutor(
        stages=(
            SimilarRamenCandidateGenerator(
                ramen_vector_file=(RamenUtils.DATA_DIR / "ramen-vectors.pkl").resolve(),
                ramen_query_service=ramen_q,
            ),
            SameBrandFilter(
                filter_explanation=Explanation(
                    explanation_string="This ramen is from a different brand than the target ramen."
                )
            ),
            RamenRatingScorer(
                scoring_explanation=Explanation(
                    explanation_string="This ramen has a high rating score."
                )
            ),
            RamenStyleScorer(
                scoring_explanation=Explanation(
                    explanation_string="This ramen is the same style as the target ramen."
                )
            ),
            CandidateRanker(),
        )
    )

    recommend_for_context = RamenContext(target_ramen=target_ramen)

    run_and_display(pipe=ramen_rec_pipe, context=recommend_for_context)


def demo_ramen_for_user(*, ramen_eater_uri: URIRef):
    data_files = [
        (RamenUtils.DATA_DIR / "ramen-ratings.ttl").resolve(),
    ]
    user_files = [
        (RamenUtils.DATA_DIR / "ramen-users.ttl").resolve(),
    ]

    ramen_graph = LocalGraph(file_paths=data_files)
    ramen_q = GraphRamenQueryService(queryable=ramen_graph)
    user_graph = LocalGraph(file_paths=user_files)
    ramen_eater_q = GraphRamenEaterQueryService(queryable=user_graph)

    print(f"Demo retrieve 'recommendations' for ramens eater {ramen_eater_uri}")
    try:
        target_ramen_eater = ramen_eater_q.get_ramen_eater_by_uri(ramen_eater_uri=ramen_eater_uri)
    except DomainObjectNotFoundException:
        print(f"Target ramen eater with URI {ramen_eater_uri} not found.")
        sys.exit(2)
    print("Target ramen eater content: ")
    print(target_ramen_eater.to_json())
    print("")

    ramen_rec_pipe = PipelineExecutor(
        stages=(
            MatchEaterLikesRamenCandidateGenerator(
                ramen_vector_file=(RamenUtils.DATA_DIR / "ramen-vectors.pkl").resolve(),
                ramen_query_service=ramen_q,
            ),
            RamenEaterProhibitCountryFilter(
                filter_explanation=Explanation(
                    explanation_string="This ramen is not from a country that is prohibited by the eater."
                )
            ),
            RamenRatingScorer(
                scoring_explanation=Explanation(
                    explanation_string="This ramen has a high rating score."
                )
            ),
            RamenEaterLikesBrandScorer(
                success_scoring_explanation=Explanation(
                    explanation_string="This ramen is from a brand that the user likes."
                ),
                failure_scoring_explanation=Explanation(
                    explanation_string="This ramen is from not a brand that the user likes."
                )
            ),
            RamenEaterLikesStyleScorer(
                success_scoring_explanation=Explanation(
                    explanation_string="This ramen is a style that the user likes."
                ),
                failure_scoring_explanation=Explanation(
                    explanation_string="This ramen is not a style that the user likes."
                )
            ),
            RamenEaterLikesCountryScorer(
                success_scoring_explanation=Explanation(
                    explanation_string="This ramen is from a country that the user likes."
                ),
                failure_scoring_explanation=Explanation(
                    explanation_string="This ramen is from not a country that the user likes."
                )
            ),
            CandidateRanker(),
        )
    )

    recommend_for_context = RamenEaterContext(ramen_eater_profile=target_ramen_eater)

    run_and_display(pipe=ramen_rec_pipe, context=recommend_for_context)


def run_example(argv):

    if len(argv) != 2:
        print(
            "The Ramen Recommendation toy example expects two inputs: the context type {EATER or RAMEN} and a URI suffix."
        )
        print("e.g. examples.ramen_rec RAMEN 101")
        sys.exit(2)
    context_type = argv[0]
    uri_suffix = argv[1]

    if context_type == "RAMEN":
        demo_similar_ramens(ramen_uri=RamenUtils.ramen_ns[uri_suffix])
    elif context_type == "EATER":
        demo_ramen_for_user(ramen_eater_uri=RamenUtils.ex_ns[uri_suffix])
    else:
        print(
            "Invalid context type. The first argument should be EATER (to demo ramen recommendations for a ramen eater) or RAMEN (to demo retrieving recommending similar ramens to an input ramen)."
        )
        sys.exit(2)


if __name__ == "__main__":
    print(
        'Showing results for getting top 5 "recommended" ramens, using a hardcoded target ramen.'
    )
    print("Candidates are generated based on jaccard similarity of ramen contents.")
    print("Ramen from the same brand as the target are filtered out.")
    print(
        "Scoring is based on the ramen rating info and whether or not it is the same style as the target ramen."
    )
    print("---")
    run_example(sys.argv[1:])
