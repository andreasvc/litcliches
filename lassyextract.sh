#!/bin/bash
# Extract tokenized text from Lassy Large.
# Output is one file per section, one sentence per line, space-separated tokens
# including original punctuation and capitalization.

set -e

# The input for these sections consists of tokenized text.
# Strip sentence ID if any, concatenate into a single file.
for a in EINDHOVEN EMEA EUROPARL NLWIKI20110804 SENSEVAL TROONREDE;
do
	echo $a
	find $a/SUITES -name '*.gz' -print \
		| xargs zcat | sed -r 's/^[^|]*\|//' \
		> lassy-$a.tok
done

# The input for SONAR was POS tagged, strip tags:
echo SONAR
find SONAR/SUITES -name '*.gz' -print \
	| xargs python3 filtertags.py -o lassy-SONAR.tok
