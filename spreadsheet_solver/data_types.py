'''License notice
Copyright 2024, Andreas Einwiller <einwil01@ads.uni-passau.de> \
Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.  This file is offered as-is,
without any warranty. \
SPDX-License-Identifier: FSFAP
'''
from typing import List, Tuple, Optional

from spreadsheet_solver import InvalidConfig


class DecisionVariable:
    """Define decision variables and apply constraints."""

    value: int = None
    lower_bound: Optional[int] = None
    upper_bound: Optional[int] = None

    # call DecisionVariable.allowed_comparison_operators()
    @staticmethod
    def allowed_comparison_operators() -> List[str]:
        """TODO docstring"""
        return ["<", "<=", ">", ">="]

    def __init__(self, name: str, unit_profit: float) -> None:
        """TODO docstring"""
        self.name: str = name
        self.unit_profit: float = float(unit_profit)

    def __str__(self) -> str:
        """TODO docstring"""
        return (
            f"Decision Variable: name={self.name}, count={self.value}, unit profit={self.unit_profit}, "
            f"constraint=[{self.lower_bound}, {self.upper_bound}]"
        )

    def apply_constraint(self, comparison_operator: str, value: int) -> None:
        """TODO docstring"""
        from typing import List, Tuple, Optional
        if comparison_operator not in DecisionVariable.allowed_comparison_operators():
            raise InvalidConfig(
                (
                    f"An error occurred while trying to applying a constraint to the "
                    f"decision variable {self.name}. "
                    f'The operator "{comparison_operator}" is not allowed. '
                    f"Only the following comparison operators are allowed to set a lower or "
                    f"upper bound: {DecisionVariable.allowed_comparison_operators()}."
                )
            )
        # check if new constraint is more strict than current lower and upper bound
        if comparison_operator == "<=":
            if self.upper_bound is None or value < self.upper_bound:
                self.upper_bound = value
        if comparison_operator == "<":
            if self.upper_bound is None or value - 1 < self.upper_bound:
                self.upper_bound = value - 1
        if comparison_operator == ">=":
            if self.lower_bound is None or value > self.lower_bound:
                self.lower_bound = value
        if comparison_operator == ">":
            if self.lower_bound is None or value + 1 > self.lower_bound:
                self.lower_bound = value + 1

        # check if lower_bound is still <= upper bound
        # requires lower and upper bound to be initialized :: both values not None
        if self.lower_bound and self.upper_bound:
            if self.lower_bound > self.upper_bound:
                raise InvalidConfig(
                    (
                        f"An error occurred while trying to applying a constraint to the "
                        f"decision variable {self.name}. Lower bound has to remain "
                        f"less or equal compared to the upper bound."
                    )
                )


class ConstraintVariable:
    """Constraints based on one or multiple decision variables."""

    @staticmethod
    def allowed_comparison_operators() -> List[str]:
        """TODO docstring"""
        return ["<", "<=", ">", ">="]

    def __init__(
        self,
        name: str,
        dependencies: List[Tuple[str, float]],
        comparison_operator: str,
        constraint_value: float,
    ):
        """TODO docstring"""
        self.name: str = name
        # decision variable name (lookup value later), decision varibale cost
        self.dependencies: List[Tuple[str, float]] = dependencies
        for (
            index,
            (dv_name, dv_cost),
        ) in enumerate(self.dependencies):
            self.dependencies[index] = (dv_name, float(dv_cost))
        self.comparison_operator: str = comparison_operator
        self.constraint_value: float = float(constraint_value)

    def __str__(self):
        """TODO docstring"""
        _repr = ""
        _repr += f"Constraint Variable: name={self.name}, constraint="
        for dv_name, dv_cost in self.dependencies:
            _repr += f"{dv_cost}*{dv_name}_count + "
        _repr = _repr.rstrip("+ ")
        _repr += f" {self.comparison_operator} {self.constraint_value}"
        return _repr
