#!/bin/bash
# Copyright 2024, Andreas Einwiller <einwil01@ads.uni-passau.de>
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.
# SPDX-License-Identifier: FSFAP

SCRIPT_PATH=$(dirname $(realpath -s "$0"))

# Print error message and exit
function error_exit {
    echo "Smoke test failed! $1" >&2
    exit 1
}

# Check if command exists
function command_exists {
    command -v "$1" >/dev/null 2>&1
}

# Software to be invoked
software=("latexmk" "python3" "git" "make")

# Check if each required software dependency is installed
for app in "${software[@]}"; do
    if ! command_exists "$app"; then
        error_exit "Required software '$app' is not installed."
    fi
done

# Check if the software dependency reacts
for app in "${software[@]}"; do
    version_output="$($app --version)"
    if [[ $? -ne 0 ]]; then
        error_exit "Could not to get version of '$app'."
    else
        echo "Version of '$app': $version_output"
    fi
done

# Packages to be invoked
packages=("pyyaml")

# Check for Python packages using requirements.txt
for package in "${packages[@]}"; do
  if ! pip3 show "$package" &>/dev/null; then
      error_exit "Python package '$package' is not installed."
  else
      echo "Invoking Python package '$package':"
      pip3 show "$package"
  fi
done

# If all checks passed, print success message
echo "Smoke test passed. Required software is installed and reacting."