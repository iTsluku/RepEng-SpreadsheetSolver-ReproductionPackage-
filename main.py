'''License notice
Copyright 2024, Andreas Einwiller <einwil01@ads.uni-passau.de> \
Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.  This file is offered as-is,
without any warranty. \
SPDX-License-Identifier: FSFAP
'''
import argparse
import os

from spreadsheet_solver.config import Config, InvalidConfig
from spreadsheet_solver.solver import Solver, Timeout

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spreadsheet solver.")
    parser.add_argument(
        "--config",
        default=os.path.join(os.path.dirname(os.path.abspath(__file__)),"configs/config.yaml"),
        help="Path to the configuration file.",
    )
    args = parser.parse_args()
    try:
        config = Config(args.config)
        timeout = config.get_timeout()
        criterion = config.get_criterion()
        decision_variables = config.get_decision_variables(apply_constraints=True)
        constraint_variables = config.get_constraint_variables()
        solver = Solver(
            timeout=timeout,
            criterion=criterion,
            decision_variables=decision_variables,
            constraint_variables=constraint_variables,
        )
        solver.solve()
        solver.print_solution()
    except InvalidConfig as e:
        print(e)
    except Timeout as e:
        print(e)
