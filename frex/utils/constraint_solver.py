from __future__ import annotations
from ortools.sat.python import cp_model
from frex.models import Candidate, ConstraintSolutionSection, ConstraintSolution
from typing import Tuple, Optional, Dict, List
from frex.utils.common import rgetattr
from frex.models.constraints import ConstraintType, AttributeConstraint, SectionSetConstraint, ItemConstraint
from enum import Enum
from rdflib import URIRef


class ConstraintSolver:
    """
    A class to perform constraint solving to produce a final solution of items using constraints on the overall
    set of items.
    """

    def __init__(self, *, scaling: int = 1):
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._candidates: Tuple[Candidate, ...] = ()
        self._sections: Tuple[SectionSetConstraint, ...] = ()

        self._scaling = scaling

        self._overall_item_constraints: List[AttributeConstraint] = []
        self._item_selection_constraints: List[ItemConstraint] = []

        self._count_constraints = []

        self._required_item_uris = []

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

    def set_section_set_constraints(self, *, section_sets: Tuple[SectionSetConstraint, ...]):
        """
        Set all the SectionSetConstraints that need to be solved to produce a valid solution.

        :param section_sets: A tuple of SectionSetConstraints that will be applied to the solution
        :return:
        """
        self._sections = section_sets
        return self

    def add_overall_count_constraint(
        self,
        *,
        min_count: int = None,
        max_count: int = None,
        exact_count: int = None,
    ):
        """
        Set constraints on the total number of items chosen for the solution.
        This function will check for an exact count first, and if it exists it will only create a constraint for making
        sure the number of items assigned to the target section is equal to that quantity. Otherwise, both a min
        and max count of items assigned to a section can be specified.

        :param min_count: The minimum number of items to assign to the target section
        :param max_count: The maximum number of items to assign to the target section
        :param exact_count: An exact number of items to assign to the target section
        :return:
        """
        constraints = []
        # check exact count first.
        if exact_count is not None:
            self._count_constraints.append(
                AttributeConstraint(
                    attribute_name='__item_count',
                    constraint_type=ConstraintType.EQ,
                    constraint_value=exact_count
                )
            )
        else:
            if min_count is not None:
                self._count_constraints.append(
                    AttributeConstraint(
                        attribute_name='__item_count',
                        constraint_type=ConstraintType.GEQ,
                        constraint_value=min_count
                    )
                )
            if max_count is not None:
                self._count_constraints.append(
                    AttributeConstraint(
                        attribute_name='__item_count',
                        constraint_type=ConstraintType.LEQ,
                        constraint_value=max_count
                    )
                )

        return self

    def add_overall_item_constraint(
        self,
        *,
        attribute_name: str,
        constraint_type: ConstraintType,
        constraint_value: int
    ) -> ConstraintSolver:
        """
        Add a constraint to be applied to the entire solution. E.g., a constraint on the cost of all items chosen
        across all sections of the solution.

        :param attribute_name: The domain_object's attribute to apply the constraint to
        :param constraint_type: The type of constraint - i.e. ==, <=, or >=
        :param constraint_value: The value to constraint the solution to
        :return: self, with a new Constraint added to the overall_constraints list
        """
        self._overall_item_constraints.append(
            AttributeConstraint(
                attribute_name=attribute_name,
                constraint_type=constraint_type,
                constraint_value=constraint_value,
            )
        )
        return self

    def add_item_selection_constraint(
        self,
        *,
        item_a_uri: URIRef,
        item_b_uri: URIRef,
        constraint_type: ConstraintType
    ):
        """
        Require that candidates chosen in the final solution have some relationship based on the constraint, e.g.,
        EQ to ensure either both item_a and item_b are selected/not selected, or LEQ to ensure that if item_a is
        selected then item_b must also be selected.
        :param item_a_uri: The domain object's URI of the first item
        :param item_b_uri: The domain object's URI of the second item
        :param constraint_type: The type of constraint to apply for how the final items are selected
        :return:
        """
        self._item_selection_constraints.append(
            ItemConstraint(
                item_a_uri=item_a_uri,
                item_b_uri=item_b_uri,
                constraint_type=constraint_type
            )
        )
        return self

    def add_required_item_selection(
            self,
            *,
            target_uri: URIRef
    ):
        """
        Require that the final solution selects a candidate whose domain object has the target URI.

        :param target_uri: the URI of the item that must be included in the final solution
        :return:
        """
        self._required_item_uris.append(target_uri)
        return self

    def solve(
            self,
            *,
            output_uri: URIRef
    ) -> Optional[ConstraintSolution]:
        """
        Perform integer programming to solve constraints and maximize an objective function based on the total scores
        applied to candidates. This function expects candidates that are the result of some recommendation pipeline
        (i.e., candidates have scores, and problematic candidates have already been filtered out).

        This will produce outputs assigning candidates to 'sections'. A section can be thought of as e.g. a day in
        a meal plan, or a semester in a student's plan-of-study.

        Currently assumes that (1) the objective function is always to maximize the total score of the final output,
        (2) each candidate can only be a part of one section, (3) each section must have an exact number of
        candidates assigned to it, and (4) the order of sections does not matter.

        :output_uri: The URI to attach to the output constraint solution
        :return:
        """

        required_item_uris = set(self._required_item_uris)

        candidate_count = len(self._candidates)
        dom_obj_uri_to_ind: Dict[URIRef, int] = dict()

        # keep track of attributes that have constraints applied, to be able to show relevant results in the solution
        attributes_of_interest = set()

        item_choices = []
        for i in range(candidate_count):
            dom_obj_uri_to_ind[self._candidates[i].domain_object.uri] = i
            item_choices.append(self._model.NewIntVar(0, 1, ""))
            if self._candidates[i].domain_object.uri in required_item_uris:
                self._model.Add(item_choices[i] == 1)
        item_choices = tuple(item_choices)

        for section in self._sections:
            section.setup_section_constraints(items=self._candidates, item_selection=item_choices, model=self._model)
            attributes_of_interest = attributes_of_interest.union(section.attributes_of_interest)

        for oc in self._overall_item_constraints:
            attributes_of_interest.add(oc.attribute_name)
            ss = sum(
                [
                    int(round(rgetattr(self._candidates[i].domain_object, oc.attribute_name)*self._scaling))
                    * item_choices[i]
                    for i in range(candidate_count)
                ]
            )
            self._model.Add(oc.constraint_type(ss, int(round(oc.constraint_value*self._scaling))))

        if self._count_constraints:
            item_count = sum([item_choices[i] for i in range(candidate_count)])
            for cc in self._count_constraints:
                self._model.Add(cc.constraint_type(item_count, cc.constraint_value))

        for isc in self._item_selection_constraints:
            self._model.Add(
                isc.constraint_type(
                    item_choices[dom_obj_uri_to_ind[isc.item_a_uri]],
                    item_choices[dom_obj_uri_to_ind[isc.item_b_uri]],
                )
            )

        # maximize score
        objective_terms = []
        for i in range(candidate_count):
            # in the future, maybe incorporate more into this objective function
            # e.g., we would prefer the combination of all items in a section to have some field value in a range,
            # so incorporate that into the score somehow?
            objective_terms.append(
                int(round(self._candidates[i].total_score * self._scaling)) * item_choices[i]
            )
        self._model.Maximize(sum(objective_terms))

        status = self._solver.Solve(self._model)

        if status != cp_model.OPTIMAL and status != cp_model.FEASIBLE:
            # possibly to revisit, if in the future it makes more sense to raise an exception than return None
            return None

        overall_attributes = {attr: 0 for attr in attributes_of_interest}

        selected_candidates = []
        if status != cp_model.OPTIMAL and status != cp_model.FEASIBLE:
            # TODO what to do if no solution?
            print('no optimal or feasible solution found.', status)
            return None
        else:
            # if status == cp_model.OPTIMAL:
                # print('optimal solution found')

            for i in range(len(item_choices)):
                if self._solver.Value(item_choices[i]):
                    candidate = self._candidates[i]
                    selected_candidates.append(candidate)

                    for attr in overall_attributes.keys():
                        overall_attributes[attr] += rgetattr(candidate.domain_object, attr)
        section_assignments = [section.get_solution_assignments(solver=self._solver,
                                                                items=self._candidates,
                                                                )
                               for section in self._sections]

        return ConstraintSolution(
            uri=output_uri,
            solution_section_sets=tuple(section_assignments),
            overall_score=self._solver.ObjectiveValue()/self._scaling,
            overall_attribute_values=overall_attributes,
            items=tuple(selected_candidates)
        )
