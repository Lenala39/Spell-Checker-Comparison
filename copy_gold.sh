#!/usr/bin/env bash
for i in *.txt; do mv %i ${i%.txt}_gold.txt;done;