#!/bin/bash
# Copyright 2024, Andreas Einwiller <einwil01@ads.uni-passau.de>
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.
# SPDX-License-Identifier: FSFAP

SCRIPT_PATH=$(dirname $(realpath -s "$0"))
PAPER_CONFIG_DIR="$SCRIPT_PATH/../configs/head_first_data_analysis_chap3/"

echo "Running smoke test"
(cd "$SCRIPT_PATH" && ./smoke.sh)

echo "Removing unnecessary paper artefacts"
(cd "$SCRIPT_PATH" && ./cleanup_paper_artefacts.sh)

echo "Running experiments"
for config_file in "$PAPER_CONFIG_DIR"*.yaml; do
    echo "Running "$(basename "$config_file")""
    python "$SCRIPT_PATH"/../main.py --config "$config_file"
done

echo "Building report"
(cd "$SCRIPT_PATH" && ./build_report.sh)
