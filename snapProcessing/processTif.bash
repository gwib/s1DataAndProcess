#!/bin/bash
# enable next line for debugging purpose
# set -x 

############################################
# User Configuration
############################################

# adapt this path to your needs
#export PATH=~/progs/snap/bin:$PATH
#gptPath="gpt"
gptPath="$snapGPT"

############################################
# Command line handling
############################################

# first parameter is a path to the graph xml
graphXmlPath="$1"

# second parameter is a path to a parameter file
# parameters are hard-coded in XML file
#parameterFilePath="$2"

# use third parameter for path to source products
sourceDirectory="$2"

# use fourth parameter for path to target products
targetDirectory="$3"

# the fifth parameter is a file prefix for the target product name, typically indicating the type of processing
targetFilePrefix="$4"

   
############################################
# Helper functions
############################################
removeExtension() {
    file="$1"
#    echo "$(echo "$file" | sed -r 's/\.[^\.]*$//')"
    echo "$(echo "$file" | sed -E 's/\.[^\.]*$//')"
}


############################################
# Main processing
############################################

# Create the target directory
mkdir -p "${targetDirectory}"

# the d option limits the elemeents to loop over to directories. Remove it, if you want to use files.
for F in $(ls -1d "${sourceDirectory}"/*.tif); do #TODO: change filename and extension
  sourceFile="$(realpath "$F")"
  targetFile="${targetDirectory}/${targetFilePrefix}_$(removeExtension "$(basename ${F})").dim"
  ${gptPath} ${graphXmlPath} -e -t ${targetFile} ${sourceFile} -x
done
