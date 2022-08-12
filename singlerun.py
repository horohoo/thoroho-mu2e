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
import datetime

nfiles = 7
d = {}
filehead = '/pnfs/mu2e/scratch/outstage/ehrlich/wideband8/crvreco/rec.mu2e.CRV_wideband_cosmics.crvaging-001.00'
# import the data
date = np.array([])
PE_yield = np.zeros(nfiles)
temperature = np.zeros(nfiles)
for i in range(nfiles):
    # hard-coded information about dates of runs
    if i == 0:
        d["data_{0}".format(i)] = np.genfromtxt(filehead + '1031_000.txt', skip_header=2)
        date = np.append(date, datetime.datetime(2022, 4, 27))
    if i == 1:
        d["data_{0}".format(i)] = np.genfromtxt(filehead + '1033_000.txt', skip_header=2)
        date = np.append(date, datetime.datetime(2022, 4, 29))
    if i >= 2 and i <= 5:
        d["data_{0}".format(i)] = np.genfromtxt(filehead + '1034_00' + str(i-2) + '.txt', skip_header=2)
        date = np.append(date, datetime.datetime(2022, 5, 2))
    if i == 6:
        d["data_{0}".format(i)] = np.genfromtxt(filehead + '1035_000.txt', skip_header=2)
        date = np.append(date, datetime.datetime(2022, 5, 11))

# now that the data is imported, loop through each FEB/channel and plot data
timediff = np.zeros(nfiles)
timediff_years = np.zeros(nfiles)
FEB0 = np.zeros(64)
FEB1 = np.zeros(64)
histbins = np.linspace(0.0, 15.0, num=16)
for j in range(128): # 0-63 are FEB 0 and 64-127 are FEB 1
    for i in range(nfiles):
        data = d["data_{0}".format(i)]
        PE_yield[i] = data[j, 3]
        temperature[i] = data[j, 8]
        duration = date[i] - date[0]
        timediff[i] = duration.total_seconds() / 86400 # time after t=0 in days
        timediff_years[i] = duration.total_seconds() / 31536000
        
    linfit_params = np.polyfit(timediff, PE_yield, 1)
    linfit_params_years = np.polyfit(timediff_years, PE_yield, 1)
    slope = round(linfit_params_years[0] / PE_yield[0] * 100, 2)
    print(slope)
    linfit_fnct = np.poly1d(linfit_params)

    if j < 64:
        feb = 0
        channel = j
        FEB0[channel] = -1 * slope
    else:
        feb = 1
        channel = j - 64
        FEB1[channel] = -1 * slope
    
    plt.figure(num=j)
    plt.plot(timediff, PE_yield, 'r.', timediff, linfit_fnct(timediff), '--k')
    plt.text(1, 46, 'PE yield change: {0} %/yr'.format(slope))
    plt.ylim(30,50)
    plt.xlabel('Days after April 27, 2022')
    plt.ylabel('PE yield')
    plt.title('PE yield over short timespan, FEB {0}, channel {1}'.format(feb, channel))
    plt.savefig('smallrun/smallrun_feb{0}_ch{1}.pdf'.format(feb, channel))
    plt.close(fig=j)

    plt.figure(num=129+j)
    plt.plot(temperature[0], PE_yield[0], 'red.')
    plt.plot(temperature[1], PE_yield[1], 'orange.')
    plt.plot(temperature[2], PE_yield[2], 'yellow.')
    plt.plot(temperature[3], PE_yield[3], 'green.')
    plt.plot(temperature[4], PE_yield[4], 'blue.')
    plt.plot(temperature[5], PE_yield[5], 'indigo.')
    plt.plot(temperature[6], PE_yield[6], 'violet.')
    plt.xlim(22,24)
    plt.ylim(30, 50)
    plt.xlabel('Average temp. of CMB [degC]')
    plt.ylabel('Temperature corrected PE yield')
    plt.savefig('smallrun/PEvstemp_feb{0}_ch{1}.pdf'.format(feb, channel))
    plt.close(fig=129+j)

plt.figure(num=128)
hist0 = plt.hist(FEB0, bins=histbins, histtype='step', color='b', label='FEB 0')
hist1 = plt.hist(FEB1, bins=histbins, histtype='step', color='r', label='FEB 1')
plt.legend()
plt.xlabel('% PE yield change over time')
plt.ylabel('Channels / % change')
plt.ylim(bottom=0)
plt.xlim(0, 15)
plt.savefig('percent_histogram_smallrun.pdf')
plt.close(fig=128)

#
