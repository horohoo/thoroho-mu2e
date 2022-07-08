#######################################################################
# A python script for plotting the PE yield in each channel over time #
# for the Mu2e cosmic ray veto. This script needs to be changed for   #
# each run, as the script has hard-coded info about the dates and     #
# number of runs. It is critical to import files in chronological     #
# order (i.e. the order in which the runs happened                    #
# Created on Thu 7 July 2022                                          #
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
    date = np.zeros(nfiles)
    PE_yield = np.zeros(nfiles)
    for i in range(nfiles):
        d["data_{0}".format(i)] = np.genfromtxt(str(sys.argv[i + 1]), skip_header=2)
        
        # hard-coded information about dates of runs
        if i <= 1:
            date[i] = datetime.datetime(2021, 7, 8)
        if i >= 2 and i <= 14:
            date[i] = datetime.datetime(2021, 12, 10)
        if i >= 15 and i <= 25:
            date[i] = datetime.datetime(2022, 1, 12)
        if i == 26:
            date[i] = datetime.datetime(2022, 2, 15)
        if i == 27:
            date[i] = datetime.datetime(2022, 2, 25)
        if i == 28:
            date[i] = datetime.datetime(2022, 3, 7)
        if i == 29:
            date[i] = datetime.datetime(2022, 3, 10)
        if i >= 30 and i <= 32:
            date[i] = datetime.datetime(2022, 3, 18)
        if i == 33:
            date[i] = datetime.datetime(2022, 4, 27)
        if i == 34 or i == 35:
            date[i] = datetime.datetime(2022, 4, 29)
        if i >= 36 and i <= 40:
            date[i] = datetime.datetime(2022, 5, 2)
        if i == 41:
            date[i] = datetime.datetime(2022, 5, 11)

    # now that the data is imported, loop through each FEB/channel and plot data
    for j in range(128): # 0-63 are FEB 0 and 64-127 are FEB 1
        for i in range(nfiles):
            data = d["data_{0}".format(i)]
            PE_yield[i] = data[j, 3]
        if j < 64:
            feb = 0
            channel = j
        else:
            feb = 1
            channel = j - 64
        plt.scatter(date, PE_yield)
        plt.xlabel('Date of run')
        plt.ylabel('PE yield')
        plt.title('PE yield over time for FEB {0}, channel {1}'.format(feb, channel))
        plt.savefig('aging_feb{0}_ch{1}.pdf'.format(feb, channel))
