import csv

import pandas as pd
from pandas.tools.plotting import andrews_curves

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib

directory="../TrafficData/"
junctionBFile = directory+'4112_reworked.csv'
timesFile = directory+'traveltimes_avghourly_2016-05-12_v2.csv'

print "hello Zwolle"

junctionDF = pd.read_csv(junctionBFile)

print junctionDF

dirtyTimes = pd.read_csv(timesFile)

print dirtyTimes
print dirtyTimes['AC']

distances = pd.read_csv(directory+'VID-Junction-dist_reformatted.csv')

print distances
print distances['AC'][0]

parts = junctionDF.keys().delete(0);

colors = cm.rainbow(np.linspace(0, 1, len(parts)))
plt.figure()
for key, c in zip(parts, colors):
    x = distances[key][0]/dirtyTimes[key]
    print x
    y = junctionDF[key]
    plt.scatter(x, y, color = c)
    xm = np.ma.masked_array(x,mask=np.isnan(x)).compressed()
    ym = np.ma.masked_array(y,mask=np.isnan(x)).compressed()
    m,b = np.polyfit(xm, ym, 1)
    plt.plot(x, m*x+b, label=key, color = c)
plt.ylabel('intensity')
plt.xlabel('speed')
plt.legend(loc='best')
plt.show()

def plotIntensityVsTime():
    plt.figure()
    for key in parts:
        plt.plot(junctionDF[junctionDF.keys()[0]], junctionDF[key])
    plt.ylabel('intensity')
    plt.xlabel('time')
    plt.show()

#for key in parts:
#    junctionDF[key] = zip(junctionDF[key], dirtyTimes[key])

#print junctionDF

#plt.figure()
#plt.scatter(zip*(junctionDF['AC']))
#plt.show()
#andrews_curves(junctionDF, 'AC')


