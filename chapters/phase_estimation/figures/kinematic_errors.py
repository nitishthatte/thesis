import numpy as np
import matplotlib as mpl
from matplotlib import rc
import scipy.io as sio
import pdb
mpl.use("pgf")
import matplotlib.pyplot as plt
from palettable.cartocolors.qualitative import Prism_9 as color_pallette
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
        r"\usepackage{units}",
    ]
}
mpl.rcParams.update(pgf_with_custom_preamble)

#colors = [color_pallette.mpl_colors[i] 
#    for i in range(len(color_pallette.mpl_colors)) if i != 7]
colors = color_pallette.mpl_colors

data = sio.loadmat('kinematic_error_data.mat')

fig, ax = plt.subplots(2, 2, figsize=(3,3.5), sharex='all', sharey='row')

ax[0,0].set_ylabel('Angle  Error\n(deg)')
ax[1,0].set_ylabel("Moment Error\n"r"(\unitfrac{N-m}{kg})")

for label, axes in zip(('a', 'b', 'c', 'd'), ax.flatten()):
    axes.text(-0.15, 1.1, label, horizontalalignment='left', 
        transform=axes.transAxes, fontsize=12)

title_props = {'weight':'semibold','pad':27}
ax[0,0].set_title('Knee', **title_props)
ax[0,1].set_title('Ankle', **title_props)

num_subjects = 9
bar_color = [0.75, 0.75, 0.75]
x_pos = np.arange(0,3)
rand_scatter_pts = 0.05*np.random.randn(num_subjects)
scatter_opts = {'s':8, 'zorder':10}

subject_list = np.concatenate((np.arange(1,8), [0], [8]))
marker_able = 'o'
marker_amp = '^'
marker_exp = 's'

#plot bar plots and sig stars
ax[0,0].bar(x_pos, 180/np.pi*data['knee_angle_errors_median'].flatten(), 
    color = bar_color)
add_barplot_sigstars(ax[0,0], data['condition_combinations']-1, 
    data['p_values_knee_angle'].flatten(), 
    180/np.pi*np.max(data['knee_angle_errors']))

ax[0,1].bar(x_pos, 180/np.pi*data['ankle_angle_errors_median'].flatten(), 
    color = bar_color)
add_barplot_sigstars(ax[0,1], data['condition_combinations']-1, 
    data['p_values_ankle_angle'].flatten(), 
    180/np.pi*np.max(data['ankle_angle_errors']))

ax[1,0].bar(x_pos, data['knee_moment_errors_median'].flatten(), 
    color = bar_color, tick_label=('GP-EKF','NM','IMP'))
add_barplot_sigstars(ax[1,0], data['condition_combinations']-1, 
    data['p_values_knee_moment'].flatten(), 
    np.max(data['knee_moment_errors']))

ax[1,1].bar(x_pos, data['ankle_moment_errors_median'].flatten(), 
    color = bar_color, tick_label=('GP-EKF','NM','IMP'))
add_barplot_sigstars(ax[1,1], data['condition_combinations']-1, 
    data['p_values_ankle_moment'].flatten(), 
    np.max(data['ankle_moment_errors']))

for i in range(3):
    for sub in subject_list:
        if sub==0:
            marker = marker_exp
        elif sub==8:
            marker = marker_amp
        else:
            marker = marker_able

        color = colors[sub]
        ax[0,0].scatter(x_pos[i] + rand_scatter_pts[sub], 
            180/np.pi*data['knee_angle_errors'][sub,i], color=color, 
            marker=marker, **scatter_opts)

        ax[0,1].scatter(x_pos[i] + rand_scatter_pts[sub], 
            180/np.pi*data['ankle_angle_errors'][sub,i], color=color, 
            marker=marker, **scatter_opts)

        ax[1,0].scatter(x_pos[i] + rand_scatter_pts[sub], 
            data['knee_moment_errors'][sub,i], color=color, 
            marker=marker, **scatter_opts)

        ax[1,1].scatter(x_pos[i] + rand_scatter_pts[sub], 
            data['ankle_moment_errors'][sub,i], color=color, 
            marker=marker, **scatter_opts)

#turn off all spines
for axis in ax.flatten():
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
    axis.spines['bottom'].set_visible(False)
    axis.spines['left'].set_visible(False)

for axis in ax.flatten():
    axis.tick_params('x', which='both',length=0)

for axis in ax[0,:].flatten():
    [label.set_visible(False) for label in axis.get_xticklabels()]

for axis in ax[:,1].flatten():
    axis.tick_params('y', which='both',length=0)
    [label.set_visible(False) for label in axis.get_yticklabels()]

ax[0,0].set_yticks(np.arange(0, 16, 4))
ax[1,0].set_yticks(np.arange(0, 60, 20))

#center all axis labels in bounds

for axis in ax.flatten():
    inv_data = axis.transData.inverted()
    inv_axes = axis.transAxes.inverted()

    try:
        ylabelpos_axes = axis.yaxis.get_label().get_position()
        ylabelpos_display = axis.transAxes.transform(ylabelpos_axes)
        ylabelpos_data = inv_data.transform(ylabelpos_display)
        ylabelpos_data[1] = (axis.get_yticks()[0] + axis.get_yticks()[-1])/2.0
        ylabelpos_display = axis.transData.transform(ylabelpos_data)
        ylabelpos_axes = inv_axes.transform(ylabelpos_display)
        axis.yaxis.get_label().set_position(ylabelpos_axes)
    except:
        pass
    
    try:
        xlabelpos_axes = axis.xaxis.get_label().get_position()
        xlabelpos_display = axis.transAxes.transform(xlabelpos_axes)
        xlabelpos_data = inv_data.transform(xlabelpos_display)
        xlabelpos_data[0] = (axis.get_xticks()[0] + axis.get_xticks()[-1])/2.0
        xlabelpos_display = axis.transData.transform(xlabelpos_data)
        xlabelpos_axes = inv_axes.transform(xlabelpos_display)
        axis.xaxis.get_label().set_position(xlabelpos_axes)
    except:
        pass

fig.align_ylabels()
#fig.subplots_adjust(hspace = 0.5, wspace = 0.2)
plt.tight_layout()

fig.savefig('kinematic_errors.pdf', bbox_inches='tight')
plt.close(fig)
