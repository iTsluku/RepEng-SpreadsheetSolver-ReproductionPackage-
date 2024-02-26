#!/bin/bash
# Copyright 2024, Andreas Einwiller <einwil01@ads.uni-passau.de>
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.
# SPDX-License-Identifier: FSFAP

# Copy experiment results (stored in datasets/replication) to report/data/replication

SCRIPT_PATH=$(dirname $(realpath -s "$0"))

# Check if the destination directory exists
if [ ! -d "report/data/replication" ]; then
    echo "Directory report/data/replication does not exist."
    exit 1
fi

# Copy *.csv files
for file in "datasets/replication"/*.csv; do
    cp "$file" "report/data/replication"
    echo "Copied file $filename from datasets/replication to report/data/replication"
done