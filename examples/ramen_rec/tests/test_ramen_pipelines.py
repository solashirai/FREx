from frex.pipeline_stages.scorers import CandidateRanker
from examples.ramen_rec.app.models import RamenContext, RamenEaterContext
from examples.ramen_rec.app.pipelines import *
from examples.ramen_rec.tests.conftest import placeholder_ramen_candidate


def test_generate_candidates(
    ramen_candidate_generator, test_ramen_101, test_ramen_202, test_ramen_103
):

    candidates = list(ramen_candidate_generator(
        context=RamenContext(target_ramen=test_ramen_101)))
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
    cand_202 = placeholder_ramen_candidate(test_ramen_202, context=score_context)
    cand_103 = placeholder_ramen_candidate(test_ramen_103, context=score_context)

    assert (
        rating_scorer.score(candidate=cand_202)
        == cand_202.domain_object.rating / 5
        and rating_scorer.score(candidate=cand_103)
        == cand_103.domain_object.rating / 5
    )


def test_score_style(test_ramen_101, test_ramen_202, test_ramen_103, style_scorer):
    score_context = RamenContext(target_ramen=test_ramen_101)
    cand_202 = placeholder_ramen_candidate(test_ramen_202, context=score_context)
    cand_103 = placeholder_ramen_candidate(test_ramen_103, context=score_context)

    assert (
        style_scorer.score(candidate=cand_202) == 0
        and style_scorer.score(candidate=cand_103) == 1
    )


def test_filter_same_brand(
    test_ramen_101, test_ramen_202, test_ramen_103, same_brand_filterer
):
    score_context = RamenContext(target_ramen=test_ramen_101)

    cand_202 = placeholder_ramen_candidate(test_ramen_202,context=score_context)
    cand_103 = placeholder_ramen_candidate(test_ramen_103,context=score_context)

    assert not same_brand_filterer.filter(candidate=cand_202
    ) and same_brand_filterer.filter(candidate=cand_103)


def test_full_ramen_pipeline(
    sim_ramen_pipe,
    test_ramen_101,
):
    output_candidates = list(sim_ramen_pipe())

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


def test_filter_prohibited_country(
    test_ramen_101,
    test_ramen_202,
    prohibited_country_filterer,
    test_ramen_eater_01_context,
):

    cand_202 = placeholder_ramen_candidate(test_ramen_202,
        context=test_ramen_eater_01_context)
    cand_101 = placeholder_ramen_candidate(test_ramen_101,
        context=test_ramen_eater_01_context)

    assert prohibited_country_filterer.filter(candidate=cand_202
    ) and not prohibited_country_filterer.filter(candidate=cand_101
    )


def test_score_likes_brand(
    test_ramen_101, test_ramen_1011, likes_brand_scorer, test_ramen_eater_01_context
):
    cand_1011 = placeholder_ramen_candidate(test_ramen_1011,
        context=test_ramen_eater_01_context)
    cand_101 = placeholder_ramen_candidate(test_ramen_101,
        context=test_ramen_eater_01_context)

    assert likes_brand_scorer.score(candidate=cand_101
    ) == (False, 0) and likes_brand_scorer.score(candidate=cand_1011
    ) == (
        True,
        0.9,
    )


def test_score_likes_style(
    test_ramen_101, test_ramen_1011, likes_style_scorer, test_ramen_eater_01_context
):
    cand_1011 = placeholder_ramen_candidate(test_ramen_1011,
        context=test_ramen_eater_01_context)
    cand_101 = placeholder_ramen_candidate(test_ramen_101,
        context=test_ramen_eater_01_context)

    assert likes_style_scorer.score(candidate=cand_101
    ) == (True, 1.1) and likes_style_scorer.score(candidate=cand_1011
    ) == (
        False,
        0,
    )


def test_score_likes_country(
    test_ramen_101, test_ramen_1011, likes_country_scorer, test_ramen_eater_01_context
):
    cand_101 = placeholder_ramen_candidate(test_ramen_101, context=test_ramen_eater_01_context)
    cand_1011 = placeholder_ramen_candidate(test_ramen_1011, context=test_ramen_eater_01_context)

    assert likes_country_scorer.score(candidate=cand_101
    ) == (True, 1) and likes_country_scorer.score(candidate=cand_1011
    ) == (
        False,
        0,
    )
