import numpy as np
import matplotlib as mpl
from matplotlib import rc
import scipy.io as sio
import pdb
mpl.use("pgf")
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import pandas
from palettable.cartocolors.qualitative import Prism_9 as color_pallette
import sys
import sys 
sys.path.append('..')
from sigstars import add_barplot_sigstars
#import omnigraffle

pgf_with_custom_preamble = {
    "pgf.texsystem": "xelatex",
    "font.family": "sans-serif", # use san serif/main font for text elements
    "font.size": 6,
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
colors = color_pallette.mpl_colors
colors.append((0., 0., 0.))

data = sio.loadmat('torso_variability.mat', squeeze_me=True)

fig, ax = plt.subplots(1, 1, figsize=(4.5,3))

ax.set_ylabel('Torso Pitch Angle\nVariability (rad)')

num_subjects = 10
bar_color = [0.75, 0.75, 0.75]
x_pos = np.array((0, 1, 2, 4, 5, 6))
rand_scatter_pts = 0.05*np.random.randn(num_subjects)

ax.bar(x_pos, np.median(data['torso_std_x'],0), color = bar_color,
    tick_label=('No Pros','NM','IMP','No Pros','NM','IMP'))
add_barplot_sigstars(ax, data['condition_combinations']-1, 
    data['p_values_torso_std_x'], x_pos, star_loc='3x3')

subject_list = range(num_subjects)
scatter_opts = {'s':10, 'zorder':10,'marker':'o'}
for i in range(6):
    ax.scatter(x_pos[i] + rand_scatter_pts, data['torso_std_x'][:,i], 
        color=colors, **scatter_opts)

trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)
group_label_props = {'horizontalalignment':'center', 
    'verticalalignment':'center', 'fontsize':6, 'transform':trans,
    'clip_on':False}
group_label_pos = -0.2;
ax.text(1, group_label_pos, 'No Disturbance', **group_label_props)
ax.text(5, group_label_pos, 'With Disturbance', **group_label_props)

#turn off all spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

ax.tick_params('x', which='both',length=0)

#ax.set_yticks(np.arange(0, 0.15, 0.05))

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
fig.subplots_adjust(bottom=-group_label_pos)

plt.tight_layout()

fig.savefig('../treadmill_vib_torso_var_x.pdf', bbox_inches='tight')
plt.close(fig)
