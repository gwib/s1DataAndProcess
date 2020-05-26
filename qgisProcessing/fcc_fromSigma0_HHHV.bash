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
    #date_extr="$([[ "$file" =~ ([0-9]{8}T[0-9]{6}) ]] && echo "${BASH_REMATCH[1]}")"
    date_extr="$([[ "$file" =~ ([0-9]{8}) ]] && echo "${BASH_REMATCH[1]}")"
    echo "FCC_Sigma0_HHHV_$date_extr"
}

############################################
# Main processing
############################################

# Create the target directory
mkdir -p "${targetDirectory}"

# the d option limits the elemeents to loop over to directories. Remove it, if you want to use files.
for F in $(ls -1d "${sourceDirectory}"/WinsvoldGRD*.data); do #TODO: change filename and extension
  hhFile="$(realpath "$F")/Sigma0_HH_db.img"
  hvFile="$(realpath "$F")/Sigma0_HV_db.img"
  targetFile="${targetDirectory}/$(removeExtension "$(basename ${F})").tif"
  echo "Filenames"
  echo "HH: $hhFile"
  echo "HV: $hvFile"
  echo "Target: $targetFile"
  #${gptPath} ${graphXmlPath} -e -t ${targetFile} ${sourceFile} -x
done
