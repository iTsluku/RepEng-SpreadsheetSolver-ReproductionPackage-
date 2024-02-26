"""License notice
Copyright 2024, Andreas Einwiller <einwil01@ads.uni-passau.de> \
Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.  This file is offered as-is,
without any warranty. \
SPDX-License-Identifier: FSFAP
"""

import yaml

from typing import List, Tuple, Optional
from spreadsheet_solver import InvalidConfig
from spreadsheet_solver.data_types import DecisionVariable, ConstraintVariable


class Config:
    """Config parser replacing Excel solver spreadsheet and GUI."""

    def __init__(self, path: str):
        """Load yaml file and validate."""
        with open(path, "r") as file:
            self.data = yaml.safe_load(file)
        try:
            self.validate()
        except InvalidConfig as e:
            raise InvalidConfig(e.message)

    def validate(self):
        """Validate yaml file format/contents."""
        for key in [
            "timeout",
            "criterion",
            "decision_variables",
            "decision_variable_constraints",
            "constraint_variables",
        ]:
            if key not in self.data:
                raise InvalidConfig(
                    (
                        f"An error occurred while trying to parse the yaml config. "
                        f"The user must provide information about {key}."
                    )
                )
        if self.data["timeout"] is None:
            raise InvalidConfig(
                (
                    f"An error occurred while trying to parse the yaml config. "
                    f"The timeout upper bound must be defined to ensure termination."
                )
            )
        if self.data["criterion"] is None:
            raise InvalidConfig(
                (
                    f"An error occurred while trying to parse the yaml config. "
                    f"The criterion must be defined."
                )
            )
        if self.data["decision_variables"] is None:
            raise InvalidConfig(
                (
                    f"An error occurred while trying to parse the yaml config. "
                    f"At least one decision variable must be defined."
                )
            )

        if self.data["decision_variable_constraints"] is None:
            raise InvalidConfig(
                (
                    f"An error occurred while trying to parse the yaml config. "
                    f"Since atl east one decision variable must be defined, "
                    f"at least two decision variable constraints need to be defined "
                    f"(lower and upper bound)."
                )
            )

    def get_criterion(self) -> str:
        """Get criterion, i.e., min or max."""
        return self.data["criterion"]

    def get_timeout(self) -> int:
        """get timeout parameter, default: 10s."""
        return self.data["timeout"]

    def get_decision_variables(self, apply_constraints: bool) -> dict:
        """Get decision variables parsed of config."""
        # List[Tuple[str, float]] -> dict
        decision_variables: dict = {}
        for dv_name, dv_unit_profit in self.data["decision_variables"]:
            if dv_name in decision_variables:
                raise InvalidConfig(
                    (
                        f"An error occurred while trying to parse the decision variable "
                        f"{dv_name}. The name of each decision variable needs "
                        f"to be unique. This assumption can not be violated."
                    )
                )
            decision_variables[dv_name] = DecisionVariable(
                name=dv_name, unit_profit=dv_unit_profit
            )

        if apply_constraints:
            for (
                decision_variable_constraint
            ) in self.get_decision_variable_constraints():
                (
                    decision_variable_name,
                    comparison_operator,
                    value,
                ) = decision_variable_constraint
                decision_variables[decision_variable_name].apply_constraint(
                    comparison_operator, value
                )
        return decision_variables

    def get_decision_variable_constraints(self) -> List[Tuple[str, str, int]]:
        """Get decision variable constraints parsed of config."""
        return self.data["decision_variable_constraints"]

    def get_constraint_variables(
        self,
    ) -> Optional[dict]:
        """Get constraint variables parsed of config."""
        # Optional[List[Tuple[str, List[Tuple[str, float]], str, float]]] -> Optional[dict]
        if self.data["constraint_variables"] is None:
            return None
        constraint_variables: dict = {}
        for cv_name, dv_list, comp_op, bound_val in self.data["constraint_variables"]:
            # check if constraint variable is unique
            if cv_name in constraint_variables:
                raise InvalidConfig(
                    (
                        f"An error occurred while trying to parse the constraint variable "
                        f"{cv_name}. The name of each constraint variable needs "
                        f"to be unique. This assumption can not be violated."
                    )
                )
            # check if decision variables exist
            for dv_name, dv_cost in dv_list:
                if dv_name not in self.get_decision_variables(apply_constraints=False):
                    raise InvalidConfig(
                        (
                            f"An error occurred while trying to parse the constraint variable "
                            f"{cv_name}. The decision variable {dv_name} needs "
                            f"to be created first, before u can add it as an dependent variable."
                        )
                    )
            # check that no decision variable is used multiple times
            if len(set([dv_name for dv_name, dv_cost in dv_list])) != len(dv_list):
                raise InvalidConfig(
                    (
                        f"An error occurred while trying to parse the constraint variable "
                        f"{cv_name}. The dependent decision variables need to be unique. "
                        f"U are not allowed to use a decision variable multiple times "
                        f"when constructing a constraint variable."
                    )
                )
            # check if comparison operator is valid/allowed
            if comp_op not in ConstraintVariable.allowed_comparison_operators():
                raise InvalidConfig(
                    (
                        f"An error occurred while trying to applying a bounding constraint to the "
                        f"constraint variable {cv_name}. "
                        f'The operator "{comp_op}" is not allowed. '
                        f"Only the following comparison operators are allowed to set a lower or "
                        f"upper bound constraint: {ConstraintVariable.allowed_comparison_operators()}."
                    )
                )
            # initialize constraint variable
            constraint_variables[cv_name] = ConstraintVariable(
                name=cv_name,
                dependencies=dv_list,
                comparison_operator=comp_op,
                constraint_value=bound_val,
            )
        return constraint_variables
