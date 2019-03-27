import numpy as np
import matplotlib as mpl
from matplotlib import rc
import scipy.io as sio
import pdb
mpl.use("pgf")
import matplotlib.pyplot as plt


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

#define colors http://paletton.com/#uid=73B1q0kleqtbzEKgVuIpcmGtdhZ
colors = ['#365D8A', '#973384', '#ABC944', '#D39C47']
colors_dark = ['#0F345D', '#670955', '#6D890C', '#8F5C0D']
colors_light = ['#81A0C1', '#CD83BF', '#E3F79E', '#FFDBA3']
stance_color = 0.85*np.ones(3)

data = sio.loadmat('torque_tracking_plot_data.mat', squeeze_me=True)

fig, ax = plt.subplots(1, 2, figsize=(4.5,2), sharex='all')

step_num = 10
desired_line_props = {'color':colors[0]}
measured_line_props = {'color':colors[1]}

plot_des_knee, = ax[0].plot(data['time_pros_stride'][step_num], 
    data['knee_torque_commanded_stride'][step_num], **desired_line_props)
plot_meas_knee, = ax[0].plot(data['time_pros_stride'][step_num], 
    data['knee_torque_measured_stride'][step_num], **measured_line_props)

plot_des_ankle, = ax[1].plot(data['time_pros_stride'][step_num], 
    data['ankle_torque_commanded_stride'][step_num], **desired_line_props)
plot_meas_ankle, = ax[1].plot(data['time_pros_stride'][step_num], 
    data['ankle_torque_measured_stride'][step_num], **measured_line_props)

#turn off all spines and set x axis to log scale
for axis in ax:
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
    axis.spines['bottom'].set_visible(False)
    axis.spines['left'].set_visible(False)

ax[0].set_ylabel('Knee Torque (N-m)')
ax[1].set_ylabel('Ankle Torque (N-m)')

for axis in ax:
    axis.set_xlabel('Time (s)')

ax[0].set_xlim((-0.1, 1.5))
ax[0].set_xticks(np.arange(0, 2.0, 0.5))
ax[1].set_xticks(np.arange(0, 2.0, 0.5))
ax[1].set_ylim((ax[1].get_ylim()[0], 40)) 

for axis in ax:
    patch_handle = axis.add_patch(mpl.patches.Rectangle((0, axis.get_ylim()[0]), 
    data['toeoff_time'][step_num], axis.get_ylim()[1] -axis.get_ylim()[0],
    color=stance_color, zorder=0))

ax[0].legend([plot_des_knee, plot_meas_knee, patch_handle], 
    ['Desired Torque', 'Measured Torque', 'Stance Phase'], frameon=False, 
    loc='lower center', bbox_to_anchor=(1.1, 1.0), ncol=3)

#center all axis labels in bounds
for axis in ax:
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

ax[1].yaxis.get_label().set_position(
    (ax[1].yaxis.get_label().get_position()[0],
     ax[0].yaxis.get_label().get_position()[1]))

fig.align_ylabels()
fig.subplots_adjust(wspace = 0.4)
#plt.tight_layout()
fig.savefig('torque_tracking.pdf', bbox_inches='tight')
