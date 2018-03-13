import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from scipy import optimize
sns.set_style('white')
sns.set_context('paper', font_scale=1.5)
from glob import glob
from figtools import *
from fusco import SFS


pi = np.pi
mu = 0.02
alpha = 30
fusco_alpha = 0.55
fusco_beta = 2.3

mappings = [ '../model/experiments/u0.01/0_0_0_outs*']
colors_ = ['gray']
labels_ = ['Simulation']

fig = plt.figure()

ax = fig.add_subplot('111')
freq_plot(ax,
          mappings,
          colors_=colors_,
          labels_=labels_,
          neutral=True,
          noS=True,
          calculate_slopes=True,
          slope_start=-2)


sfs, x_c_prime = SFS(10**8, mu, fusco_alpha, fusco_beta, with_correction=False)

sfs = np.vectorize(sfs)
fusco_support = np.logspace(-4.1, np.log10(x_c_prime), num=1000, endpoint=False)
ax.plot(np.log10(fusco_support), np.log10(sfs(2*fusco_support)), ':b', label='Fusco et al. (Without Correction)')
fusco_support = np.logspace(np.log10(x_c_prime)+np.finfo(float).eps, 0, num=1000, endpoint=False)
ax.plot(np.log10(fusco_support), np.log10(sfs(2*fusco_support)), ':b')


fusco_support = np.logspace(-4.1, 0, num=1000)
sfs, x_c_prime = SFS(10**8, mu, fusco_alpha, fusco_beta)
sfs = np.vectorize(sfs)
ax.plot(np.log10(fusco_support), np.log10(sfs(2*fusco_support)), '--r', label='Fusco et al. (With Correction)')

freq_support = np.logspace(-2.05,0, num=1000)
ax.plot(np.log10(freq_support), np.log10((alpha*mu/(4*np.sqrt(np.pi)))*freq_support**(-2.5)), '-', label='Deterministic Result')

ax.set_xlabel('$log_{10}(f)$')
ax.set_ylabel('$log_{10}(p(f))$')
sns.despine()

ax.legend(loc='upper right')
# fig.tight_layout()
fig.savefig('./Analytic.pdf')

