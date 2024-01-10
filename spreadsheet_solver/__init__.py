'''License notice
Copyright 2024, Andreas Einwiller <einwil01@ads.uni-passau.de> \
Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.  This file is offered as-is,
without any warranty. \
SPDX-License-Identifier: FSFAP
'''

class InvalidConfig(Exception):
    """Exception raised for invalid user input in the config file."""

    def __init__(self, message="Invalid config file."):
        self.message = message
        super().__init__(self.message)
