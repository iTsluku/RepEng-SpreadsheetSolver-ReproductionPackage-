# Functional Replication of Spreadsheet Solver

# Copyright 2024, Andreas Einwiller <einwil01@ads.uni-passau.de>
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.
# SPDX-License-Identifier: FSFAP

# Linux LTS base image
FROM ubuntu:22.04

LABEL maintainer="Andreas Einwiller einwil01@ads.uni-passau.de"

# Copy artefacts
COPY . /app/
# Setup working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y python3 python3-pip python3.10-venv
RUN pip3 install --upgrade pip

# Create venv
RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Install required packages
RUN pip3 install -r requirements.txt

# Make the paper config execution script executable
RUN chmod +x run_paper_configurations.sh

# Set default command that is run when the container is run based on this image
CMD ["./run_paper_configurations.sh"]