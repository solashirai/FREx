from ortools.sat.python import cp_model
from ortools.linear_solver import pywraplp
from frex.models import Candidate
from typing import Tuple, Dict
from dataclasses import fields


class ConstraintSolverUtils:
    """
    A utility class for general constraint solving related to recommendations.
    """

    @staticmethod
    def solve_constraints_on_candidates(
        *,
        candidates: Tuple[Candidate],
        num_sections: int,
        per_section_count: int,
        per_section_constraints: Tuple[Tuple[str, str, int]],  # field, eq/leq/geq, val
        overall_constraints: Tuple[Tuple[str, str, int]],  # field, eq/leq/geq, valS
    ) -> Tuple[Tuple[Candidate]]:
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
        solver = pywraplp.Solver.CreateSolver("SCIP")

        candidate_count = len(candidates)
        solve_choice = {}
        for i in range(candidate_count):
            for j in range(num_sections):
                solve_choice[i, j] = solver.IntVar(0, 1, "")

        # each item is only assigned to one section
        for i in range(candidate_count):
            solver.Add(
                solver.Sum([solve_choice[i, j] for j in range(num_sections)]) <= 1
            )

        # each section has exactly per_section_count items chosen
        for j in range(num_sections):
            solver.Add(
                solver.Sum([solve_choice[i, j] for i in range(candidate_count)])
                == per_section_count
            )

        # constraints to apply on each section, based on certain field names
        for psc in per_section_constraints:
            for j in range(num_sections):
                ss = solver.Sum(
                    [
                        getattr(candidates[i].domain_object, psc[0])
                        * solve_choice[i, j]
                        for i in range(candidate_count)
                    ]
                )
                if psc[1] == "eq":
                    solver.Add(ss == psc[2])
                elif psc[1] == "leq":
                    solver.Add(ss <= psc[2])
                else:
                    solver.Add(ss >= psc[2])

        # constraints to apply to the overall solution, based on certain field names
        for oc in overall_constraints:
            ss = solver.Sum(
                [
                    getattr(candidates[i].domain_object, oc[0]) * solve_choice[i, j]
                    for i in range(candidate_count)
                    for j in range(num_sections)
                ]
            )
            if oc[1] == "eq":
                solver.Add(ss == oc[2])
            elif oc[1] == "leq":
                solver.Add(ss <= oc[2])
            else:
                solver.Add(ss >= oc[2])

        # maximize score
        objective_terms = []
        for i in range(candidate_count):
            for j in range(num_sections):
                # in the future, maybe incorporate more into this objective function
                # e.g., we would prefer the combination of all items in a section to have some field value in a range,
                # so incorporate that into the score somehow?
                objective_terms.append(candidates[i].total_score * solve_choice[i, j])
        solver.Maximize(solver.Sum(objective_terms))

        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            # print('Total final score = ', solver.Objective().Value(), '\n')
            # print()
            output_candidates = []
            for j in range(num_sections):
                section_candidates = []
                for i in range(candidate_count):
                    if solve_choice[i, j].solution_value() > 0.5:
                        print("Candidate ", i, " assigned to section ", j)
                        section_candidates.append(candidates[i])
                output_candidates.append(tuple(section_candidates))
            return tuple(output_candidates)
        else:
            # print('No solution found.')
            return ()  # TODO: what to return if no solution?
