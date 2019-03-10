import numpy as np
import matplotlib as mpl
from matplotlib import rc
import scipy.io as sio
import pdb
mpl.use("pgf")
import matplotlib.pyplot as plt
import pandas
import sys

pgf_with_custom_preamble = {
    "pgf.texsystem": "xelatex",
    "font.family": "sans-serif", # use san serif/main font for text elements
    "text.usetex": False,    # use inline math for ticks
    "pgf.rcfonts": False,   
    "font.size": 10,
    "pgf.preamble": [
        r"\usepackage{amsmath}",
        r"\usepackage{fontspec}",
        r"\setmainfont{Avenir Next}",
        r"\setsansfont{Avenir Next}",
    ]
}
mpl.rcParams.update(pgf_with_custom_preamble)

#define colors http://paletton.com/#uid=73B1q0kleqtbzEKgVuIpcmGtdhZ
colors = []
colors.append('#204976')
colors.append('#B85C7F')
colors.append('#94C160')
colors.append('#933157')
colors.append('#6B9A33')
colors.append('#6E1236')
colors.append('#477413')
colors.append('#49001C')
colors.append('#294D00')

colors_err = []
'''
colors_err.append('#5277A0')
colors_err.append('#4F162C')
colors_err.append('#375317')
colors_err.append('#5C253A')
colors_err.append('#466127')
colors_err.append('#623949')
colors_err.append('#53673B')
colors_err.append('#825265')
colors_err.append('#718956')
'''
colors_err.append('#5277A0')
colors_err.append('#4F162C')
colors_err.append('#375317')
colors_err.append('#5C253A')
colors_err.append('#466127')
colors_err.append('#825265')
colors_err.append('#718956')
colors_err.append('#825265')
colors_err.append('#718956')

exp_data = sio.loadmat('net_work_data_new.mat')

fig = plt.figure()
ax = fig.add_subplot(111)

n_cond = 9
n_sub = 5
width = 1
spacing = 1.2
pos = []
pos.append(spacing*np.arange(n_cond))
pos[0][0] -= 0.5 
for i in range(1,n_sub):
    pos.append(pos[i-1] + n_cond + 5)

bar_plots = []
for sub in range(n_sub):
    b = ax.bar(pos[sub], exp_data['bar_data'][sub,:], 
        yerr = exp_data['bar_err_data'][sub,:], width = width, 
        color = colors, ecolor = colors_err)
    bar_plots.append(b)

ax.set_xticks([np.mean(p) for p in pos])
ax.set_xticklabels(["1/5", "2/9", "3/3", "4/6", "5/6"])

ax.set_ylabel('Ankle Net Work (J/kg)')
ax.set_xlabel('Subject/Parameter Number')

#turn off spines except left
ax.spines['bottom'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.set_ylim(-0.07, 0.2)
ax.spines['left'].set_bounds(-0.05, 0.15)
ax.set_yticks(np.arange(-0.05, 0.2, 0.05))

ax.tick_params('x', which='both',length=0)
ax.tick_params('y', which='both',direction='out')

#add significane test resutls
for sub in range(n_sub):
    for comp in np.arange(1,5):
        if exp_data['t_test_results'][sub, comp]:
            xloc1 = pos[sub][2*comp-1]
            xloc2 = pos[sub][2*comp]
            yloc = np.max(exp_data['bar_data'][sub,(2*comp-1):(2*comp+1)]) +\
                0.01

            ax.annotate("", xy=(xloc1, yloc), xycoords='data',
                       xytext=(xloc2, yloc), textcoords='data',
                       arrowprops=dict(arrowstyle="-", ec='#696969',
                                       connectionstyle="bar,fraction=0.6",
                                       linewidth=1.5))
            ax.text(0.5*(xloc1 + xloc2), yloc+0.005, '*', 
                horizontalalignment='center', verticalalignment='center', 
                color = '#696969', fontsize=12)

inv_data = ax.transData.inverted()
inv_axes = ax.transAxes.inverted()

ylabelpos_axes = ax.yaxis.get_label().get_position()
ylabelpos_display = ax.transAxes.transform(ylabelpos_axes)
ylabelpos_data = inv_data.transform(ylabelpos_display)
ylabelpos_data[1] = np.array(ax.spines['left'].get_bounds()).mean()
ylabelpos_display = ax.transData.transform(ylabelpos_data)
ylabelpos_axes = inv_axes.transform(ylabelpos_display)
ax.yaxis.get_label().set_position(ylabelpos_axes)

fig.savefig('net_work_fig_new.pdf', bbox_inches='tight')
