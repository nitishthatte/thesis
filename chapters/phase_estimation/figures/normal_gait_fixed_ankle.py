import numpy as np
import matplotlib as mpl
from matplotlib import rc
import scipy.io as sio
import pdb
mpl.use("pgf")
import matplotlib.pyplot as plt
from palettable.cartocolors.qualitative import Prism_9 as color_pallette
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

fig, ax = plt.subplots(4, 1, figsize=(2,4), sharex='all')

ax[3].set_xlabel('Phase')

ax[0].set_ylabel('Knee Angle\n(deg)')
ax[1].set_ylabel('Ankle Angle\n(deg)')
ax[2].set_ylabel("Knee Moment\n"r"(\unitfrac{N-m}{kg})")
ax[3].set_ylabel("Ankle Moment\n"r"(\unitfrac{N-m}{kg})")

''' plot human data '''
data_folder = 'phase_var_fixed_ankle/'
data = sio.loadmat(data_folder+'normal_plot_data.mat')
human_phase = data['human_data']['percent_stance'][0][0].flatten()
human_knee_angle_mean = 180/np.pi*data['human_data'][
    'knee_angle_mean'][0][0].flatten()
human_ankle_angle_mean = 180/np.pi*data['human_data'][
    'ankle_angle_mean'][0][0].flatten()
human_knee_angle_sd = 180/np.pi*data['human_data'][
    'knee_angle_sd'][0][0].flatten()
human_ankle_angle_sd = 180/np.pi*data['human_data'][
    'ankle_angle_sd'][0][0].flatten()
human_knee_moment_mean = data['human_data']['knee_moment_mean'][0][0].flatten()
human_ankle_moment_mean = data['human_data'][
    'ankle_moment_mean'][0][0].flatten()
human_knee_moment_sd = data['human_data']['knee_moment_sd'][0][0].flatten()
human_ankle_moment_sd = data['human_data']['ankle_moment_sd'][0][0].flatten()

human_data_color = 'k'
human_area_alpha = 0.25
human_linewidth = 1

ax[0].fill_between(human_phase, 
    human_knee_angle_mean-2*human_knee_angle_sd, 
    human_knee_angle_mean+2*human_knee_angle_sd, 
    color = human_data_color, alpha = human_area_alpha, linewidth=0)
ax[0].plot(human_phase, human_knee_angle_mean, color = human_data_color, 
    linewidth = human_linewidth)

ax[1].fill_between(human_phase, 
    human_ankle_angle_mean-2*human_ankle_angle_sd, 
    human_ankle_angle_mean+2*human_ankle_angle_sd, 
    color = human_data_color, alpha = human_area_alpha, linewidth=0)
ax[1].plot(human_phase, human_ankle_angle_mean, color = human_data_color, 
    linewidth = human_linewidth)

ax[2].fill_between(human_phase, 
    human_knee_moment_mean-2*human_knee_moment_sd, 
    human_knee_moment_mean+2*human_knee_moment_sd, 
    color = human_data_color, alpha = human_area_alpha, linewidth=0)
ax[2].plot(human_phase, human_knee_moment_mean, color = human_data_color, 
    linewidth = human_linewidth)

ax[3].fill_between(human_phase, 
    human_ankle_moment_mean-2*human_ankle_moment_sd, 
    human_ankle_moment_mean+2*human_ankle_moment_sd, 
    color = human_data_color, alpha = human_area_alpha, linewidth=0)
ax[3].plot(human_phase, human_ankle_moment_mean, color = human_data_color, 
    linewidth = human_linewidth)

phase = data['normal_percent_stance'].flatten()
linewidth = 1

num_params = data['normal_plot_data'].shape[0]
for param in range(num_params):

    knee_angle_mean_gp = 180/np.pi*data['normal_plot_data'][param][0][
        'knee_angle_mean'][0][0].flatten()
    ankle_angle_mean_gp = 180/np.pi*data['normal_plot_data'][param][0][
        'ankle_angle_mean'][0][0].flatten()
    knee_moment_mean_gp = data['normal_plot_data'][param][0][
        'knee_moment_mean'][0][0].flatten()
    ankle_moment_mean_gp = data['normal_plot_data'][param][0][
        'ankle_moment_mean'][0][0].flatten()

    ax[0].plot(phase, knee_angle_mean_gp, color = colors[param]) 
    ax[1].plot(phase, ankle_angle_mean_gp, color = colors[param]) 
    ax[2].plot(phase, knee_moment_mean_gp, color = colors[param])
    ax[3].plot(phase, ankle_moment_mean_gp, color = colors[param]) 

#turn off all spines
for axis in ax.flatten():
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
    axis.spines['bottom'].set_visible(False)
    axis.spines['left'].set_visible(False)

for axis in ax[0:3]:
    axis.tick_params('x', which='both',length=0)
    [label.set_visible(False) for label in axis.get_xticklabels()]

ax[0].set_yticks((0, 20, 40))
ax[1].set_yticks((-20, 0, 20))
ax[2].set_yticks((-0.5, 0, 0.5))
ax[3].set_yticks(np.arange(-1.5, 0.75, 0.75))

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

fig.savefig('normal_data_fixed_ankle.pdf', bbox_inches='tight')
plt.close(fig)
