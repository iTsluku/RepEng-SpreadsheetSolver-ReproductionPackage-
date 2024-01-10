# Functional Replication of Spreadsheet Solver

# Copyright 2024, Andreas Einwiller <einwil01@ads.uni-passau.de>
# Copying and distribution of this file, with or without modification, 
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.
# SPDX-License-Identifier: FSFAP

FROM python:3.9-slim

LABEL maintainer="Andreas Einwiller einwil01@ads.uni-passau.de"

# Setup working directory
WORKDIR /app

# Create venv
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Install required packages
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

# Make the paper config execution script executable
RUN chmod +x run_paper_configurations.sh

# Set default command
CMD ["./run_paper_configurations.sh"]