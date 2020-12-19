from typing import Optional, Tuple, List, Dict, Callable
from frex.utils.constraints import ConstraintType, AttributeConstraint, SectionAssignmentConstraint, SectionConstraintHierarchy
from frex.utils.common import rgetattr
from frex.models import DomainObject, Candidate, ConstraintSolutionSectionSet, ConstraintSolutionSection
from rdflib import URIRef
from collections import defaultdict
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import IntVar


class SectionSetConstraint:
    """
    A solution section represents some grouping of the items chosen for the solution, used to
    group together the items to fulfill some goal.
    An example of the use solution sections would be for a course recommender system. One solution section would handle
    how to assign various courses to fulfill graduation requirements. A second solution section would be used to choose
    which courses are assigned to which semester.
    """

    def __init__(self, *, scaling: int = 1):
        self._sections: Tuple[DomainObject, ...] = ()
        self._uri_to_index = {}
        self._targeted_section_constraints: Dict[int, List[AttributeConstraint]] = defaultdict(lambda: [])

        self._section_constraint_hierarchies: List[SectionConstraintHierarchy, ...] = []
        self._section_enforcement_bools = []

        self._assignment_count_constraint: Dict[int, List[AttributeConstraint]] = defaultdict(lambda: [])
        def always_true(*args):
            return True
        self._section_assignment_filter: Dict[int, Callable[..., bool]] = defaultdict(lambda: always_true)
        self._section_assignment_constraints: List[SectionAssignmentConstraint] = []

        # this dict will store variables used to assign items to each section in the optimization solution
        self._item_assignments = {}

        # store attribute names that might be relevant to the solution that is produced
        self._attributes_of_interest = set()

        # used to convert from floats to ints
        self._scaling = scaling

    @property
    def attributes_of_interest(self):
        """
        Getter for the attributes of interest property
        :return:
        """
        return self._attributes_of_interest

    def set_sections(self, *, sections: Tuple[DomainObject, ...]):
        """
        Set the sections that items will be assigned to.
        For example, in a course recommender system, these sections could be a tuple of semesters (assign each class to
        a semester) or a tuple of graduation requirements (assign each class to one or more requirement).

        :param sections: A tuple of domain objects that concrete instances of 'sections' to which items should be assigned
        :return:
        """
        self._sections = sections
        self._section_enforcement_bools = [[] for i in range(len(sections))]
        # keep a dictionary relating the domain object's URI to its index that is used for constraint solving purposes
        for index, section in enumerate(sections):
            self._uri_to_index[section.uri] = index

        return self

    def set_section_assignment_filter(
            self,
            *,
            target_uri: URIRef,
            filter: Callable[..., bool]
    ):
        """
        Add a filter for sections to determine whether or not each item is allowed to be assigned to it.
        If no filter is specified for a given section, we assume all items are allowed to be assigned.

        :param target_uri: The URI of the section to set this filter for
        :param filter: The filter function that takes anything as input and produces a bool indicating whether that item
        is allowed to be assigned to the target section
        :return:
        """
        self._section_assignment_filter[self._uri_to_index[target_uri]] = filter
        return self

    def add_section_constraint(
        self,
        *,
        attribute_name: str,
        constraint_type: ConstraintType,
        constraint_value: int,
        target_uri: Optional[URIRef] = None
    ):
        """
        Add a constraint to be applied to each section solution. E.g., a constraint on the cost of all items chosen
        within each given section.
        If no target uri is specified, we assume all sections have this constraint

        :param attribute_name: The domain_object's attribute to apply the constraint to
        :param constraint_type: The type of constraint - i.e. ==, <=, or >=
        :param constraint_value: The value to constraint the solution to
        :param target_uri: The target URI of the section that this constraint should apply to. If none, all sections
        will have the constraint applied.
        :return: self, with a new Constraint added to the section_constraints list
        """
        if target_uri is None:
            for j in range(len(self._sections)):
                self._targeted_section_constraints[j].append(
                    AttributeConstraint(
                        attribute_name=attribute_name,
                        constraint_type=constraint_type,
                        constraint_value=constraint_value,
                    )
                )
        else:
            self._targeted_section_constraints[self._uri_to_index[target_uri]].append(
                AttributeConstraint(
                    attribute_name=attribute_name,
                    constraint_type=constraint_type,
                    constraint_value=constraint_value,
                )
            )
        return self

    def add_hierarchical_section_constraint(
            self,
            *,
            hierarchy: SectionConstraintHierarchy
    ):
        """
        Add constraints based on a hierarchy of logical AND/OR operators that should be enforced.
        if a hierarchy is set like this, all sections by default will use the hierarchy to determine whether
        or not to enforce its various constraints.

        :param hierarchy: A SectionConstraintHierarchy of sections that will be applied for the solution sections.
        :return:
        """
        self._section_constraint_hierarchies.append(hierarchy)

        return self

    def _add_recursive_enforcement_booleans(
            self,
            *,
            model: cp_model,
            parent_bools,  # WHAT TYPE IS THIS? List[???]
            hierarchy: SectionConstraintHierarchy
    ):
        """
        Recursively add boolean variables to establish relationships among sections.
        This primarily is used to handle setup for logical AND/OR operators between sections, which can be applicable
        to situations like graduation requirements (where some requirements require all of their sub-requirements to be
        fulfilled, or how some can be fulfilled by fulfilling any 1 of its sub-requirements).

        :param model: The cp_model that is being set up
        :param parent_bools: The boolean variables that were applied to the parent section that called this function.
        :param hierarchy: The SectionConstraintHierarchy to be recursively working through to add boolean variables
        :return:
        """
        self._section_enforcement_bools[self._uri_to_index[hierarchy.root_uri]] = parent_bools

        nested_and_bools = []
        for next_level in SectionConstraintHierarchy.dependency_and:
            new_and_bool = model.NewBoolVar("")
            nested_and_bools.append(new_and_bool)

            next_level_bools = [new_and_bool]
            next_level_bools.extend(parent_bools)
            self._add_recursive_enforcement_booleans(model=model, parent_bools=next_level_bools, hierarchy=next_level)
        if nested_and_bools:
            model.Add(sum(nested_and_bools) >= len(nested_and_bools)).OnlyEnforceIf(parent_bools)

        nested_or_bools = []
        for next_level in SectionConstraintHierarchy.dependency_or:
            new_or_bool = model.NewBoolVar("")
            nested_or_bools.append(new_or_bool)

            next_level_bools = [new_or_bool]
            next_level_bools.extend(parent_bools)
            self._add_recursive_enforcement_booleans(model=model, parent_bools=next_level_bools, hierarchy=next_level)
        if nested_and_bools:
            model.Add(sum(nested_or_bools) >= 1).OnlyEnforceIf(parent_bools)

    def add_section_assignment_constraint(
            self,
            *,
            section_a_uri: URIRef,
            section_b_uri: URIRef,
            constraint_type: ConstraintType
    ):
        """
        Add constraints on how items are assigned to different sections.
        The main use of this type of constraint is to apply constraints on whether items can be assigned to multiple
        sections, or forcing items to be applied to multiple sections.
        Some uses include enforcing that item assignments for different graduation requirements are unique (i.e.,
        for requirements that both can be fulfilled by some class but the class can't count for both).

        :param section_a_uri: The URI of a section to apply this constraint
        :param section_b_uri: Another URI of a section to apply this constraint
        :param constraint_type: The type of constraint to be applying on the items assigned to section A and B.
        :return:
        """
        self._section_assignment_constraints.append(
            SectionAssignmentConstraint(
                constraint_type=constraint_type,
                section_a_uri=section_a_uri,
                section_b_uri=section_b_uri
            )
        )
        return self

    def add_section_count_constraint(
        self,
        *,
        min_count: int = None,
        max_count: int = None,
        exact_count: int = None,
        target_uri: Optional[URIRef] = None
    ):
        """
        Set constraints on the number of items assigned to sections.
        If no target URI is specified, it is assumed that the count constraint applies to all sections.
        This function will check for an exact count first, and if it exists it will only create a constraint for making
        sure the number of items assigned to the target section is equal to that quantity. Otherwise, both a min
        and max count of items assigned to a section can be specified.

        :param min_count: The minimum number of items to assign to the target section
        :param max_count: The maximum number of items to assign to the target section
        :param exact_count: An exact number of items to assign to the target section
        :param target_uri: The uri of the section to apply this constraint to, if any
        :return:
        """
        constraints = []
        # check exact count first.
        if exact_count is not None:
            constraints.append(
                AttributeConstraint(
                    attribute_name='__item_count',
                    constraint_type=ConstraintType.EQ,
                    constraint_value=exact_count
                )
            )
        else:
            if min_count is not None:
                constraints.append(
                    AttributeConstraint(
                        attribute_name='__item_count',
                        constraint_type=ConstraintType.GEQ,
                        constraint_value=min_count
                    )
                )
            if max_count is not None:
                constraints.append(
                    AttributeConstraint(
                        attribute_name='__item_count',
                        constraint_type=ConstraintType.LEQ,
                        constraint_value=max_count
                    )
                )

        if target_uri is not None:
            self._assignment_count_constraint[self._uri_to_index[target_uri]].extend(constraints)
        else:
            for index in self._uri_to_index.values():
                self._assignment_count_constraint[index].extend(constraints)
        return self

    def setup_section_constraints(
            self,
            *,
            items: Tuple[Candidate, ...],
            item_selection: Tuple[IntVar, ...],
            model: cp_model
    ):
        """
        Convert the various constraints applied to this solution section into a matrix form to feed into the
        constraint solver.

        :param items: The candidate items being used to assign into the solution
        :param item_selection: Variables manipulated by the solver to determine whether or not each item is chosen
        :param model: The constraint solver model
        :return:
        """
        item_count = len(item_selection)
        section_count = len(self._sections)

        for i in range(item_count):
            this_item_assignment_vars = []
            for j in range(section_count):
                self._item_assignments[i, j] = model.NewIntVar(0, 1, "")
                this_item_assignment_vars.append(self._item_assignments[i, j])
                model.Add(self._item_assignments[i, j] <= item_selection[i])
            # ensure that each item is assigned to at least 1 section, if it is selected
            model.AddMaxEquality(item_selection[i], this_item_assignment_vars)

        # set up boolean operators among sections, which will be used to choose whether or not to enforce
        # various constraints on each solution section
        if self._section_constraint_hierarchies:
            for hierarchy in self._section_constraint_hierarchies:
                self._add_recursive_enforcement_booleans(
                    model=model, parent_bools=[], hierarchy=hierarchy)

        for section_index in range(section_count):
            section_bools = self._section_enforcement_bools[section_index]

            for ac in self._assignment_count_constraint[section_index]:
                section_assignment_sum = sum(
                    [self._item_assignments[i, section_index]
                     * self._section_assignment_filter[section_index](items[i].domain_object)
                     for i in range(item_count)])
                model.Add(ac.constraint_type(section_assignment_sum, ac.constraint_value)).OnlyEnforceIf(section_bools)

            for ac in self._targeted_section_constraints[section_index]:
                self._attributes_of_interest.add(ac.attribute_name)
                ss = sum(
                    [
                        int(round(rgetattr(items[i].domain_object, ac.attribute_name)*self._scaling))
                        * self._section_assignment_filter[section_index](items[i].domain_object)
                        * self._item_assignments[i, section_index]
                        for i in range(item_count)
                    ]
                )
                model.Add(ac.constraint_type(ss, int(round(ac.constraint_value*self._scaling)))).OnlyEnforceIf(section_bools)

        for sac in self._section_assignment_constraints:
            for i in range(item_count):
                model.Add(sac.constraint_type(
                    self._item_assignments[i, self._uri_to_index[sac.section_a_uri]],
                    self._item_assignments[i, self._uri_to_index[sac.section_b_uri]]
                ))

    def get_solution_assignments(
            self,
            *,
            solver: cp_model.CpSolver,
            items: Tuple[Candidate, ...]
    ) -> ConstraintSolutionSectionSet:
        """
        Using a solver that has already solved for the overall constraints, create a constraint solution section set
        that captures all the sections, the items assigned to each section, and the scores/attribute values associated
        with those assignments

        :param solver: A constraint solver, which has already been run to obtain a solution
        :param items: A tuple of candidates that was used by the solver to derive the solution
        :return: A ConstraintSolutionSectionSet object capturing the relevant information for this set of sections
        """
        section_scores = [0 for s in self._sections]
        section_attribute_values = [{attr: 0 for attr in self._attributes_of_interest} for s in self._sections]
        section_items = [[] for s in self._sections]

        for i in range(len(items)):
            for j in range(len(self._sections)):
                if solver.Value(self._item_assignments[i, j]):
                    section_items[j].append(items[i])
                    section_scores[j] += items[i].total_score
                    for attr in self._attributes_of_interest:
                        section_attribute_values[j][attr] += rgetattr(items[i].domain_object, attr)

        return ConstraintSolutionSectionSet(
            sections=tuple(
                ConstraintSolutionSection(
                    section_object=self._sections[j],
                    section_score=section_scores[j],
                    section_attribute_values=section_attribute_values[j],
                    section_candidates=tuple(section_items[j])
                )
                for j in range(len(self._sections))
            )
        )