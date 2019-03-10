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

colors = color_pallette.mpl_colors
subopt_alpha = 0.5

color_hum_fill = np.array((0.75, 0.75, 0.75))
color_hum_mean = np.array((0.0, 0.0, 0.0))

data = sio.loadmat('all_arm_data.mat')

fig, ax = plt.subplots(2, 2, figsize=(4,3), sharex='all')

ax[0,0].set_ylabel('Angle (Deg)')
ax[1,0].set_ylabel('Moment (N-m/kg)')
ax[1,0].set_xlabel('Stance Percent')
ax[1,1].set_xlabel('Stance Percent')

title_font_weight = 'heavy'
title_ypos = 1
ax[0,0].set_title('Knee Kinematics', weight=title_font_weight, 
    position=(0.5, title_ypos))
ax[0,1].set_title('Ankle Kinematics', weight=title_font_weight, 
    position=(0.5, title_ypos))
ax[1,0].set_title('Knee Moment', weight=title_font_weight, 
    position=(0.5, title_ypos))
ax[1,1].set_title('Ankle Moment', weight=title_font_weight, 
    position=(0.5, title_ypos))

time = np.squeeze(data['time_hum'])
ax[0,0].fill_between(time, 
    np.squeeze(data['knee_angle_hum_mean'] - data['knee_angle_hum_lb']),
    np.squeeze(data['knee_angle_hum_mean'] + data['knee_angle_hum_ub']), 
    interpolate=True, color = color_hum_fill)
ax[0,0].plot(time, data['knee_angle_hum_mean'], color = color_hum_mean,
    linewidth = 1)
ax[0,1].fill_between(time, 
    np.squeeze(data['ankle_angle_hum_mean'] - data['ankle_angle_hum_lb']),
    np.squeeze(data['ankle_angle_hum_mean'] + data['ankle_angle_hum_ub']), 
    interpolate=True, color = color_hum_fill)
ax[0,1].plot(time, data['ankle_angle_hum_mean'], color = color_hum_mean,
    linewidth = 1)
ax[1,0].fill_between(time, 
    np.squeeze(data['knee_moment_hum_mean'] - data['knee_moment_hum_lb']),
    np.squeeze(data['knee_moment_hum_mean'] + data['knee_moment_hum_ub']), 
    interpolate=True, color = color_hum_fill)
ax[1,0].plot(time, data['knee_moment_hum_mean'], color = color_hum_mean,
    linewidth = 1)
ax[1,1].fill_between(time, 
    np.squeeze(data['ankle_moment_hum_mean'] - data['ankle_moment_hum_lb']),
    np.squeeze(data['ankle_moment_hum_mean'] + data['ankle_moment_hum_ub']), 
    interpolate=True, color = color_hum_fill)
ax[1,1].plot(time, data['ankle_moment_hum_mean'], color = color_hum_mean,
    linewidth = 1)

time = data['time_pros'][0]
n_sub = 5
for i in range(n_sub):
    line_props = {'color':colors[2*i], 'alpha':0.25, 'linewidth':0.5}
    ax[0,0].plot(time,  data['subopt_data'][0,i]['knee_angle'][0,0].T, 
        **line_props)
    ax[0,1].plot(time,  data['subopt_data'][0,i]['ankle_angle'][0,0].T, 
        **line_props)
    ax[1,0].plot(time,  data['subopt_data'][0,i]['knee_moment'][0,0].T, 
        **line_props)
    ax[1,1].plot(time,  data['subopt_data'][0,i]['ankle_moment'][0,0].T, 
        **line_props)

for i in range(n_sub):
    line_props = {'color':colors[2*i], 'linewidth':1.5}
    ax[0,0].plot(time,  data['hand_data'][0,i]['knee_angle'][0,0].T, '--',
        **line_props)
    ax[0,1].plot(time,  data['hand_data'][0,i]['ankle_angle'][0,0].T, '--',
        **line_props)
    ax[1,0].plot(time,  data['hand_data'][0,i]['knee_moment'][0,0].T, '--',
        **line_props)
    ax[1,1].plot(time,  data['hand_data'][0,i]['ankle_moment'][0,0].T, '--',
        **line_props)

for i in range(n_sub):
    line_props = {'color':colors[2*i], 'linewidth':1.5}
    ax[0,0].plot(time,  data['opt_data'][i,0]['knee_angle'][0,0].T, 
        **line_props)
    ax[0,1].plot(time,  data['opt_data'][i,0]['ankle_angle'][0,0].T, 
        **line_props)
    ax[1,0].plot(time,  data['opt_data'][i,0]['knee_moment'][0,0].T, 
        **line_props)
    ax[1,1].plot(time,  data['opt_data'][i,0]['ankle_moment'][0,0].T, 
        **line_props)

#turn off all spines
for axis in ax.flatten():
    axis.set_xlim(-5, 100)
    axis.set_xticks(np.arange(0,150,50))
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
    axis.spines['bottom'].set_visible(False)
    axis.spines['left'].set_visible(False)

for axis in ax[0,:].flatten():
    axis.tick_params('x', which='both',length=0)
    [label.set_visible(False) for label in axis.get_xticklabels()]


ax[0,0].set_ylim(-25, 75)
ax[0,0].set_yticks(np.arange(-25, 100, 25))

ax[0,1].set_ylim(-40, 40)
ax[0,1].set_yticks(np.arange(-40, 60, 20))

ax[1,0].set_ylim(-1, 1)
ax[1,0].set_yticks(np.arange(-1, 2, 1))

ax[1,1].set_ylim(-2, 1)
ax[1,1].set_yticks(np.arange(-2,2,1))


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
plt.tight_layout()

#fig.subplots_adjust(hspace = 0.3, wspace = 0.3)
fig.savefig('kin_all_arms.pdf', bbox_inches='tight')
plt.close(fig)
