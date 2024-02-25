#!/bin/bash
# Copyright 2024, Andreas Einwiller <einwil01@ads.uni-passau.de>
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.
# SPDX-License-Identifier: FSFAP

SCRIPT_PATH=$(dirname $(realpath -s "$0"))

RUN test -d "$SCRIPT_PATH"/../report || mkdir "$SCRIPT_PATH"/../report
cd "$SCRIPT_PATH"/../report

# Run make report
make report

# Move report.pdf to shared_dir/ (potentially mounted volume)
RUN test -d "$SCRIPT_PATH"/../shared_dir || mkdir "$SCRIPT_PATH"/../shared_dir
mv report.pdf "$SCRIPT_PATH"/../shared_dir/

# Run make clean
make clean