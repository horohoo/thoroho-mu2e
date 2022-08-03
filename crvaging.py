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

nfiles = 36
badfiles = 14
d = {}
filehead = '/pnfs/mu2e/scratch/users/thoroho/recotar/crvreco/rec.mu2e.CRV_wideband_cosmics.crvaging-001.00'
# import the data
date = np.array([])
for i in range(nfiles):
    # hard-coded information about dates of runs
    if i == 0:
        d["data_{0}".format(i)] = np.genfromtxt(filehead + '0066_00' + str(i) + '.txt', skip_header=2)
        date = np.append(date, datetime.datetime(2021, 7, 8))
        #date[i] = datetime.datetime(2021, 7, 8)
    if i >= 1 and i <= 12:
        if i >= 1 and i <= 10:
            d["data_{0}".format(i)] = np.genfromtxt(filehead + '0094_00' + str(i-1) + '.txt', skip_header=2)
        if i >= 11 and i <= 12:
            d["data_{0}".format(i)] = np.genfromtxt(filehead + '0094_0' + str(i-1) + '.txt', skip_header=2)
        date = np.append(date, datetime.datetime(2021, 12, 10))
        #date[i] = datetime.datetime(2021, 12, 10)
    if i >= 13 and i <= 22:
        d["data_{0}".format(i)] = np.genfromtxt(filehead + '0105_00' + str(i-13) + '.txt', skip_header=2)
        date = np.append(date, datetime.datetime(2022, 1, 12))
        #date[i] = datetime.datetime(2022, 1, 12)
    if i == 23:
        d["data_{0}".format(i)] = np.genfromtxt(filehead + '0119_000.txt', skip_header=2)
        date = np.append(date, datetime.datetime(2022, 2, 15))
        #date[i] = datetime.datetime(2022, 2, 15)
    if i == 24:
        d["data_{0}".format(i)] = np.genfromtxt(filehead + '1010_000.txt', skip_header=2)
        date = np.append(date, datetime.datetime(2022, 2, 25))
        #date[i] = datetime.datetime(2022, 2, 25)
    if i == 25:
        d["data_{0}".format(i)] = np.genfromtxt(filehead + '1020_000.txt', skip_header=2)
        date = np.append(date, datetime.datetime(2022, 3, 7))
        #date[i] = datetime.datetime(2022, 3, 7)
    if i == 26:
        d["data_{0}".format(i)] = np.genfromtxt(filehead + '1021_000.txt', skip_header=2)
        date = np.append(date, datetime.datetime(2022, 3, 10))
        #date[i] = datetime.datetime(2022, 3, 10)
    if i >= 27 and i <= 28:
        d["data_{0}".format(i)] = np.genfromtxt(filehead + '1022_00' + str(i-27) + '.txt', skip_header=2)
        date = np.append(date, datetime.datetime(2022, 3, 18))
        #date[i] = datetime.datetime(2022, 3, 18)
    if i == 29:
        d["data_{0}".format(i)] = np.genfromtxt(filehead + '1031_000.txt', skip_header=2)
        date = np.append(date, datetime.datetime(2022, 4, 27))
        #date[i] = datetime.datetime(2022, 4, 27)
    if i == 30:
        d["data_{0}".format(i)] = np.genfromtxt(filehead + '1033_000.txt', skip_header=2)
        date = np.append(date, datetime.datetime(2022, 4, 29))
        #date[i] = datetime.datetime(2022, 4, 29)
    if i >= 31 and i <= 34:
        d["data_{0}".format(i)] = np.genfromtxt(filehead + '1034_00' + str(i-31) + '.txt', skip_header=2)
        date = np.append(date, datetime.datetime(2022, 5, 2))
        #date[i] = datetime.datetime(2022, 5, 2)
    if i == 35:
        d["data_{0}".format(i)] = np.genfromtxt(filehead + '1035_000.txt', skip_header=2)
        date = np.append(date, datetime.datetime(2022, 5, 11))
        #date[i] = datetime.datetime(2022, 5, 11)

# now that the data is imported, loop through each FEB/channel and plot data
FEB0_raw = np.zeros(64)
FEB1_raw = np.zeros(64)
histbins = np.linspace(0.0, 15.0, num=16)

for j in range(128): # 0-63 are FEB 0 and 64-127 are FEB 1
    if j < 64:
        feb = 0
        channel = j

        timediff = np.zeros(nfiles)
        PE_yield = np.zeros(nfiles)
        
        for i in range(nfiles):
            data = d["data_{0}".format(i)]
            PE_yield[i] = data[j, 3]
            duration = date[i] - date[0]
            timediff[i] = duration.total_seconds() / 31536000
    else:
        feb = 1
        channel = j - 64

        timediff = np.zeros(nfiles - badfiles)
        PE_yield = np.zeros(nfiles - badfiles)
        
        for i in range(nfiles):
            if i < 9:
                data = d["data_{0}".format(i)]
                PE_yield[i] = data[j, 3]
                duration = date[i] - date[0]
                timediff[i] = duration.total_seconds() / 31536000                
            elif i > 22:
                data = d["data_{0}".format(i)]
                PE_yield[i - badfiles] = data[j, 3]
                duration = date[i] - date[0]
                timediff[i - badfiles] = duration.total_seconds() / 31536000
        
    linfit_params = np.polyfit(timediff, PE_yield, 1)
    slope = round(linfit_params[0] / PE_yield[0] * 100, 2)
    linfit_fnct = np.poly1d(linfit_params)

    if j < 64:
        FEB0_raw[channel] = -1 * slope
    else:
        FEB1_raw[channel] = -1 * slope
    print('Finished FEB {0} channel {1} ...'.format(feb, channel))
    
    plt.figure(num=j)
    plt.plot(timediff, PE_yield, 'r.', timediff, linfit_fnct(timediff), '--k')
    plt.text(0.4, 46, 'PE yield change: {0} %/yr'.format(slope))
    plt.ylim(30,50)
    plt.xlabel('Years since July 8, 2021')
    plt.ylabel('PE yield')
    plt.title('PE yield over time for FEB {0}, channel {1}'.format(feb, channel))
    plt.savefig('aging/aging_feb{0}_ch{1}.pdf'.format(feb, channel))
    plt.close(fig=j)

#channels to exclude
rm_FEB0 = [28, 29, 30, 31, 56, 57, 58, 59, 60, 61, 62, 63]
rm_FEB1 = [18]

FEB0 = np.delete(FEB0_raw, rm_FEB0)
FEB1 = np.delete(FEB1_raw, rm_FEB1)

mean0 = round(np.mean(FEB0), 2)
mean1 = round(np.mean(FEB1), 2)

plt.figure(num=128)
hist0 = plt.hist(FEB0, bins=histbins, histtype='step', color='b', label='FEB 0 ({0} %)'.format(mean0))
hist1 = plt.hist(FEB1, bins=histbins, histtype='step', color='r', label='FEB 1 ({0} %)'.format(mean1))
plt.legend()
plt.xlabel('% PE yield change over time')
plt.ylabel('Channels / % change')
plt.ylim(bottom=0)
plt.savefig('percent_histogram.pdf')
plt.close(fig=128)
#
