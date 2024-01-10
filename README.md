# Functional Replication Package: Spreadsheet Solver
This site provides the functional reproduction package which aims to replicate the functionality of the spreadsheet solver in order to achieve identical output values for all three scenarios defined in Head First Data Analysis chapter three.

## Building the Docker image
- Clone the repository
    > git clone https://github.com/iTsluku/RepEng-SpeadsheetSolver-ReproductionPackage.git
- Build the Docker image from scratch
    > docker build -t spreadsheet-solver:1.0 .

## Run docker container and perform measurements
- Run spreadsheet solver with paper configurations in docker container
    > docker run --name spreadsheet-solver spreadsheet-solver:1.0
- Cleanup
    > docker stop spreadsheet-solver
    > docker remove spreadsheet-solver

## Performing measurements in the Docker container
The following steps are identical for container-based run.

- Access the container interactively
    > docker run -it --name spreadsheet-solver spreadsheet-solver:1.0 /bin/bash
- Run spreadsheet solver with specified config w.r.t. paper scenarios
    > python main.py --config "config/head_first_data_analysis_chap3/config1.yaml"
    > python main.py --config "config/head_first_data_analysis_chap3/config2.yaml"
    > python main.py --config "config/head_first_data_analysis_chap3/config3.yaml"
- Exit container
    > exit
- Cleanup
    > docker stop spreadsheet-solver
    > docker remove spreadsheet-solver


## Mounting
The following steps are not relevant for the functional replication, but make it possible to configure new scenarios (independent of the original paper) outside the container, process them in the container and extract the artifacts from the container.

- Run docker container with volume mount in interactive mode
    > docker run -v /user/path/to/my_config_dir:/app/my_config_dir/ -it --name spreadsheet-solver spreadsheet-solver:1.0 /bin/bash
- Run spreadsheet solver with config from mounted directory
    > python main.py --config "my_config_dir/config.yaml"
- Exit container
    > exit
- Cleanup
    >docker stop spreadsheet-solver
    >docker remove spreadsheet-solver

## License
Copyright 2024, Andreas Einwiller <einwil01@ads.uni-passau.de>
Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.  This file is offered as-is,
without any warranty.
SPDX-License-Identifier: FSFAP
