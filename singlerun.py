#######################################################################
# A python script for plotting the PE yield in each channel for a     #
# single run in order to check for fluctations in the PE yield. This  #
# script needs to be changed for each run, as the script has          #
# hard-coded info about the runs. For the first instance I chose run  #
# 94, which ran for 26 days. It contains 12 files (numbered 0-11).    #
# Each files contains approximately two days worth of data            #
# Created on Mon 1 August 2022                                        #
# @author: Tyler Horoho                                               #
#######################################################################

import sys
import numpy as np
import matplotlib.pyplot as plt

nfiles = 12
d = {}
filehead = '/pnfs/mu2e/scratch/users/thoroho/recotar/crvreco/rec.mu2e.CRV_wideband_cosmics.crvaging-001.000094_0'
# import the data
run = np.arange(nfiles)
PE_yield = np.zeros(nfiles)
for i in range(nfiles):
    # hard-coded information about dates of runs
    if i < 10:
        d["data_{0}".format(i)] = np.genfromtxt(filehead + '0' + str(i) + '.txt', skip_header=2)
    if i >= 10 and i <= 11:
        d["data_{0}".format(i)] = np.genfromtxt(filehead + str(i) + '.txt', skip_header=2)

# now that the data is imported, loop through each FEB/channel and plot data

for j in range(128): # 0-63 are FEB 0 and 64-127 are FEB 1
    for i in range(nfiles):
        data = d["data_{0}".format(i)]
        PE_yield[i] = data[j, 3]
    print(PE_yield)
        
    mean = round(np.mean(data), 2)
    std = round(np.std(data), 2)
    print(np.mean(data), mean)
    print(np.std(data), std)

    if j < 64:
        feb = 0
        channel = j
    else:
        feb = 1
        channel = j - 64
    
    plt.figure(num=j)
    plt.plot(run, PE_yield, 'r.')
    plt.text(1, 20, 'PE yield: {0} +/- {1}'.format(mean, std))
    plt.ylim(0,50)
    plt.xlabel('Run # (approx 2 days)')
    plt.ylabel('PE yield')
    plt.title('PE yield of run 94, FEB {0}, channel {1}'.format(feb, channel))
    plt.savefig('run94/run94_feb{0}_ch{1}.pdf'.format(feb, channel))
    plt.close(fig=j)
    

#
