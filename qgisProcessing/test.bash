#!/usr/local/bin/bash
[[ "TestT100String" =~ ([0-9]+) ]] && echo "${BASH_REMATCH[1]}"