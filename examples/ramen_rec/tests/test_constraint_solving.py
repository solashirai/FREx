from frex.pipeline_stages.scorers import CandidateRanker
from examples.ramen_rec.app.models import RamenContext, RamenEaterContext
from examples.ramen_rec.app.pipelines import *
from examples.ramen_rec.tests.conftest import placeholder_ramen_candidate
from frex.utils import ConstraintSolverUtils


def test_choose_ramens_using_constraints(
    sim_ramen_pipe,
    test_ramen_101,
):
    output_candidates = tuple(
        sim_ramen_pipe(
            context=RamenContext(target_ramen=test_ramen_101),
        )
    )

    csu = ConstraintSolverUtils()

    final_candidates = csu.solve_constraints_on_candidates(
        candidates=output_candidates,
        num_sections=2,  # 2 sections (e.g., think of this like 2 days)
        per_section_count=3,  # choose 3 ramens per section (e.g., 3 ramens per day)
        per_section_constraints=(
            (
                "rating",
                "leq",
                13,
            ),  # total combined ratings of ramens chosen for a section is <= 13
        ),
        overall_constraints=(
            (
                "rating",
                "leq",
                22,
            ),  # total combined ratings of all ramens chosen is <= 22
        ),
    )

    section_ratings = []
    total_rating = 0
    for section in final_candidates:
        section_rating = 0
        for c in section:
            section_rating += c.domain_object.rating
            total_rating += c.domain_object.rating
        section_ratings.append(section_rating)

    assert (
        all(sr <= 13 for sr in section_ratings)
        and total_rating <= 22
        and len(final_candidates) == 2
        and len(final_candidates[0]) == 3
    )
