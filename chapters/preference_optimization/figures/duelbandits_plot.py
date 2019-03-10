import numpy as np
import matplotlib as mpl
from matplotlib import rc
import scipy.io as sio
import pdb
mpl.use("pgf")
import matplotlib.pyplot as plt
import pandas
import sys
from palettable.cartocolors.qualitative import Prism_9 as color_pallette

pgf_with_custom_preamble = {
    "pgf.texsystem": "xelatex",
    "font.family": "sans-serif", # use san serif/main font for text elements
    "font.size": 10,
    "text.usetex": False,    # use inline math for ticks
    "pgf.rcfonts": False,   
    "pgf.preamble": [
        r"\usepackage{amsmath}",
        r"\usepackage{fontspec}",
        r"\setmainfont{Avenir Next}",
        r"\setsansfont{Avenir Next}",
    ]
}
mpl.rcParams.update(pgf_with_custom_preamble)

colors = color_pallette.mpl_colors

data = sio.loadmat('duelbandit_plot_data.mat')

fig, ax = plt.subplots(1, 1, figsize=(4.5,2))

n_param = 9
n_sub = 5
width = 0.85
pos = np.arange(n_param)+1.0
bottom = np.zeros((n_param,))

bar_plots = []
for sub in range(n_sub):
    ydata = data['copeland_score_total'][:,sub]
    b = ax.bar(pos, ydata, width = width, bottom=bottom, color = colors[2*sub])
    bar_plots.append(b)
    bottom += ydata

ax.legend(bar_plots, ('Subject 1', 'Subject 2' , 'Subject 3', 'Subject 4',
    'Subject 5'), loc = 'lower center', bbox_to_anchor=(0.45, 1.04), 
    ncol = n_sub, frameon=False, columnspacing=1.5, handletextpad=0.5, 
    fontsize=8)

ax.set_xticks(pos)

ax.set_ylabel('Total Copeland Score')
ax.set_xlabel('Parameter Set')

#turn off spines except left
ax.spines['bottom'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.set_ylim(0, 25)
ax.set_yticks(np.arange(0, 30, 5))

ax.tick_params('x', which='both',length=0)

inv_data = ax.transData.inverted()
inv_axes = ax.transAxes.inverted()

try:
    ylabelpos_axes = ax.yaxis.get_label().get_position()
    ylabelpos_display = ax.transAxes.transform(ylabelpos_axes)
    ylabelpos_data = inv_data.transform(ylabelpos_display)
    ylabelpos_data[1] = (ax.get_yticks()[0] + ax.get_yticks()[-1])/2.0
    ylabelpos_display = ax.transData.transform(ylabelpos_data)
    ylabelpos_axes = inv_axes.transform(ylabelpos_display)
    ax.yaxis.get_label().set_position(ylabelpos_axes)
except:
    pass

try:
    xlabelpos_axes = ax.xaxis.get_label().get_position()
    xlabelpos_display = ax.transAxes.transform(xlabelpos_axes)
    xlabelpos_data = inv_data.transform(xlabelpos_display)
    xlabelpos_data[0] = (ax.get_xticks()[0] + ax.get_xticks()[-1])/2.0
    xlabelpos_display = ax.transData.transform(xlabelpos_data)
    xlabelpos_axes = inv_axes.transform(xlabelpos_display)
    ax.xaxis.get_label().set_position(xlabelpos_axes)
except:
    pass

fig.savefig('copeland_scores_new.pdf', bbox_inches='tight')
plt.close(fig)
