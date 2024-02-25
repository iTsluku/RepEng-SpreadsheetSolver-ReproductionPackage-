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

# Fix: tzdata hangs during Docker image build
# Reference: https://dev.to/grigorkh/fix-tzdata-hangs-during-docker-image-build-4o9m
# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
ENV TZ=Atlantic/Jan_Mayen
RUN ln -snf /usr/share/zoneinfo/${TZ} /etc/localtime && echo ${TZ} > /etc/timezone

ENV HOME=/app

# Copy artefacts
COPY . ${HOME}
# Setup working directory
WORKDIR ${HOME}

# Install dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    git \
    latexmk \
    make \
    python3 \
    python3-pip \
    python3.10-venv \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-latex-recommended \
    texlive-latex-extra

RUN pip3 install --upgrade pip

# Create venv
RUN python3 -m venv venv
ENV PATH="/app/venv/bin:${PATH}"

# Install required packages
RUN pip3 install -r requirements.txt

# Make scripts executable
RUN chmod +x ${HOME}/scripts/do_all.sh
RUN chmod +x ${HOME}/scripts/smoke.sh
RUN chmod +x ${HOME}/scripts/build_report.sh


# Clone report (into existing report/ directory)
RUN git clone https://github.com/iTsluku/RepEng-SpreadsheetSolver-Report-.git report
RUN mv ${HOME}/scripts/Makefile ${HOME}/report/

# Set default command that is run when the container is run based on this image
CMD ${HOME}/scripts/do_all.sh