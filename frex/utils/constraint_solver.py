from __future__ import annotations
from ortools.linear_solver import pywraplp
from frex.models import Candidate
from typing import Tuple
from frex.utils.common import rgetattr
from frex.utils import ConstraintType, Constraint
from enum import Enum


class ConstraintSolver:
    """
    Perform integer programming to solve constraints and maximize an objective function based on the total scores
    applied to candidates. This function expects candidates that are the result of some recommendation pipeline
    (i.e., candidates have scores, and problematic candidates have already been filtered out).

    This will produce outputs assigning candidates to 'sections'. A section can be thought of as e.g. a day in
    a meal plan, or a semester in a student's plan-of-study.

    Currently assumes that (1) the objective function is always to maximize the total score of the final output,
    (2) each candidate can only be a part of one section, (3) each section must have an exact number of
    candidates assigned to it, and (4) the order of sections does not matter.

    :param candidates: The candidates to choose for the optimization problem
    :param num_sections: The number of sections to assign candidates to
    :param per_section_count: The number of candidates that must be assigned into each section
    :param per_section_constraints: Constraints to apply for each section. Currently using tuples of (str, str, int)
    of the form (field_to_constrain, type_of_constraint (i.e., 'eq', 'leq', 'geq), value_to_constrain).
    :param overall_constraints: Constraints for the overall solution. Currently using tuples of (str, str, int)
    containing (field_to_constrain, type_of_constraint (i.e., 'eq', 'leq', 'geq), value_to_constrain).
    :return: A tuple of tuples, containing candidates assigned to each section.
    """

    def __init__(self):
        self.solver = pywraplp.Solver.CreateSolver("SCIP")
        self.candidates = ()
        self.sections = 1
        self.per_section_count = 1
        self.section_constraints = []
        self.overall_constraints = []

    def set_candidates(self, *, candidates: Tuple[Candidate]):
        self.candidates = candidates
        return self

    def set_sections(self, *, num_sections: int):
        self.sections = num_sections
        return self

    def set_items_per_section(self, *, count: int):
        self.per_section_count = count
        return self

    def add_section_constraint(self, *, attribute_name: str, constraint_type: ConstraintType, constraint_val: int):
        self.section_constraints.append(
            Constraint(attribute_name=attribute_name,
                       constraint_type=constraint_type,
                       constraint_val=constraint_val)
        )
        return self

    def add_overall_constraint(self, *, attribute_name: str, constraint_type: ConstraintType, constraint_val: int):
        self.overall_constraints.append(
            Constraint(attribute_name=attribute_name,
                       constraint_type=constraint_type,
                       constraint_val=constraint_val)
        )
        return self

    def solve(self) -> Tuple[Tuple[Candidate]]:

        candidate_count = len(self.candidates)
        solve_choice = {}
        for i in range(candidate_count):
            for j in range(self.sections):
                solve_choice[i, j] = self.solver.IntVar(0, 1, "")

        # each item is only assigned to one section
        for i in range(candidate_count):
            self.solver.Add(
                self.solver.Sum([solve_choice[i, j] for j in range(self.sections)]) <= 1
            )

        # each section has exactly per_section_count items chosen
        for j in range(self.sections):
            self.solver.Add(
                self.solver.Sum([solve_choice[i, j] for i in range(candidate_count)])
                == self.per_section_count
            )

        # constraints to apply on each section, based on certain field names
        for psc in self.section_constraints:
            for j in range(self.sections):
                ss = self.solver.Sum(
                    [
                        rgetattr(self.candidates[i].domain_object, psc.attribute_name)
                        * solve_choice[i, j]
                        for i in range(candidate_count)
                    ]
                )
                self.solver.Add(psc.constraint_type(ss, psc.constraint_val))

        # constraints to apply to the overall solution, based on certain field names
        for oc in self.overall_constraints:
            ss = self.solver.Sum(
                [
                    rgetattr(self.candidates[i].domain_object, oc.attribute_name) * solve_choice[i, j]
                    for i in range(candidate_count)
                    for j in range(self.sections)
                ]
            )
            self.solver.Add(oc.constraint_type(ss, oc.constraint_val))

        # maximize score
        objective_terms = []
        for i in range(candidate_count):
            for j in range(self.sections):
                # in the future, maybe incorporate more into this objective function
                # e.g., we would prefer the combination of all items in a section to have some field value in a range,
                # so incorporate that into the score somehow?
                objective_terms.append(self.candidates[i].total_score * solve_choice[i, j])
        self.solver.Maximize(self.solver.Sum(objective_terms))

        status = self.solver.Solve()

        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            print('Total final score = ', self.solver.Objective().Value(), '\n')
            print()
            output_candidates = []
            for j in range(self.sections):
                section_candidates = []
                for i in range(candidate_count):
                    if solve_choice[i, j].solution_value() > 0.5:
                        print("Candidate ", i, " assigned to section ", j)
                        section_candidates.append(self.candidates[i])
                output_candidates.append(tuple(section_candidates))
            return tuple(output_candidates)
        else:
            # print('No solution found.')
            return ()  # TODO: what to return if no solution?

