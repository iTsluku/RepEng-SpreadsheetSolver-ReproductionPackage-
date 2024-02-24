#!/bin/bash
# Copyright 2024, Andreas Einwiller <einwil01@ads.uni-passau.de>
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.
# SPDX-License-Identifier: FSFAP

# shellcheck disable=SC2046
SCRIPT_PATH=$(dirname $(realpath -s "$0"))
PAPER_CONFIG_DIR="$SCRIPT_PATH/../configs/head_first_data_analysis_chap3/"

for config_file in "$PAPER_CONFIG_DIR"*.yaml; do
    # shellcheck disable=SC2027
    echo "Solving "$(basename "$config_file")":"
    python "$SCRIPT_PATH"/../main.py --config "$config_file"
done
