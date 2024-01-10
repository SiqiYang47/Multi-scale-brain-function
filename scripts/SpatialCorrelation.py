#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is used to plot the Fig.5a

@author: sqyang
"""

##### correlation 
import seaborn as sns
import pandas as pd
sns.set_theme()

# Load the penguins dataset

data = pd.read_csv('/home/sqyang/data/data.csv')

# Plot sepal width as a function of sepal_length across days
g = (sns.jointplot(x='TLE_hctsa',y='TLE_RC',data=data, kind ="kde",cmap='GnBu',fill=True, n_levels=27)).plot_joint(sns.regplot,marker='None',line_kws={"color":"m",'linewidth':3.7})
g.savefig('/home/sqyang/figures/TLE-corr.svg', format="svg")


g = (sns.jointplot(x='GTCS_hctsa',y='GTCS_RC',data=data, kind ="kde",cmap='PuBu',fill=True, n_levels=27)).plot_joint(sns.regplot,marker='None',line_kws={"color":"b",'linewidth':3.7})
g.savefig('/home/sqyang/figures/IGE-corr.svg', format="svg")









