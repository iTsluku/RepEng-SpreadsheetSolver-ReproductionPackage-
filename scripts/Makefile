# Copyright 2024, Andreas Einwiller <einwil01@ads.uni-passau.de>
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.
# SPDX-License-Identifier: FSFAP

# Reference code and documentation: https://tex.stackexchange.com/questions/40738/how-to-properly-make-a-latex-project
# Note: This Makefile will be moved to the report/ directory once the report repository is cloned (see Dockerfile)

.PHONY: report.pdf all clean

all: report.pdf

report.pdf: report.tex
	latexmk -pdf -pdflatex="pdflatex -interaction=nonstopmode" -use-make report.tex

report: report.pdf

clean:
	latexmk -CA