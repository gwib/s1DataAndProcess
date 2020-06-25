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
    echo "$(echo "$file" | sed -E 's/\.[^\.]*$//')"
    #date_extr="$([[ "$file" =~ ([0-9]{8}T[0-9]{6}) ]] && echo "${BASH_REMATCH[1]}")"
#    date_extr="$([[ "$file" =~ ([0-9]{8}) ]] && echo "${BASH_REMATCH[1]}")"
#    echo "FCC_Sigma0_HHHV_$date_extr"
}

############################################
# Main processing
############################################

# Create the target directory
mkdir -p "${targetDirectory}"

# the d option limits the elemeents to loop over to directories. Remove it, if you want to use files.
for F in $(ls -1d "${sourceDirectory}"/*.tif); do #TODO: change filename and extension
  targetFile="${targetDirectory}/$(removeExtension "$(basename ${F})")_clipped.tif"
  echo "Filenames"
  echo "In: $F"
  echo "Target: $targetFile"
  gdal_translate -projwin -395238.4066986203 -2118490.8478196627 -260059.74896617507 -2256690.5412598336 -of GTiff ${F} ${targetFile}
  #${gptPath} ${graphXmlPath} -e -t ${targetFile} ${sourceFile} -x
done
