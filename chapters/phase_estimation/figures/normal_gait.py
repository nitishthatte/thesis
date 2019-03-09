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


fig, ax = plt.subplots(4, 3, figsize=(6.5,4), sharex='all', sharey='row')

for axis in ax[3,:]:
    axis.set_xlabel('Phase')

ax[0,0].set_ylabel('Knee Angle\n(deg)')
ax[1,0].set_ylabel('Ankle Angle\n(deg)')
ax[2,0].set_ylabel("Knee Moment\n"r"(\unitfrac{N-m}{kg})")
ax[3,0].set_ylabel("Ankle Moment\n"r"(\unitfrac{N-m}{kg})")

title_props = {'weight':'semibold'}
ax[0,0].set_title('GP-EKF control', **title_props)
ax[0,1].set_title('NM control', **title_props)
ax[0,2].set_title('IMP control', **title_props)

''' plot human data '''
data = sio.loadmat('normal_plot_data.mat')
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
human_ankle_moment_mean = data['human_data']['ankle_moment_mean'][0][0].flatten()
human_knee_moment_sd = data['human_data']['knee_moment_sd'][0][0].flatten()
human_ankle_moment_sd = data['human_data']['ankle_moment_sd'][0][0].flatten()

human_data_color = 'k'
human_area_alpha = 0.25
human_linewidth = 1

for axis in ax[0, 0:3]:
    axis.fill_between(human_phase, 
        human_knee_angle_mean-2*human_knee_angle_sd, 
        human_knee_angle_mean+2*human_knee_angle_sd, 
        color = human_data_color, alpha = human_area_alpha, linewidth=0)
    axis.plot(human_phase, human_knee_angle_mean, color = human_data_color, 
        linewidth = human_linewidth)

for axis in ax[1, 0:3]:
    axis.fill_between(human_phase, 
        human_ankle_angle_mean-2*human_ankle_angle_sd, 
        human_ankle_angle_mean+2*human_ankle_angle_sd, 
        color = human_data_color, alpha = human_area_alpha, linewidth=0)
    axis.plot(human_phase, human_ankle_angle_mean, color = human_data_color, 
        linewidth = human_linewidth)

for axis in ax[2, 0:3]:
    axis.fill_between(human_phase, 
        human_knee_moment_mean-2*human_knee_moment_sd, 
        human_knee_moment_mean+2*human_knee_moment_sd, 
        color = human_data_color, alpha = human_area_alpha, linewidth=0)
    axis.plot(human_phase, human_knee_moment_mean, color = human_data_color, 
        linewidth = human_linewidth)

for axis in ax[3, 0:3]:
    axis.fill_between(human_phase, 
        human_ankle_moment_mean-2*human_ankle_moment_sd, 
        human_ankle_moment_mean+2*human_ankle_moment_sd, 
        color = human_data_color, alpha = human_area_alpha, linewidth=0)
    axis.plot(human_phase, human_ankle_moment_mean, color = human_data_color, 
        linewidth = human_linewidth)

phase = data['normal_percent_stance'].flatten()
linewidth = 1

num_subjects = data['normal_plot_data'].shape[0]
linestyle_able = '-'
linestyle_amp = '--'
linestyle_exp = '-.'
for subject in np.concatenate((np.arange(1,8), [0], [8])):

    knee_angle_mean_gp = 180/np.pi*data['normal_plot_data'][subject][0][0][
        'gp'][0][0]['knee_angle_mean'][0].flatten()  
    ankle_angle_mean_gp = 180/np.pi*data['normal_plot_data'][subject][0][0][
        'gp'][0][0]['ankle_angle_mean'][0].flatten()  
    knee_moment_mean_gp = data['normal_plot_data'][subject][0][0][
        'gp'][0][0]['knee_moment_mean'][0].flatten()  
    ankle_moment_mean_gp = data['normal_plot_data'][subject][0][0][
        'gp'][0][0]['ankle_moment_mean'][0].flatten()  
    knee_angle_mean_nm = 180/np.pi*data['normal_plot_data'][subject][0][0][
        'nm'][0][0]['knee_angle_mean'][0].flatten()  
    ankle_angle_mean_nm = 180/np.pi*data['normal_plot_data'][subject][0][0][
        'nm'][0][0]['ankle_angle_mean'][0].flatten()  
    knee_moment_mean_nm = data['normal_plot_data'][subject][0][0][
        'nm'][0][0]['knee_moment_mean'][0].flatten()  
    ankle_moment_mean_nm = data['normal_plot_data'][subject][0][0][
        'nm'][0][0]['ankle_moment_mean'][0].flatten()  
    knee_angle_mean_imp = 180/np.pi*data['normal_plot_data'][subject][0][0][
        'imp'][0][0]['knee_angle_mean'][0].flatten()  
    ankle_angle_mean_imp = 180/np.pi*data['normal_plot_data'][subject][0][0][
        'imp'][0][0]['ankle_angle_mean'][0].flatten()  
    knee_moment_mean_imp = data['normal_plot_data'][subject][0][0][
        'imp'][0][0]['knee_moment_mean'][0].flatten()  
    ankle_moment_mean_imp = data['normal_plot_data'][subject][0][0][
        'imp'][0][0]['ankle_moment_mean'][0].flatten()  

    if subject == 0:
        linestyle = linestyle_exp
    elif subject < 8:
        linestyle = linestyle_able
    else:
        linestyle = linestyle_amp

    ax[0,0].plot(phase, knee_angle_mean_gp, color = colors[subject], 
        linestyle=linestyle)
    ax[0,1].plot(phase, knee_angle_mean_nm, color = colors[subject], 
        linestyle=linestyle)
    ax[0,2].plot(phase, knee_angle_mean_imp, color = colors[subject], 
        linestyle=linestyle)

    ax[1,0].plot(phase, ankle_angle_mean_gp, color = colors[subject], 
        linestyle=linestyle)
    ax[1,1].plot(phase, ankle_angle_mean_nm, color = colors[subject], 
        linestyle=linestyle)
    ax[1,2].plot(phase, ankle_angle_mean_imp, color = colors[subject], 
        linestyle=linestyle)

    ax[2,0].plot(phase, knee_moment_mean_gp, color = colors[subject], 
        linestyle=linestyle)
    ax[2,1].plot(phase, knee_moment_mean_nm, color = colors[subject], 
        linestyle=linestyle)
    ax[2,2].plot(phase, knee_moment_mean_imp, color = colors[subject], 
        linestyle=linestyle)

    ax[3,0].plot(phase, ankle_moment_mean_gp, color = colors[subject], 
        linestyle=linestyle)
    ax[3,1].plot(phase, ankle_moment_mean_nm, color = colors[subject], 
        linestyle=linestyle)
    ax[3,2].plot(phase, ankle_moment_mean_imp, color = colors[subject], 
        linestyle=linestyle)

#turn off all spines
for axis in ax.flatten():
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
    axis.spines['bottom'].set_visible(False)
    axis.spines['left'].set_visible(False)

for axis in ax[0:3,:].flatten():
    axis.tick_params('x', which='both',length=0)
    [label.set_visible(False) for label in axis.get_xticklabels()]

for axis in ax[:,1:3].flatten():
    axis.tick_params('y', which='both',length=0)
    [label.set_visible(False) for label in axis.get_yticklabels()]

'''
ax[3].set_xlim((-2, 10))
ax[3].set_xticks(np.arange(-1, 11, 1))
ax[1].set_yticks(np.arange(0, 2.0, 0.5))
ax[2].set_ylim((-5, 20))
'''

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

fig.savefig('normal_data.pdf', bbox_inches='tight')
plt.close(fig)
