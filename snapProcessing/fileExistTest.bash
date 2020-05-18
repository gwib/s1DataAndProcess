#!/bin/bash
# enable next line for debugging purpose
# set -x 

# first parameter is a path to the graph xml
sourceDirectory="$1"

# second parameter is a path to a parameter file
# parameters are hard-coded in XML file
targetDirectory="$2"

############################################
# Helper functions
############################################
removeExtension() {
    file="$1"
    echo "$(echo "$file" | sed -r 's/\.[^\.]*$//')"
}

#################################################


for F in $(ls -1d "${sourceDirectory}"/*.dim); do
  sourceFile="$(realpath "$F")"
  targetFile="${targetDirectory}/WinsvoldGRD_Sigma0_$(removeExtension "$(basename ${F})").dim"
  if [ -f ${targetFile} ]; then
  	echo "${targetFile} already exists. No action needed"
  else
	echo "${targetFile} does not exist. Processing graph."
fi
done
