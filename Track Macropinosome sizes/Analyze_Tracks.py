# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 22:55:45 2019

@author: kaysch
"""

from __future__ import print_function
from __future__ import division
from pandas import *
import pandas as pd
from math import *
import matplotlib.pyplot as plt
import numpy
import glob
import random
import seaborn as sns
import matplotlib.ticker as ticker
import os
plt.rcParams["figure.figsize"] = (8,6)





datapath = "D:/Kay/Dropbox/Phafin2/Phafin2_Phenotypes/Size_Tracking/"

dirnames = ["WT","KO"]


palette3 = ["Magenta", "Cyan"]

# gather all files in the directroy "savepath"
#files1 = glob.glob(datapath1+"/*.csv") 

results = []


def percentage(dataframe, columnname, value):
    percent = 100/dataframe[columnname].count()*dataframe[dataframe[columnname]>value].count()
    return percent

for dirnum,directory in enumerate(dirnames):
    datapath1 = datapath+"/"+directory
    files1 = glob.glob(datapath1+"/*.csv") 
    print(files1) ## these files will be processed
    for filenum, csvfile in enumerate(files1):
        filename_w_ext = os.path.basename(csvfile)
        df = pd.read_csv(csvfile, sep= ",",  decimal='.')
        df["Genotype"] = directory
        df["File"] = str(filenum)
        df["Filename"]=  str(filename_w_ext)
              
        df2 = df.sort_values(by=['Track', 'Time'])
        
        df2 = df2.reset_index(drop=True)
        print("Processing file " + str(filenum))

        for i in range(0, df2["Track"].max()):
            current_track = df2[df2["Track"]==i].sort_values(by="Time").copy()
            if current_track["Time"].iloc[0] == 0:
                pass
            else:
                mean_size = current_track[:5]["Area"].mean()
                current_track["Mean Area"] = mean_size
                mean_radius = current_track[:5]["Radius"].mean()
                current_track["Mean Radius"] = mean_radius
                results.append(current_track[:1])

    
df3 = pd.concat(results)
df_wt=df3[df3["Genotype"]=="WT"]
df_ko=df3[df3["Genotype"]=="KO"]
df_max = df3.groupby(["Genotype","File"]).max().reset_index()
df_mean = df3.groupby(["Genotype","File"]).mean().reset_index()
df3["Area_log"]=np.log2(df3["Area"])
small = df3[df3["Radius"]<5]
df4 = small.groupby(["Genotype", "File"]).count().reset_index()

medium = df3[(df3["Radius"]>5) & (df3["Radius"]<15)]
df5 = medium.groupby(["Genotype", "File"]).count().reset_index()

large = df3[df3["Radius"]>15]
df6 = large.groupby(["Genotype", "File"]).count().reset_index()

large = df3[df3["Area"]>100]
df6 = large.groupby(["Genotype", "File"]).mean().reset_index().copy()
df6["Experiment"] = df6["Experiment"].astype(int)

large["Area"]=large["Area"]*(0.08*0.08)
df6["Area"]=df6["Area"]*(0.08*0.08)




sns.set(context="notebook", style="white", font_scale=1.5)
sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})

mean_per_exp = df6.groupby(["Genotype","Experiment"]).mean().reset_index()


ax =sns.stripplot(x="Genotype", y="Area", data=df6, hue="Experiment",size=8, order=["WT", "KO"], zorder=2)
ax =sns.pointplot(x="Genotype", y="Area", data=mean_per_exp,join=False, order=["WT", "KO"], ci=95, color="Black", markers="_", capsize=0.1, errwidth=3,zorder=1)

mean = df6.groupby('Genotype', sort=False)["Area"].mean()

std = df6.groupby('Genotype', sort=False)["Area"].std() / np.sqrt(df6.groupby('Genotype',sort=False)["Area"].count())

sns.despine()
#plt.errorbar(range(len(mean)), mean, yerr=std, fmt="_", capsize=10, color='k')

median_width = 0.4
"""

median_val = df1.groupby('Proteins', sort=False)["Phafin2 in pellet"].mean()
for count, tick in enumerate(ax.get_xticks()):
    ax.plot([tick-median_width/3, tick+median_width/3], [median_val[count], median_val[count]],
            lw=2, color='k')

plt.show()

plt.show()
"""

mean = df6.groupby('Genotype', sort=False)["Area"].mean()

for tick, text in zip(ax.get_xticks(), ax.get_xticklabels()):
    sample_name = text.get_text()  # "X" or "Y"

    # calculate the median value for all replicates of either X or Y
    median_val = df6[df6['Genotype']==sample_name]["Area"].mean()

    # plot horizontal lines across the column, centered on the tick
    ax.plot([tick-median_width/3, tick+median_width/3], [median_val, median_val],
            lw=4, color='darkgrey')


ax.legend_.remove()
ax.set(xticklabels=["WT \n siCTRL","WT \n siFLNA", "KO \n siCTRL","KO \n siFLNA"])
plt.xlabel("")

plt.ylabel("Mean macropinosome size ($um^2$) \n per cell")
plt.tight_layout()


plt.savefig(datapath+"/SizeTracking_perCell.svg")
plt.show()

# All macropinosomes
ax =sns.stripplot(x="Genotype", y="Area", data=large, hue="Experiment", order=["WT", "KO"])
ax =sns.pointplot(x="Genotype", y="Area", data=large,join=False, order=["WT", "KO"], ci=95, color="Black", markers="_", capsize=0.1, errwidth=2)
sns.despine()
plt.ylabel("Macropinosome size ($um^2$) \n (individual macropinosomes)")
plt.tight_layout()
plt.savefig(datapath+"/Macropinosome_sizes.svg")
plt.show()


sns.set(context="notebook", style="white", font_scale=1.5)
sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})

# plotting nicely next to each other


mean_per_exp = df6.groupby(["Genotype","Experiment"]).mean().reset_index()


fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax1 =sns.stripplot(x="Genotype", y="Area", data=df6, hue="Experiment",size=8, order=["WT", "KO"], zorder=2, ax=ax1)
ax1 =sns.pointplot(x="Genotype", y="Area", data=mean_per_exp,join=False, order=["WT", "KO"], ci=95, color="Black", markers="_", capsize=0.1, errwidth=3,zorder=1, ax=ax1)

mean = df6.groupby('Genotype', sort=False)["Area"].mean()

std = df6.groupby('Genotype', sort=False)["Area"].std() / np.sqrt(df6.groupby('Genotype',sort=False)["Area"].count())

#plt.errorbar(range(len(mean)), mean, yerr=std, fmt="_", capsize=10, color='k')

median_width1 = 1
median_width = 0.4


for tick, text in zip(ax1.get_xticks(), ax1.get_xticklabels()):
    sample_name = text.get_text()  # "X" or "Y"

    # calculate the median value for all replicates of either X or Y
    median_val = mean_per_exp[mean_per_exp['Genotype']==sample_name]["Area"].mean()

    # plot horizontal lines across the column, centered on the tick
    ax1.plot([tick-median_width/3, tick+median_width/3], [median_val, median_val],
            lw=4, color='darkgrey', zorder=99)
    ax1.plot([tick-median_width1/3, tick+median_width1/3], [median_val, median_val],
            lw=4, color='white', zorder=1)




ax1.set_ylabel("Mean macropinosome size ($um^2$) \n per cell")
ax1.set_xlabel("")

plt.plot()

mean_per_exp_large = df6.groupby(["Genotype","Experiment"]).mean().reset_index()




g =sns.stripplot(x="Genotype", y="Area", data=large, hue="Experiment", order=["WT", "KO"],size=8, ax=ax2, zorder=2)
g =sns.pointplot(x="Genotype", y="Area", data=mean_per_exp_large,join=False, order=["WT", "KO"], ci=95, color="Black", markers="_", capsize=0.1, errwidth=2, ax=ax2,zorder=100)


for tick, text in zip(ax1.get_xticks(), ax1.get_xticklabels()):
    sample_name = text.get_text()  # "X" or "Y"

    # calculate the median value for all replicates of either X or Y
    median_val = mean_per_exp_large[mean_per_exp_large['Genotype']==sample_name]["Area"].mean()

    # plot horizontal lines across the column, centered on the tick
    ax2.plot([tick-median_width/3, tick+median_width/3], [median_val, median_val],
            lw=4, color='darkgrey', zorder=99)
    ax2.plot([tick-median_width1/3, tick+median_width1/3], [median_val, median_val],
            lw=4, color='white', zorder=1)
    

ax2.set_ylabel("Macropinosome size ($um^2$) \n (individual macropinosomes)")
ax2.set_xlabel("")
plt.tight_layout()
sns.despine()


plt.savefig(datapath+"/Macropinosome_size_dualPlot.svg")
plt.show()

