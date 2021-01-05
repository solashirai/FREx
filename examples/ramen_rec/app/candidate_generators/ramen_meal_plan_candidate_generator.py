from frex.pipeline_stages.candidate_generators import CandidateGenerator
from frex.utils import VectorSimilarityUtils
from typing import Dict, List, Generator, Optional
from rdflib import URIRef
from frex.models import Explanation, Candidate
from examples.ramen_rec.app.models import RamenEaterContext, RamenMealPlanCandidate
from frex.models import DomainObject
from frex.utils import ConstraintSolver
from frex.models.constraints import SectionSetConstraint, ConstraintType


class RamenMealPlanCandidateGenerator(CandidateGenerator):
    """
    Generate a candidate 'meal plan' of ramens to eat.
    """

    def __init__(
        self,
        *,
        num_days: int = 2,
        ramens_per_day: int = 3,
        min_daily_rating: int = 7,
        max_daily_price: int = 7,
        max_total_price: int = 13,
        **kwargs
    ):
        days = []
        for i in range(num_days):
            # generate a bunch of fake 'day' domain objects
            days.append(DomainObject(uri=URIRef(f'placeholder.com/day{str(i+1)}')))
        days = tuple(days)
        day_solver_section = (SectionSetConstraint(scaling=100)
                                    .set_sections(sections=days)
                                    .add_section_count_constraint(exact_count=ramens_per_day)
                                    .add_section_constraint(
            attribute_name="price",
            constraint_type=ConstraintType.LEQ,
            constraint_value=max_daily_price,
        )
                                    .add_section_constraint(
            attribute_name="rating",
            constraint_type=ConstraintType.GEQ,
            constraint_value=min_daily_rating,
        )
        )
        for day_ind, day in enumerate(days):
            for day2_ind, day2 in enumerate(days[day_ind+1:]):
                day_solver_section.add_section_assignment_constraint(
                    section_a_uri=day.uri,
                    section_b_uri=day2.uri,
                    constraint_type=ConstraintType.AM1
                )
        self.solver = (
            ConstraintSolver(scaling=100)
                .add_overall_item_constraint(
                attribute_name="price",
                constraint_type=ConstraintType.LEQ,
                constraint_value=max_total_price,
            )
                .add_overall_count_constraint(
                exact_count=num_days*ramens_per_day)  # this constraint isnt strictly necessary, but improves solving speed by a ton
                .set_section_set_constraints(section_sets=(day_solver_section,))
        )

        CandidateGenerator.__init__(self, **kwargs)

    def __call__(
        self,
        *,
        candidates: Generator[Candidate, None, None] = None,
        context: RamenEaterContext
    ) -> Generator[Candidate, None, None]:
        candidates = tuple(candidates)
        self.solver.set_candidates(candidates=candidates)

        # just yielding a single 'best' solution for now
        soln = self.solver.solve(output_uri=URIRef("placeholder.com/placeholderMealPlanURI"))
        yield RamenMealPlanCandidate(
            domain_object=soln,
            context=context,
            applied_explanations=[self.generator_explanation],
            applied_scores=[0],
        )
