'''License notice
Copyright 2024, Andreas Einwiller <einwil01@ads.uni-passau.de> \
Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.  This file is offered as-is,
without any warranty. \
SPDX-License-Identifier: FSFAP
'''
import signal
from typing import List

from spreadsheet_solver import InvalidConfig
from spreadsheet_solver.data_types import DecisionVariable


class Timeout(Exception):
    """Exception raised when optimization problem can not be solved within a set time."""

    def __init__(self, message="Invalid config file."):
        self.message = message
        super().__init__(self.message)


class Solver:
    """Solver for linear optimization problem."""

    # call Solver.allowed_criteria()
    @staticmethod
    def allowed_criteria() -> List[str]:
        """TODO docstring"""
        return ["max", "min"]

    # call Solver.epsilon_comp_val()
    @staticmethod
    def epsilon_comp_val() -> float:
        """TODO docstring"""
        return 1e-7

    def __init__(
        self,
        timeout: int,
        criterion: str,
        decision_variables: dict,
        constraint_variables: dict,
    ):
        """TODO docstring"""
        self.timeout = timeout
        if criterion not in Solver.allowed_criteria():
            raise InvalidConfig(
                (
                    f"An error occurred while trying to initialize the solver. "
                    f'The criterion "{criterion}" is not allowed. '
                    f"Only the following criteria are allowed: "
                    f"{Solver.allowed_criteria()}."
                )
            )
        self.criterion = criterion
        self.decision_variables_name_map: dict = decision_variables
        # convert dict to list
        self.decision_variables: List[DecisionVariable] = []
        for decision_variable_name, decision_variable in decision_variables.items():
            if decision_variable.lower_bound is None:
                raise InvalidConfig(
                    (
                        f"An error occurred while trying to initialize the solver. "
                        f"The decision variable {decision_variable.name} requires an "
                        f"lower bound constraint."
                    )
                )
            if decision_variable.upper_bound is None:
                raise InvalidConfig(
                    (
                        f"An error occurred while trying to initialize the solver. "
                        f"The decision variable {decision_variable.name} requires an "
                        f"upper bound constraint."
                    )
                )
            self.decision_variables.append(decision_variable)
        self.number_decision_variables: int = len(decision_variables)
        self.constraint_variables = constraint_variables
        self.optimum = None
        self.optimal_decision_variable_values = []

    def any_violated_constraints(self) -> bool:
        """TODO docstring"""
        if self.constraint_variables is None:
            return False
        for (
            constraint_variable_name,
            constraint_variable,
        ) in self.constraint_variables.items():
            _sum = 0
            for dv_name, dv_cost in constraint_variable.dependencies:
                dv_value = self.decision_variables_name_map[dv_name].value
                _sum += dv_value * dv_cost

            sum_left: float = _sum
            sum_right: float = constraint_variable.constraint_value

            if constraint_variable.comparison_operator == "<=":
                if sum_left > (sum_right + Solver.epsilon_comp_val()):
                    return True
            if constraint_variable.comparison_operator == "<":
                if sum_left >= sum_right:
                    return True
            if constraint_variable.comparison_operator == ">=":
                if sum_left < (sum_right - Solver.epsilon_comp_val()):
                    return True
            if constraint_variable.comparison_operator == ">":
                if sum_left <= sum_right:
                    return True
        # no violation, return True
        return False

    def objective_function(self) -> float:
        """TODO docstring"""
        result = 0
        for decision_variable in self.decision_variables:
            result += decision_variable.unit_profit * decision_variable.value
        return result

    def brute_force(self, index=0) -> None:
        """TODO docstring"""
        # solver method
        # lin prog optimization
        # generate nested for loop over all decision variables
        # adjust decision variable values inplace, save optimal values
        if self.number_decision_variables <= 0:
            return
        for dv_value in range(
            self.decision_variables[index].lower_bound,
            self.decision_variables[index].upper_bound + 1,
        ):
            self.decision_variables[
                index
            ].value = dv_value  # update decision value inplace - efficient solution!
            if index + 1 < self.number_decision_variables:
                self.brute_force(index + 1)
            else:
                # given all decision variable values, calculate total profit and check for optimal solution
                result = self.objective_function()
                # check for constraint violations, if any then continue
                if self.any_violated_constraints():
                    continue
                # pot. store optimal decision variable values, given criterion
                if not self.optimum is None:
                    if self.criterion == "max":
                        if result <= self.optimum:
                            continue
                    if self.criterion == "min":
                        if result >= self.optimum:
                            continue
                # optimal decision variable values (at this iteration state) -> update optimum and dv_values
                optimal_dv_values = []
                for index in range(self.number_decision_variables):
                    optimal_dv_values.append(self.decision_variables[index].value)
                self.optimum = result
                self.optimal_decision_variable_values = optimal_dv_values

    def set_optimal_decision_variable_values(self) -> None:
        """TODO docstring"""
        # can only set values if there is a solution to the problem
        if self.optimum is not None:
            for index, optimal_decision_variable_value in enumerate(
                self.optimal_decision_variable_values
            ):
                self.decision_variables[index].value = optimal_decision_variable_value

    def print_solution(self):
        """TODO docstring"""
        if self.optimum is None:
            print("Objective could not be solved.")
            return
        # print objective
        print(f"Objective: {self.optimum}")
        # print constraint variables
        if self.constraint_variables:
            for (
                constraint_variable_name,
                constraint_variable,
            ) in self.constraint_variables.items():
                left_sum = 0
                for dv_name, dv_cost in constraint_variable.dependencies:
                    dv_value = self.decision_variables_name_map[dv_name].value
                    left_sum += dv_value * dv_cost
                print(f"{constraint_variable}, left_sum={left_sum}")
        # print decision variables
        for decision_variable in self.decision_variables:
            print(decision_variable)
        print("")

    def timeout_handler(self, signum, frame):
        """TODO docstring"""
        raise TimeoutError(f"Solver function timed out after {self.timeout} seconds.")

    def solve(self) -> None:
        """TODO docstring"""
        signal.signal(signal.SIGALRM, self.timeout_handler)
        signal.alarm(self.timeout)
        try:
            self.brute_force()
            self.set_optimal_decision_variable_values()
        except Timeout as e:
            raise Timeout(e.message)
        finally:
            signal.alarm(0)
