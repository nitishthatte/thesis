import numpy as np
import matplotlib as mpl
from matplotlib import rc
import scipy.io as sio
import pdb
mpl.use("pgf")
import matplotlib.pyplot as plt
import pandas
import sys
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

#define colors http://paletton.com/#uid=73B1q0kleqtbzEKgVuIpcmGtdhZ
colors = np.array(((217., 82., 25., 50.),
                   (0., 114., 189., 50.)))/255;
'''
colors_med = np.array(((217., 82., 25., 128.),
                   (0., 114., 189., 200.)))/255;
'''
colors_med = np.array(((152., 58., 17., 128.),
                   (0., 77., 127., 200.)))/255;

data = sio.loadmat('traj_data.mat')
time_swing = data['time_swing'].flatten()

minjerk_normal_knee_med = \
    180.0/np.pi*data['unconstrained_normal_knee_med'].flatten()
minjerk_normal_ankle_med = \
    180.0/np.pi*data['unconstrained_normal_ankle_med'].flatten()
minjerk_normal_time = data['unconstrained_normal_time']
minjerk_normal_knee = 180.0/np.pi*data['unconstrained_normal_knee']
minjerk_normal_ankle = 180.0/np.pi*data['unconstrained_normal_ankle']
mpc_normal_knee_med = \
    180.0/np.pi*data['constrained_normal_knee_med'].flatten()
mpc_normal_ankle_med = \
    180.0/np.pi*data['constrained_normal_ankle_med'].flatten()
mpc_normal_time = data['constrained_normal_time']
mpc_normal_knee = 180.0/np.pi*data['constrained_normal_knee']
mpc_normal_ankle = 180.0/np.pi*data['constrained_normal_ankle']

minjerk_disturb_knee_med = \
    180.0/np.pi*data['unconstrained_disturb_knee_med'].flatten()
minjerk_disturb_ankle_med = \
    180.0/np.pi*data['unconstrained_disturb_ankle_med'].flatten()
minjerk_disturb_time = data['unconstrained_disturb_time']
minjerk_disturb_knee = 180.0/np.pi*data['unconstrained_disturb_knee']
minjerk_disturb_ankle = 180.0/np.pi*data['unconstrained_disturb_ankle']
mpc_disturb_knee_med = \
    180.0/np.pi*data['constrained_disturb_knee_med'].flatten()
mpc_disturb_ankle_med = \
    180.0/np.pi*data['constrained_disturb_ankle_med'].flatten()
mpc_disturb_time = data['constrained_disturb_time']
mpc_disturb_knee = 180.0/np.pi*data['constrained_disturb_knee']
mpc_disturb_ankle = 180.0/np.pi*data['constrained_disturb_ankle']

fig = plt.figure(figsize=(4.5,3))
ax = []
ax.append(fig.add_subplot(221))
ax.append(fig.add_subplot(222, sharex=ax[0], sharey=ax[0]))
ax.append(fig.add_subplot(223, sharex=ax[0]))
ax.append(fig.add_subplot(224, sharex=ax[0], sharey=ax[2]))

ax[0].set_ylabel('Knee Flexion\nAngle (deg)')
ax[2].set_ylabel('Ankle Dorsiflexion\nAngle (deg)')
ax[2].set_xlabel('Swing Time (s)')

linewidth = 0.5
linewidth_med = 1.5

ax[0].plot(mpc_normal_time, mpc_normal_knee, color = colors[1,:],
    linewidth=linewidth)
ax[0].plot(minjerk_normal_time, minjerk_normal_knee, color = colors[0,:], 
    linewidth=linewidth)
'''
ax[0].plot(mpc_normal_time, mpc_normal_knee_med, color = colors_med[1,:],
    linewidth=linewidth_med)
ax[0].plot(time_swing, minjerk_normal_knee_med, color = colors_med[0,:], 
    linewidth=linewidth_med)
'''

ax[1].plot(mpc_disturb_time, mpc_disturb_knee, color = colors[1,:],
    linewidth=linewidth)
ax[1].plot(minjerk_disturb_time, minjerk_disturb_knee, color = colors[0,:], 
    linewidth=linewidth)
'''
ax[1].plot(mpc_disturb_time, mpc_disturb_knee_med, color = colors_med[1,:],
    linewidth=linewidth_med)
ax[1].plot(time_swing, minjerk_disturb_knee_med, color = colors_med[0,:], 
    linewidth=linewidth_med)
'''

ax[2].plot(mpc_normal_time, mpc_normal_ankle, color = colors[1,:],
    linewidth=linewidth)
ax[2].plot(minjerk_normal_time, minjerk_normal_ankle, color = colors[0,:], 
    linewidth=linewidth)
'''
ax[2].plot(mpc_normal_time, mpc_normal_ankle_med, color = colors_med[1,:],
    linewidth=linewidth_med)
ax[2].plot(time_swing, minjerk_normal_ankle_med, color = colors_med[0,:], 
    linewidth=linewidth_med)
'''

ax[3].plot(mpc_disturb_time, mpc_disturb_ankle, color = colors[1,:],
    linewidth=linewidth)
ax[3].plot(minjerk_disturb_time, minjerk_disturb_ankle, color = colors[0,:], 
    linewidth=linewidth)
'''
ax[3].plot(mpc_disturb_time, mpc_disturb_ankle_med, color = colors_med[1,:],
    linewidth=linewidth_med)
ax[3].plot(time_swing, minjerk_disturb_ankle_med, color = colors_med[0,:], 
    linewidth=linewidth_med)
'''

#turn off all spines
for i in range(4):
    ax[i].spines['top'].set_visible(False)
    ax[i].spines['right'].set_visible(False)
    ax[i].spines['bottom'].set_visible(False)
    ax[i].spines['left'].set_visible(False)

ax[0].tick_params('x', which='both',length=0)
ax[1].tick_params('x', which='both',length=0)
[label.set_visible(False) for label in ax[0].get_xticklabels()]
[label.set_visible(False) for label in ax[1].get_xticklabels()]

ax[1].tick_params('y', which='both',length=0)
ax[3].tick_params('y', which='both',length=0)
[label.set_visible(False) for label in ax[1].get_yticklabels()]
[label.set_visible(False) for label in ax[3].get_yticklabels()]

ax[2].set_xticks(np.arange(0,0.8,0.2))
ax[3].set_xticks(np.arange(0,0.8,0.2))
ax[0].set_yticks(np.arange(0, 120, 30))
ax[2].set_yticks(np.arange(-20, 40, 20))

title_font_weight = 'bold'
title_ypos = 1.0

ax[0].set_title('Normal\nTrajectories', fontweight=title_font_weight, 
    position=(0.5, title_ypos))
ax[1].set_title('Trip Elicitation\nTrajectories', fontweight=title_font_weight, 
    position=(0.5, title_ypos))

#center all axis labels in bounds

for axis in ax:
    inv_data = axis.transData.inverted()
    inv_axes = axis.transAxes.inverted()

    try:
        ylabelpos_axes = axis.yaxis.get_label().get_position()
        ylabelpos_display = axis.transAxes.transform(ylabelpos_axes)
        ylabelpos_data = inv_data.transform(ylabelpos_display)
        ylabelpos_data[1] = np.array(axis.spines['left'].get_bounds()).mean()
        ylabelpos_display = axis.transData.transform(ylabelpos_data)
        ylabelpos_axes = inv_axes.transform(ylabelpos_display)
        axis.yaxis.get_label().set_position(ylabelpos_axes)
    except:
        pass
    
    '''
    try:
        xlabelpos_axes = axis.xaxis.get_label().get_position()
        xlabelpos_display = axis.transAxes.transform(xlabelpos_axes)
        xlabelpos_data = inv_data.transform(xlabelpos_display)
        xlabelpos_data[0] = np.array(axis.spines['bottom'].get_bounds()).mean()
        xlabelpos_display = axis.transData.transform(xlabelpos_data)
        xlabelpos_axes = inv_axes.transform(xlabelpos_display)
        axis.xaxis.get_label().set_position(xlabelpos_axes)
    except:
        pass
    '''

inv_data = ax[2].transData.inverted()
inv_axes = ax[2].transAxes.inverted()
xlabelpos_axes = ax[2].xaxis.get_label().get_position()
xlabelpos_display = ax[2].transAxes.transform(xlabelpos_axes)
xlabelpos_data = inv_data.transform(xlabelpos_display)
xlabelpos_data[0] = 0.675
xlabelpos_display = ax[2].transData.transform(xlabelpos_data)
xlabelpos_axes = inv_axes.transform(xlabelpos_display)
ax[2].xaxis.get_label().set_position(xlabelpos_axes)

fig.align_ylabels()
fig.subplots_adjust(hspace = 0.5, wspace = 0.1)

fig.savefig('trajectories.pdf', bbox_inches='tight')
plt.close(fig)
