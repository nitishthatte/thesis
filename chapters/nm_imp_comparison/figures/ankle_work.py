import numpy as np
import matplotlib as mpl
from matplotlib import rc
import scipy.io as sio
import pdb
mpl.use("pgf")
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import pandas
import sys
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
        r"\usepackage{units}",
    ]
}
mpl.rcParams.update(pgf_with_custom_preamble)

#colors = [color_pallette.mpl_colors[i] 
#    for i in range(len(color_pallette.mpl_colors)) if i != 7]
colors = color_pallette.mpl_colors
colors.append((0., 0., 0.))

data = sio.loadmat('ankle_net_work.mat', squeeze_me=True)

fig, ax = plt.subplots(1, 1, figsize=(2,2))

ax.set_ylabel(r"Ankle Net Work (\unitfrac{J}{kg})")

num_subjects = 10
bar_color = [0.75, 0.75, 0.75]
x_pos = np.array((0, 1))
scatter_pts = np.linspace(-0.1,0.1,num_subjects)

ax.bar(x_pos, np.mean(data['ankle_net_work'][:,1:], 0), color = bar_color,
    tick_label=('NM','IMP'))
add_barplot_sigstars(ax, np.array([[0, 1]]), 
    np.array([data['p_values_ankle_net_work'][2]]), x_pos, star_loc='level')

subject_list = range(num_subjects)
scatter_opts = {'s':10, 'zorder':10,'marker':'o'}
for i in range(2):
    ax.scatter(x_pos[i] + scatter_pts, data['ankle_net_work'][:,i+1], 
        color=colors, **scatter_opts)

trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)
group_label_props = {'horizontalalignment':'center', 
    'verticalalignment':'center', 'transform':trans,
    'clip_on':False}

#turn off all spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

ax.tick_params('x', which='both',length=0)

#ax.set_yticks(np.arange(0, 1.2, 0.2))

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

plt.tight_layout()

fig.savefig('ankle_net_work.pdf', bbox_inches='tight')
plt.close(fig)

