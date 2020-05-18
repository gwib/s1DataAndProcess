#!/bin/bash
# enable next line for debugging purpose
# set -x 

if [ -f /shared/thesis/sigma0/WinsvoldGRD_Sigma0_Subset_Orb_TN_Cal__S1B_IW_GRDH_1SDH_20190717T101604_20190717T101629_017172_02042_A807.dim ]; then
 echo "$FILE exist"
else
	echo "File does not exist"
fi
