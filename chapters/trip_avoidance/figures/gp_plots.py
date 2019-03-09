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

#define colors http://paletton.com/#uid=73B1q0kleqtbzEKgVuIpcmGtdhZ
colors = np.array(((217., 82., 25., 128.),
                   (0., 114., 189., 128.)))/255;

data = sio.loadmat('gp_plot_data.mat')
time_joint = data['time_joint'].flatten()
hip_angle_joint_mean = data['hip_angle_joint_mean'].flatten()
hip_angle_joint_sd = data['hip_angle_joint_sd'].flatten() 
hip_height_joint_mean = data['hip_height_joint_mean'].flatten()
hip_height_joint_sd = data['hip_height_joint_sd'].flatten()
time_swing_completed = data['time_swing_completed'].flatten()
hip_angle_completed = data['hip_angle_completed'].flatten()
hip_height_completed = data['hip_height_completed'].flatten()
time_cond = data['time_cond'].flatten()
hip_angle_cond = data['hip_angle_cond'].flatten()
hip_height_cond = data['hip_height_cond'].flatten()
time_predict = data['time_predict'].flatten()
hip_angle_predict = data['hip_angle_predict'].flatten()
hip_angle_predict_sd = data['hip_angle_predict_sd'].flatten()
hip_height_predict = data['hip_height_predict'].flatten()
hip_height_predict_sd = data['hip_height_predict_sd'].flatten()

data2 = sio.loadmat('gp_plot_data_2.mat')
swing_time_vec = data2['swing_time_vec'].flatten()
hip_angle_vec = data2['hip_angle_vec'].flatten()
hip_height_vec = data2['hip_height_vec'].flatten()

fig = plt.figure(figsize=(3,3))
ax = []
ax.append(fig.add_subplot(211))
ax.append(fig.add_subplot(212, sharex=ax[0]))

ax[0].set_ylabel('Hip Angle (rad)')
ax[1].set_ylabel('Hip Height (m)')
ax[1].set_xlabel('Swing Time (s)')

linewidth = 2

ax[0].fill_between(time_joint, hip_angle_joint_mean - 2*hip_angle_joint_sd, 
    hip_angle_joint_mean + 2*hip_angle_joint_sd, color = colors[0,:],
    linewidth=0)
ax[0].fill_between(time_predict, hip_angle_predict - 2*hip_angle_predict_sd, 
    hip_angle_predict + 2*hip_angle_predict_sd, color = colors[1,:],
    linewidth=0)
ax[0].plot(time_joint, hip_angle_joint_mean, color = colors[0,0:3],
    linewidth=linewidth)
ax[0].plot(time_predict, hip_angle_predict, color = colors[1,0:3],
    linewidth=linewidth)
ax[0].plot(swing_time_vec, hip_angle_vec, color='k', linewidth=1)
ax[0].plot(time_cond, hip_angle_cond, 'ok', linewidth=0, markersize=3)

ax[1].fill_between(time_joint, hip_height_joint_mean - 2*hip_height_joint_sd, 
    hip_height_joint_mean + 2*hip_height_joint_sd, color = colors[0,:],
    linewidth=0)
ax[1].fill_between(time_predict, hip_height_predict - 2*hip_height_predict_sd, 
    hip_height_predict + 2*hip_height_predict_sd, color = colors[1,:],
    linewidth=0)
ax[1].plot(time_joint, hip_height_joint_mean, color = colors[0,0:3],
    linewidth=linewidth)
ax[1].plot(time_predict, hip_height_predict, color = colors[1,0:3],
    linewidth=linewidth)
ax[1].plot(swing_time_vec, hip_height_vec, color='k', linewidth=1)
ax[1].plot(time_cond, hip_height_cond, 'ok', linewidth=0, markersize=3)

#turn off all spines
for i in range(2):
    ax[i].spines['top'].set_visible(False)
    ax[i].spines['right'].set_visible(False)
    ax[i].spines['bottom'].set_visible(False)
    ax[i].spines['left'].set_visible(False)

ax[0].tick_params('x', which='both',length=0)
[label.set_visible(False) for label in ax[0].get_xticklabels()]

ax[1].set_xticks(np.arange(0,0.8,0.2))
ax[0].set_yticks(np.arange(-0.2,0.8,0.2))
ax[1].set_yticks(np.arange(0.850,0.99,0.05))

#center all axis labels in bounds

for axis in ax:
    inv_data = axis.transData.inverted()
    inv_axes = axis.transAxes.inverted()

    try:
        ylabelpos_axes = axis.yaxis.get_label().get_position()
        ylabelpos_display = axis.transAxes.transform(ylabelpos_axes)
        ylabelpos_data = inv_data.transform(ylabelpos_display)
        ylabelpos_data[1] = np.array(axis.get_yticks()).mean()
        ylabelpos_display = axis.transData.transform(ylabelpos_data)
        ylabelpos_axes = inv_axes.transform(ylabelpos_display)
        axis.yaxis.get_label().set_position(ylabelpos_axes)
    except:
        pass
    
    try:
        xlabelpos_axes = axis.xaxis.get_label().get_position()
        xlabelpos_display = axis.transAxes.transform(xlabelpos_axes)
        xlabelpos_data = inv_data.transform(xlabelpos_display)
        xlabelpos_data[0] = np.array(axis.get_xticks()).mean()
        xlabelpos_display = axis.transData.transform(xlabelpos_data)
        xlabelpos_axes = inv_axes.transform(xlabelpos_display)
        axis.xaxis.get_label().set_position(xlabelpos_axes)
    except:
        pass

fig.align_ylabels()
#fig.subplots_adjust(hspace = 0.5, wspace = 0.1)

fig.savefig('gp_plots.pdf', bbox_inches='tight')
plt.close(fig)
