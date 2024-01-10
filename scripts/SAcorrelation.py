#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Refer to BrainSMASH: https://brainsmash.readthedocs.io/en/latest/index.html

This script was used to test the p-value after spatial autocorrelation correction.

Left and right hemispheres were tested separately.

"""

## calculate the centroid point
from brainsmash.workbench.geo import cortex
surface = "/home/sqyang/templates/lh.midthickness.surf.gii"
cortex(surface=surface, outfile="/home/sqyang/geodesic/LeftDenseGeodesicDistmat.txt", euclid=False)


from brainsmash.workbench.geo import parcellate
infile = "/home/sqyang/geodesic/LeftDenseGeodesicDistmat.txt"
outfile = "/home/sqyang/geodesic/LeftParcelGeodesicDistmat.txt"
dlabel = "/home/sqyang/templates/lh.aparc.dlabel.nii"
parcellate(infile, dlabel, outfile)





##  generated the 1000 surrogate maps
from brainsmash.mapgen.base import Base
import numpy as np

hctsa = np.loadtxt("/home/sqyang/hctsa/data/HCGTCS_p1_t_global.txt")  
MFM_RC = np.loadtxt("/home/sqyang/MFM/data/dif_GTCS_RC.txt")

lh_hctsa = hctsa[0:34]
rh_hctsa = hctsa[34:68]
lh_RC = MFM_RC[0:34]
rh_RC = MFM_RC[34:68]


lh_distance = np.loadtxt("/home/sqyang/geodesic/LeftParcelGeodesicDistmat.txt")
rh_distance = np.loadtxt("/home/sqyang/geodesic/RightParcelGeodesicDistmat.txt")

###### change the measurements to assess
sourcemap = lh_hctsa  
distmap = lh_distance
targetmap = lh_RC

sourcemap = rh_hctsa  
distmap = rh_distance
targetmap = rh_RC

base = Base(sourcemap, distmap)
surrogates = base(n=1000)


####  Compute the Pearson correlation between each surrogate hctsa map and the MFM index
from brainsmash.mapgen.stats import pearsonr, pairwise_r

surrogate_brainmap_corrs = pearsonr(targetmap,surrogates).flatten()
surrogate_pairwise_corrs = pairwise_r(surrogates,flatten=True)

#### Repeat using randomly shuffled surrogate hctsa maps
naive_surrogates = np.array([np.random.permutation(sourcemap) for _ in range(1000)])
naive_brainmap_corrs = pearsonr(targetmap,naive_surrogates).flatten()
naive_pairwise_corrs = pairwise_r(naive_surrogates,flatten=True)


##  Compute non-parametric p-values using two different null distributions
from brainsmash.mapgen.stats import nonparp
from scipy import stats

test_stat = stats.pearsonr(sourcemap,targetmap)[0]
print("Spatial naive p-value:",nonparp(test_stat,naive_brainmap_corrs))
print("SpatialAutocorrelation-correlated p-value:",nonparp(test_stat,surrogate_brainmap_corrs))




#### Plot the results
import matplotlib.pyplot as plt
from scipy import stats

sac = '#386cb0'  # sutocorr-preserving (blue for EI)
sac = '#5e3c99'   # purple for RC
rc = '#e66101'  # randomly shuffled
bins = np.linspace(-1,1,51) #correlation b

# this is the empirical statistic creating a null distribution for
test_stat = stats.pearsonr(sourcemap,targetmap)[0]

fig = plt.figure(figsize=[5,5])
ax = fig.add_axes([0.2,0.25,0.6,0.6])  # autocorr preserving
ax2 = ax.twinx() # randomly shuffled

# plot the data
ax.axvline(test_stat,0,0.8,color='k',linestyle='dashed',lw=1)
ax.hist(surrogate_brainmap_corrs,bins=bins,color=sac,alpha=1,density=True,clip_on=False,zorder=1)
ax2.hist(naive_brainmap_corrs,bins=bins,color=rc,alpha=0.7,density=True,clip_on=False,zorder=2)

# make the plot nice...
ax.set_xticks(np.arange(-1,1.1,0.5))
ax.spines['left'].set_color(sac)
ax.tick_params(axis='y',colors=sac)
ax2.spines['right'].set_color(rc)
ax2.tick_params(axis='y',colors=rc)
ax.set_ylim(0,1.6)
ax2.set_ylim(0,3)
ax.set_xlim(-1,1)
[s.set_visible(False) for s in [ax.spines['top'],ax.spines['right'],\
                                    ax2.spines['top'],ax2.spines['left']]]
ax.text(0.97,1.1,'SA-independent',ha='right',va='bottom',color=rc,transform=ax.transAxes)    
ax.text(0.97,1.03,'SA-preserving',ha='right',va='bottom',color=sac,transform=ax.transAxes) 
ax.text(test_stat,1.65,'hctsa',ha='center',va='bottom')
ax.text(0.5,-0.2,"Pearson correlation\nwith RC",ha='center',va='top',transform=ax.transAxes)
ax.text(-0.3,0.5,"Density",rotation=90,ha='left',va='center',transform=ax.transAxes)

plt.savefig('/home/sqyang/figures/corr/lh.p1_RC_GTCS.svg', format="svg")
plt.show()



