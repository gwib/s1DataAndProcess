#!/bin/bash
# enable next line for debugging purpose
# set -x 

############################################
# User Configuration
############################################

# adapt this path to your needs
#export PATH=~/progs/snap/bin:$PATH
gptPath="gpt"

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
    echo "$(echo "$file" | sed -E 's/\.[^\.]*$//')"
}


############################################
# Main processing
############################################

# Create the target directory
mkdir -p "${targetDirectory}"

echo "----------------------------"
#files=($(ls -1d "${sourceDirectory}"/*))
#echo "first file"
#file1="${files[0]}"
#echo "second file"
#file2="${files[1]}"
echo "---------------"

#targetFile="${targetDirectory}/${targetFilePrefix}_$(removeExtension "$(basename ${F})").dim"
#${gptPath} ${graphXmlPath} -e -t ${targetFile} -Pmaster=${file1} -Pslave=${file2}
# the d option limits the elemeents to loop over to directories. Remove it, if you want to use files.
for F in $(ls -1d "${sourceDirectory}"/*); do

  file1=$(ls -1d "${F}"/*.zip | awk 'NR==1')
  echo $file1
  file2=$(ls -1d "${F}"/*.zip | awk 'NR==2')
  echo $file2

  echo $(basename ${F})

  echo $targetDirectory
  #sourceFile="$(realpath "$F")"
  targetFile="${targetDirectory}/${targetFilePrefix}_"$(basename ${F})".dim"
  echo $targetFile
  if [ -f "$targetFile" ]; then
    echo "$targetFile exists, no action needed"
  else
    echo "$targetFile does not exist, generating product"
    ${gptPath} ${graphXmlPath} -e -t ${targetFile} -Pmaster=${file1} -Pslave=${file2} -x
  fi
done
