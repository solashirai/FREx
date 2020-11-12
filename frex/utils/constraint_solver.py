from __future__ import annotations
from ortools.linear_solver import pywraplp
from frex.models import Candidate, ConstraintSectionSolution, ConstraintSolution
from typing import Tuple
from frex.utils.common import rgetattr
from frex.utils import ConstraintType, Constraint
from enum import Enum


class ConstraintSolver:
    """
    A class to perform constraint solving to produce a final solution of items using constraints on the overall
    set of items.
    """

    def __init__(self):
        self.solver = pywraplp.Solver.CreateSolver("SCIP")
        self._candidates = ()
        self._sections = 1
        self._per_section_count = 1
        self._section_constraints = []
        self._overall_constraints = []

    def set_candidates(self, *, candidates: Tuple[Candidate, ...]):
        """
        Set the candidates that will be used to produce the solution.
        Candidates are expected to be produced as the output of some pipeline, which handles scoring.
        The solver will not handle any sort of scoring for the candidates, but rather it will produce an optimized
        solution based on the Candidates' total_score (which should be computed by a pipeline) and other constraints.

        :param candidates: A tuple of Candidate objects, with corresponding domain_objects and scores
        :return: self, with an updated list of candidates
        """
        self._candidates = candidates
        return self

    def set_sections(self, *, sections: int):
        """
        Set the number of sections in the solution. A section can be thought of as a grouping of items, and the solution
        will give a set of sections each containing some number of items based on all other constraints and the
        optimization target.
        For example, if we are trying to produce a meal plan for 7 days, we can model this by applying the constraint
        solver with 7 sections (days) where each section contains some number of items (i.e. number of meals per day).
        Candidates are also expected to have already been appropriately filtered by the pipeline so that we do not
        consider undesirable candidates during the optimization process.

        :param sections: The number of sections for the final solution to contain
        :return: self, with an updated sections parameter
        """
        self._sections = sections
        return self

    def set_items_per_section(self, *, count: int):
        """
        Set the number of items that should be assigned to each section in the solution. This corresponds to
        the number of Candidates that are chosen in the final solution.
        The implementation currently enforces that each section will contain *exactly* this many items.

        :param count: The number of items that must be assigned to each section.
        :return: self, with the per_section_count updated
        """
        self._per_section_count = count
        return self

    def add_section_constraint(self, *, attribute_name: str, constraint_type: ConstraintType, constraint_value: int):
        """
        Add a constraint to be applied to each section solution. E.g., a constraint on the cost of all items chosen
        within each given section.

        :param attribute_name: The domain_object's attribute to apply the constraint to
        :param constraint_type: The type of constraint - i.e. ==, <=, or >=
        :param constraint_value: The value to constraint the solution to
        :return: self, with a new Constraint added to the section_constraints list
        """
        self._section_constraints.append(
            Constraint(attribute_name=attribute_name,
                       constraint_type=constraint_type,
                       constraint_value=constraint_value)
        )
        return self

    def add_overall_constraint(self, *, attribute_name: str, constraint_type: ConstraintType, constraint_value: int) -> ConstraintSolver:
        """
        Add a constraint to be applied to the entire solution. E.g., a constraint on the cost of all items chosen
        across all sections of the solution.

        :param attribute_name: The domain_object's attribute to apply the constraint to
        :param constraint_type: The type of constraint - i.e. ==, <=, or >=
        :param constraint_value: The value to constraint the solution to
        :return: self, with a new Constraint added to the overall_constraints list
        """
        self._overall_constraints.append(
            Constraint(attribute_name=attribute_name,
                       constraint_type=constraint_type,
                       constraint_value=constraint_value)
        )
        return self

    def solve(self) -> ConstraintSolution:
        """
        Perform integer programming to solve constraints and maximize an objective function based on the total scores
        applied to candidates. This function expects candidates that are the result of some recommendation pipeline
        (i.e., candidates have scores, and problematic candidates have already been filtered out).

        This will produce outputs assigning candidates to 'sections'. A section can be thought of as e.g. a day in
        a meal plan, or a semester in a student's plan-of-study.

        Currently assumes that (1) the objective function is always to maximize the total score of the final output,
        (2) each candidate can only be a part of one section, (3) each section must have an exact number of
        candidates assigned to it, and (4) the order of sections does not matter.

        :return:
        """

        candidate_count = len(self._candidates)

        # keep track of attributes that have constraints applied, to be able to show relevant results in the solution
        attributes_of_interest = set()

        solve_choice = {}
        for i in range(candidate_count):
            for j in range(self._sections):
                solve_choice[i, j] = self.solver.IntVar(0, 1, "")

        # each item is only assigned to one section
        for i in range(candidate_count):
            self.solver.Add(
                self.solver.Sum([solve_choice[i, j] for j in range(self._sections)]) <= 1
            )

        # each section has exactly per_section_count items chosen
        for j in range(self._sections):
            self.solver.Add(
                self.solver.Sum([solve_choice[i, j] for i in range(candidate_count)])
                == self._per_section_count
            )

        # constraints to apply on each section, based on certain field names
        # constraints are added to the solver here (rather than in the add_section_constraints function) because we need
        # to know the number of sections/candidates beforehand to correctly map out these constraints.
        for psc in self._section_constraints:
            attributes_of_interest.add(psc.attribute_name)
            for j in range(self._sections):
                ss = self.solver.Sum(
                    [
                        rgetattr(self._candidates[i].domain_object, psc.attribute_name)
                        * solve_choice[i, j]
                        for i in range(candidate_count)
                    ]
                )
                self.solver.Add(psc.constraint_type(ss, psc.constraint_value))

        # constraints to apply to the overall solution, based on certain field names
        # constraints are added to the solver here for similar reasons as the section_constraints
        for oc in self._overall_constraints:
            attributes_of_interest.add(oc.attribute_name)
            ss = self.solver.Sum(
                [
                    rgetattr(self._candidates[i].domain_object, oc.attribute_name) * solve_choice[i, j]
                    for i in range(candidate_count)
                    for j in range(self._sections)
                ]
            )
            self.solver.Add(oc.constraint_type(ss, oc.constraint_value))

        # maximize score
        objective_terms = []
        for i in range(candidate_count):
            for j in range(self._sections):
                # in the future, maybe incorporate more into this objective function
                # e.g., we would prefer the combination of all items in a section to have some field value in a range,
                # so incorporate that into the score somehow?
                objective_terms.append(self._candidates[i].total_score * solve_choice[i, j])
        self.solver.Maximize(self.solver.Sum(objective_terms))

        status = self.solver.Solve()

        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            sections = []
            overall_attributes = {attr:0 for attr in attributes_of_interest}
            for j in range(self._sections):
                section_candidates = []
                section_attributes = {attr:0 for attr in attributes_of_interest}
                section_score = 0
                for i in range(candidate_count):
                    if solve_choice[i, j].solution_value() > 0.5:
                        # print("Candidate ", i, " assigned to section ", j)
                        section_candidates.append(self._candidates[i])
                        section_score += self._candidates[i].total_score
                        for attr in attributes_of_interest:
                            section_attributes[attr] += rgetattr(self._candidates[i].domain_object, attr)
                sections.append(ConstraintSectionSolution(
                    section_candidates=tuple(section_candidates),
                    section_score=section_score,
                    section_attribute_values=section_attributes
                ))
                for attr in attributes_of_interest:
                    overall_attributes[attr] += section_attributes[attr]

            return ConstraintSolution(
                sections=tuple(sections),
                overall_score=self.solver.Objective().Value(),
                overall_attribute_values=overall_attributes
            )
        else:
            # print('No solution found.')
            return ()  # TODO: what to return if no solution?

