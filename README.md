# Functional Replication Package: Spreadsheet Solver
This site provides the functional replication package which aims to replicate the functionality of the spreadsheet solver in order to achieve identical output values for all three scenarios defined in Head First Data Analysis chapter three.

## Building the Docker image
- Clone the repository
    > git clone https://github.com/iTsluku/RepEng-SpeadsheetSolver-ReproductionPackage.git
- Build the Docker image from scratch
    > docker build -t spreadsheet-solver:1.1 .

## Run docker container and perform measurements
- Run spreadsheet solver with all three paper configurations in docker container
    > docker run --name spreadsheet-solver --rm spreadsheet-solver:1.1

## Performing measurements in the Docker container
The following steps are identical for container-based run.

- Access the container interactively
    > docker run -it --name spreadsheet-solver --rm spreadsheet-solver:1.1 /bin/bash
- Run dispatcher
    > ./scripts/doAll.sh
- Run spreadsheet solver with specified config w.r.t. paper scenario one, two or three
  ```bash
  python main.py --config "configs/head_first_data_analysis_chap3/scenario1.yaml"
  python main.py --config "configs/head_first_data_analysis_chap3/scenario2.yaml"
  python main.py --config "configs/head_first_data_analysis_chap3/scenario3.yaml"
  ```
- Exit container
    > exit
  
## Mounting (Retrieve report.pdf or run custom experiment)
The following steps are not relevant for the functional replication, but make it possible to configure new scenarios (independent of the original paper) outside the container, process them in the container and extract the artifacts from the container.
Furthermore, mounting provides a convenient solution to retrieve the report.

- Run docker container with volume mount in interactive mode
  ```bash
  docker run -v /abs/user/path/to/shared_dir:/app/shared_dir/ \
             -it \
             --name spreadsheet-solver \
             --rm \
             spreadsheet-solver:1.1 \
             /bin/bash
  ```
- Run dispatcher
    > ./scripts/doAll.sh
- Report (report.pdf) will be in /abs/user/path/to/shared_dir/ (user) and /app/shared_dir/ (container)
- Run spreadsheet solver with config of mounted volume
    > python main.py --config "shared_dir/my_special_config.yaml"
- Exit container
    > exit

## License
Copyright 2024, Andreas Einwiller <einwil01@ads.uni-passau.de>
Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.  This file is offered as-is,
without any warranty.
SPDX-License-Identifier: FSFAP
