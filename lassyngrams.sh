#!/bin/bash
# Extract all n-grams with n from 1..5 with a frequency threshold of 40.
# Beware, creates huge file (tens of GBs).
# Pass one or more filenames with tokenized text as arguments.

set -e

tmp=$(mktemp --tmpdir=.)

echo "Class encoding corpora...">&2
colibri-classencode -o ${tmp} -u $@

echo "Building pattern model...">&2
colibri-patternmodeller -c ${tmp}.colibri.cls -f ${tmp}.colibri.dat -t 1 -m 1 -l 5 -u -o lassyngram.model

echo "Writing lassy-$n-grams.txt ...">&2
colibri-patternmodeller -c lassygroot.cls -f lassygroot.dat -u -t 40 -m 1 -l 5 -P \
	> lassy-ngrams.txt
