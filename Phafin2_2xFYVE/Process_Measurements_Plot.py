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
from matplotlib import container

sec_per_frame = 5

datapath = os.path.dirname(__file__)
dir_name = os.path.basename(datapath)
print dir_name
print datapath
splits = dir_name.split('_')
print splits[0]
print splits[1]
savepath = datapath + "/Measurements"


Channel_1 = []
Channel_2 = []
files = glob.glob(savepath+"/*.csv")

#files = files[1:29]

print files

f = lambda x: ((x-x.min())/(x.max()-x.min())*100)
f2 = lambda x: (x/x.max()*100)
f3 = lambda x: (x/x.min())
f4 = lambda x: (x-x.min())
f5 = lambda x: (x/x.mean())
f10 = lambda x: x*1

def legend_no_error():
    # remove error bars from legend to look nicer
    ax = plt.gca()
    handles, labels = ax.get_legend_handles_labels()
    handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
    plt.legend(handles, labels, loc="upper right", bbox_to_anchor=[1, 1],
           ncol=2, shadow=True, fancybox=True)
    #end remove error bars



normalisation = f
norm2 = f4
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

print shifting_matrix
#shifting_matrix[:] = [5 - x for x in shifting_matrix]
#print shifting_matrix
headings = range(1, (len(shifting_matrix)+1))
df5.columns = headings
for position, movement in enumerate(shifting_matrix):
    print position 
    print movement
    df5.iloc[:, position] = df5.iloc[:,position].shift(5-movement)
tracklength = df5.count() - df5[:10].idxmax()

#
df6 = df4.copy()
#print df4.head()
#shifting_Matrix = [5,1,9,7,5,4,10,2,1,6,2,9,11,-1,15,21,22,16,3,7]
#shifting_Matrix = [4,11,9,9,10,6,15,]
headings = range(1, (len(shifting_matrix)+1))
df6.columns = headings

for position, movement in enumerate(shifting_matrix):
    print position 
    print movement
    df6.iloc[:, position] = df6.iloc[:,position].shift(5-movement)
#
#
##df12 = df3.apply(f2)
sns.set_style("white",{'xtick.major.size': 5, 'ytick.major.size': 5})
#sns.set_style("whitegrid",{'xtick.major.size': 5, 'ytick.major.size': 5})
#sns.set_style("darkgrid")
sns.set_palette("bright")
plt.style.use("ggplot")
sns.set_context("notebook", font_scale=1.6, rc={"lines.linewidth": 2})
new_index = list(map(lambda x: x*sec_per_frame, df5.index.tolist()))
#sns.despine(top=True, right=True, left=False, bottom=False, offset=None, trim=False)
df5["time"] = new_index
df6["time"] = new_index
df5.set_index(["time"], inplace=True, drop=True)
df6.set_index(["time"], inplace=True, drop=True)


mean_df5 = df5[:40].apply(normalisation).mean(axis=1)
std_df5 =  df5[:40].apply(normalisation).sem(axis=1)
mean_df6 = df6[:40].apply(normalisation).mean(axis=1)
std_df6 =  df5[:40].apply(normalisation).sem(axis=1)

mean_df5.plot(yerr=2*std_df5, label=splits[0], color="green")# C=sns.color_palette()[1]) #c=sns.color_palette()[1])
mean_df6.plot(yerr=2*std_df6, label=splits[1], color="red")#C=sns.color_palette()[2])#c=sns.color_palette()[2])


#plt.legend(loc="upper right", bbox_to_anchor=[1, 1],
#           ncol=2, shadow=True, fancybox=True)
#
#remove_error()
legend_no_error()

sns.despine() # Remove upper and right border
plt.xlabel('time (s)') #x axis 
plt.ylabel('relative fluorescence (normalized)') #y axis
save_plot = datapath + "/Plots/plot1.png"


plt.savefig(save_plot, dpi=600)

plt.figure()
mean_df5 = df5[:40].apply(norm2).mean(axis=1)
std_df5 =  df5[:40].apply(norm2).sem(axis=1)
mean_df6 = df6[:40].apply(norm2).mean(axis=1)
std_df6 =  df5[:40].apply(norm2).sem(axis=1)

mean_df5.plot(yerr=2*std_df5, label=splits[0], color="green")#c=sns.color_palette()[1])
mean_df6.plot(yerr=2*std_df6, label=splits[1], color="red")#c=sns.color_palette()[2])
#plt.legend(loc="upper right", bbox_to_anchor=[1, 1],
#           ncol=2, shadow=True, fancybox=True)
#remove_error()
legend_no_error()

sns.despine()
plt.xlabel('time (s)')
plt.ylabel('relative fluorescence (raw)')
save_plot = datapath + "/Plots/plot4.png"


plt.savefig(save_plot, dpi=600)




df5[:40].apply(normalisation).plot(legend = False, color="green")#c=sns.color_palette()[1])
save_plot = datapath + "/Plots/plot2.png"
plt.savefig(save_plot)
df6[:40].apply(normalisation).plot(legend = False, color="red")#c=sns.color_palette()[2])
save_plot = datapath + "/Plots/plot3.png"
plt.savefig(save_plot)

print "Analysed tracks: " + str(len(df6.columns))

save_excel = datapath +"/excel/" + splits[0]+ ".xls"
print save_excel
df5[:40].apply(normalisation).to_excel(save_excel)
save_excel = datapath +"/excel/" + splits[1]+ ".xls"
print save_excel
df6[:40].apply(normalisation).to_excel(save_excel)
save_excel = datapath +"/excel/tracklength.xls"
tracklength.to_frame().to_excel(save_excel)

