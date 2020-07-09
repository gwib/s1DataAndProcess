#!/usr/local/bin/bash
# enable next line for debugging purpose
# set -x 

############################################
# User Configuration
############################################

# adapt this path to your needs
# path to commands


############################################
# Command line handling
############################################

# use third parameter for path to source products
sourceDirectory="$1"

# use fourth parameter for path to target products
targetDirectory="$2"

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
  targetFile="${targetDirectory}/$(removeExtension "$(basename ${F})")_nodata.tif"
  echo "Filenames"
  echo "In: $F"
  echo "Target: $targetFile"
  gdal_translate -a_nodata 0 -of GTiff ${F} ${targetFile}
  #${gptPath} ${graphXmlPath} -e -t ${targetFile} ${sourceFile} -x
done
