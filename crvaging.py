#######################################################################
# A python script for plotting the PE yield in each channel over time #
# for the Mu2e cosmic ray veto. This script needs to be changed for   #
# each run, as the script has hard-coded info about the dates and     #
# number of runs. It is critical to import files in chronological     #
# order (i.e. the order in which the runs happened                    #
# Created on Thu 7 July 2022                                         #
# @author: Tyler Horoho                                               #
#######################################################################

import sys
import numpy as np
import matplotlib.pyplot as plt
import datetime

nfiles = len(sys.argv) - 1

d = {} # dictionary to store data in the loop over input files

if (nfiles == 0):
    print("No files provided")

else:
    # import the data
    for i in range(1, nfiles + 1):
        d["data_{0}".format(i)] = np.genfromtxt(str(sys.argv[i]), skip_header=2)
        
        # hard-coded information about dates of runs
        # an example of the first run (66)
        if i <= 2:
            d["date_{0}".format(i)] = datetime.datetime(2021, 7, 8)
        # do this for the other dates and check the number of files

    # now that the data is imported, loop through each FEB/channel and plot data
    for j in range(128): # 0-63 are FEB 0 and 64-127 are FEB 1
        np.append(PE_yield, 
