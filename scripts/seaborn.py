#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 15:48:07 2022

@author: sqyang
"""

#### radar

import numpy as np
import matplotlib.pyplot as plt


#plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.unicode_minus'] = False
plt.style.use('ggplot')

## empirical data
#values = [9.7, 5.3, 2.8, -2.4, -3.6, -3.5, -5.9]  #IGE p1
#values = [4.8, 4.1, 3.6, -1.3, -0.9, -2.4, -4.9]  #TLE p1
#values = [-5.4, 2.2, 0.8, 9.8, 3.4, 0.7, -1.0]  #IGE p2
#values = [-2.4, 3.2, 1.1, 4.6, 0.3, -0.6, -4.2]  #TLE p2

## simulated data
#values = [12.9, 13.8, 6.8, -3.9, -14.0, -1.9, -12.1]  #IGE p1
values = [10.1, 12.5, 5.7, -3.0, -11.4, -2.1, -8.8]  #TLE p1

feature = ['VN', 'SMN', 'DAN', 'SN', 'LN', 'FPN', 'DMN']

N = len(values)
angles=np.linspace(0, 2*np.pi, N, endpoint=False)
values=np.concatenate((values,[values[0]]))
angles=np.concatenate((angles,[angles[0]]))

fig=plt.figure()
ax = fig.add_subplot(111, polar=True)
ax.plot(angles, values, 'o-', linewidth=2)
ax.fill(angles, values, alpha=0.25)

ax.set_thetagrids(angles * 180/np.pi, feature)
ax.set_ylim(-14,14)
plt.title('RSN')
ax.grid(True)
plt.show()

#fig.savefig('/home/sqyang/storage/UESTC/figures/hctsa/TLE_RSN_p2.svg', format='svg')
fig.savefig('/home/sqyang/storage/UESTC/figures/hctsa/simu_TLE_RSN_p1.svg', format='svg')



##### correlation 
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
sns.set_theme()

# Load the penguins dataset

data = pd.read_csv('/home/sqyang/Jobbing/MFM/figures/Schaeer200/multi-level.csv')

# Plot sepal width as a function of sepal_length across days
g = (sns.jointplot(x='TLE_hctsa',y='TLE_RC',data=data, kind ="kde",cmap='GnBu',fill=True, n_levels=27)).plot_joint(sns.regplot,marker='None',line_kws={"color":"m",'linewidth':3.7})
g.savefig('/home/sqyang/Jobbing/MFM/figures/Schaeer200/TLE-corr.svg', format="svg")


g = (sns.jointplot(x='IGE_hctsa',y='IGE_RC',data=data, kind ="kde",cmap='PuBu',fill=True, n_levels=27)).plot_joint(sns.regplot,marker='None',line_kws={"color":"b",'linewidth':3.7})
g.savefig('/home/sqyang/Jobbing/MFM/figures/Schaeer200/IGE-corr.svg', format="svg")









