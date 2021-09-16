# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 13:42:59 2015

@author: kaysch
"""

from __future__ import division
from pandas import *
import pandas as pd
from math import *
import matplotlib.pyplot as plt
import numpy
import glob
import os
import seaborn as sns

import numpy as np
def ci_func(a, which=95, axis=None):
    """Return a percentile range from an array of values."""
    p = 50 - which / 2, 50 + which / 2
    return np.nanpercentile(a, p, axis)

sns.relational.ci_func = ci_func



sns.set(context="notebook", style="white", font_scale=1.5)
sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})

time_max = 40

datapath = os.path.dirname(__file__)
dir_name = os.path.basename(datapath)
print(dir_name)
print(datapath)
splits = dir_name.split('_')
print(splits[0])
print(splits[1])
savepath = datapath + "/Measurements"

Channel_1 = []
Channel_2 = []
files = glob.glob(savepath+"/*.csv")

#files = files[1:29]

print(files)

f = lambda x: ((x-x.min())/(x.max()-x.min())*100)
f2 = lambda x: (x/x.max()*100)
f3 = lambda x: (x/x.min())
f4 = lambda x: (x-x.min())
f5 = lambda x: (x/x.mean())

normalisation = f

for csvfiles in files:
    df = pd.read_csv(csvfiles, sep=',', decimal='.', index_col=0)
    df_Channel1= df["Channel 1"]
    df_Channel2 = df["Channel 2"]
    #df11 = df2.apply(f2)
 #   df1["Norm"] = df1["Mean_Intensity"] - df1["Center_Intensity_Channel1"]
#    df1["Norm2"] = df11["Mean_Intensity_Perimeter"]
#    df1["Norm3"] = df11["Center_Intensity_Channel1"]
#        
    #print df1["Mean_Intensity"]    
    Channel_1.append(df_Channel1)
    Channel_2.append(df_Channel2)
    
    #list2.append(df11)

df3 = pd.concat(Channel_1, axis=1)
df4 = pd.concat(Channel_2, axis=1)

df5 = df3.copy()

#print df4.head()
#shifting_Matrix = [5,1,9,7,5,4,10,2,1,6,2,9,11,-1,15,21,22,16,3,7]
#shifting_Matrix = [4,11,9,9,10,6,15,]
shifting_matrix = df5[:15].idxmax().tolist()
print(shifting_matrix)
#shifting_matrix[:] = [5 - x for x in shifting_matrix]
#print shifting_matrix
headings = range(1, (len(shifting_matrix)+1))
df5.columns = headings
for position, movement in enumerate(shifting_matrix):
    print(position)
    print(movement)
    df5.iloc[:, position] = df5.iloc[:,position].shift(5-movement)
#
df6 = df4.copy()
#print df4.head()
#shifting_Matrix = [5,1,9,7,5,4,10,2,1,6,2,9,11,-1,15,21,22,16,3,7]
#shifting_Matrix = [4,11,9,9,10,6,15,]
headings = range(1, (len(shifting_matrix)+1))
df6.columns = headings

for position, movement in enumerate(shifting_matrix):
    print(position) 
    print(movement)
    df6.iloc[:, position] = df6.iloc[:,position].shift(5-movement)
#
#
##df12 = df3.apply(f2)
df5= df5[:time_max]
df6 = df6[:time_max]


df5= df5[:time_max].apply(normalisation)
df6 = df6[:time_max].apply(normalisation)
df5.reset_index(inplace=True, drop=True)

# converting to tidy dataframe
pal=["Green", "Red"]
df5_tidy = pd.melt(df5.reset_index(), id_vars='index', var_name="Track", value_name="Intensity" )
df5_tidy.rename(columns={"index": "time"}, inplace=True)
df5_tidy["Protein"]=splits[0]
df5_tidy["time (s)"] = df5_tidy["time"]*5
df6.reset_index(inplace=True, drop=True)
df6_tidy = pd.melt(df6.reset_index(), id_vars='index', var_name="Track", value_name="Intensity" )
df6_tidy.rename(columns={"index": "time"}, inplace=True)
df6_tidy["Protein"]=splits[1]
df6_tidy["time (s)"] = df6_tidy["time"]*5
df_combined = pd.concat([df5_tidy, df6_tidy], axis=0)
fig, ax = plt.subplots()

g = sns.lineplot(x="time (s)", y="Intensity", data= df_combined, hue="Protein", palette=pal, ci=95)
sns.despine()


handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles[1:], labels=labels[1:], frameon=False)


plt.xlim(0,200)
plt.ylim(0,105)
savename=datapath+"/plots/"+dir_name+"_plot.svg"
plt.ylabel("Normalized intensity")
plt.tight_layout()
plt.savefig(savename)
plt.show()