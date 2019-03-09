import numpy as np
import matplotlib as mpl
from matplotlib import rc
import scipy.io as sio
import pdb
mpl.use("pgf")
import matplotlib.pyplot as plt
import pandas
#import sys
from palettable.cartocolors.qualitative import Prism_9 as color_pallette
from sigstars import add_barplot_sigstars
#import omnigraffle

pgf_with_custom_preamble = {
    "pgf.texsystem": "xelatex",
    "font.family": "sans-serif", # use san serif/main font for text elements
    "font.size": 8,
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

#colors = [color_pallette.mpl_colors[i] 
#    for i in range(len(color_pallette.mpl_colors)) if i != 7]
colors = color_pallette.mpl_colors[0:-1]

data = sio.loadmat('falls_plot_data.mat')

fig, ax = plt.subplots(1, 1, figsize=(2,2))

ax.set_ylabel('Number of Falls')

num_subjects = 8
bar_color = [0.75, 0.75, 0.75]
x_pos = np.arange(0,3)
rand_scatter_pts = 0.05*np.random.randn(num_subjects)

#add num falls
ax.bar(x_pos, data['all_falls_median'].flatten(), color = bar_color,
    tick_label=('GP-EKF','NM','IMP'))
add_barplot_sigstars(ax, data['condition_combinations']-1, 
    data['p_values_falls'].flatten(), x_pos)

subject_list = np.concatenate((np.arange(1,8), [0]))
marker_able = 'o'
marker_exp = 's'
scatter_opts = {'s':16, 'zorder':10}
for i in range(3):
    for sub in subject_list:
        if sub==0:
            marker = marker_exp
        else:
            marker = marker_able

        ax.scatter(x_pos[i] + rand_scatter_pts[sub], data['all_falls'][sub,i], 
            marker=marker, color=colors[sub], **scatter_opts)

#turn off all spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

ax.tick_params('x', which='both',length=0)

#ax[0,0].set_yticks(np.arange(0, 16, 4))

#center all axis labels in bounds

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

fig.align_ylabels()
#fig.subplots_adjust(hspace = 0.5, wspace = 0.2)
plt.tight_layout()

fig.savefig('num_falls.pdf', bbox_inches='tight')
plt.close(fig)
