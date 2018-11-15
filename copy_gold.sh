#!/usr/bin/env bash
# use while in gold folder with files named i.txt
# loop over all txt files
# mv each file ($i) to i_gold.txt
# string substitution: i%.txt removes ".txt" from i and _gold.txt is appended
# http://tldp.org/LDP/abs/html/string-manipulation.html -> substring removal

for i in *.txt; do mv $i ${i%.txt}_gold.txt; done;