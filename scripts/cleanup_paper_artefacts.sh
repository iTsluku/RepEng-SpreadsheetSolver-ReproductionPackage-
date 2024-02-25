#!/bin/bash
# Copyright 2024, Andreas Einwiller <einwil01@ads.uni-passau.de>
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.
# SPDX-License-Identifier: FSFAP

SCRIPT_PATH=$(dirname $(realpath -s "$0"))
FILES_KEEP=("bathing_friends_unlimited.xls" "historical_sales_data.xls")
ARTEFACTS_DIR="$SCRIPT_PATH"/../datasets/head_first_data_analysis_chap3/

# Check if the artifacts directory exists
if [ ! -d "$ARTEFACTS_DIR" ]; then
    echo "Artefacts directory '$ARTEFACTS_DIR' does not exist."
    exit 1
fi

# Remove files (cleanup) that are not specified prior (files_keep)
for file in "$ARTEFACTS_DIR"/*; do
    filename=$(basename "$file")
    if ! [[ " ${FILES_KEEP[@]} " =~ " $filename " ]]; then
        echo "Removing file: $filename"
        rm "$file"
    fi
done

echo "Removing all sub-directories recursively (__MACOSX,...) excluding .git/"
find "$DIRECTORY_PATH" -type d -not -path "*/.git/*" -exec rm -r {} + 2>/dev/null