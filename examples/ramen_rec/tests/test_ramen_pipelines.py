from frex.pipelines import PipelineExecutor
from frex.pipeline_stages.scorers import CandidateRanker
from examples.ramen_rec.app.models import RamenContext
from examples.ramen_rec.tests.conftest import placeholder_ramen_candidate


def test_generate_candidates(
    ramen_candidate_generator, test_ramen_101, test_ramen_202, test_ramen_103
):

    recommend_for_context = RamenContext(target_ramen=test_ramen_101)

    candidates = list(
        ramen_candidate_generator.get_candidates(context=recommend_for_context)
    )
    candidate_ramens = {candidate.domain_object.to_json() for candidate in candidates}

    # length set to 50 is just set by implementation of similar_ramen_candidate_generator
    assert (
        len(candidates) == 50
        and test_ramen_101.to_json() not in candidate_ramens
        and test_ramen_202.to_json() not in candidate_ramens
        and test_ramen_103.to_json() in candidate_ramens
    )


def test_score_rating(test_ramen_101, test_ramen_202, test_ramen_103, rating_scorer):
    score_context = RamenContext(target_ramen=test_ramen_101)

    cand_202 = placeholder_ramen_candidate(test_ramen_202)
    cand_103 = placeholder_ramen_candidate(test_ramen_103)

    assert (
        rating_scorer.score(context=score_context, candidate=cand_202)
        == cand_202.domain_object.rating / 5
        and rating_scorer.score(context=score_context, candidate=cand_103)
        == cand_103.domain_object.rating / 5
    )


def test_score_style(test_ramen_101, test_ramen_202, test_ramen_103, style_scorer):
    score_context = RamenContext(target_ramen=test_ramen_101)

    cand_202 = placeholder_ramen_candidate(test_ramen_202)
    cand_103 = placeholder_ramen_candidate(test_ramen_103)

    assert (
        style_scorer.score(context=score_context, candidate=cand_202) == 0
        and style_scorer.score(context=score_context, candidate=cand_103) == 1
    )


def test_filter_same_brand(
    test_ramen_101, test_ramen_202, test_ramen_103, same_brand_filterer
):
    score_context = RamenContext(target_ramen=test_ramen_101)

    cand_202 = placeholder_ramen_candidate(test_ramen_202)
    cand_103 = placeholder_ramen_candidate(test_ramen_103)

    assert not same_brand_filterer.filter(
        context=score_context, candidate=cand_202
    ) and same_brand_filterer.filter(context=score_context, candidate=cand_103)


def test_full_pipeline(
    ramen_candidate_generator,
    same_brand_filterer,
    style_scorer,
    rating_scorer,
    test_ramen_101,
):
    ramen_rec_pipe = PipelineExecutor(
        stages=(
            ramen_candidate_generator,
            same_brand_filterer,
            style_scorer,
            rating_scorer,
            CandidateRanker(),
        )
    )
    rec_context = RamenContext(target_ramen=test_ramen_101)
    output_candidates = list(ramen_rec_pipe.execute(context=rec_context))

    best_candidates = output_candidates[:10]

    assert (
        all([candidate.domain_object.style == "Pack" for candidate in best_candidates])
        and all(
            [candidate.domain_object.rating == 5.0 for candidate in best_candidates]
        )
        and all(
            [
                len(candidate.applied_scores)
                == len(candidate.applied_explanations)
                == 4
                for candidate in best_candidates
            ]
        )
    )
