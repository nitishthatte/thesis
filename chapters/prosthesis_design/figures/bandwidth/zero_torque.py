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
    "font.sans-serif": ["Avenir Next"],
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
colors = []
colors.append('#365D8A')
colors.append('#973384')
colors.append('#ABC944')
colors.append('#D39C47')
colors_dark = []
colors_dark.append('#0F345D')
colors_dark.append('#670955')
colors_dark.append('#6D890C')
colors_dark.append('#8F5C0D')
colors_light = []
colors_light.append('#81A0C1')
colors_light.append('#CD83BF')
colors_light.append('#E3F79E')
colors_light.append('#FFDBA3')

data = sio.loadmat('zero_torque_data.mat')

fig, ax = plt.subplots(2, 2, figsize=(4.5,3), sharex='col', sharey='row')
ax_twin = []
ax_twin.append(ax[0,0].twinx())
ax_twin.append(ax[0,1].twinx())

for axis in ax.flatten():
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
    axis.spines['bottom'].set_visible(False)
    axis.spines['left'].set_visible(False)

for axis in ax_twin:
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
    axis.spines['bottom'].set_visible(False)
    axis.spines['left'].set_visible(False)

ax[0,0].plot(data['knee_time'], data['knee_angle_filt'] - 
    data['knee_angle_filt'][0], color=colors[0])
ax[0,0].set_ylabel('Angle (deg)', color=colors[0])
ax[0,0].tick_params('y', colors=colors[0])

ax_twin[0].plot(data['knee_pks_time'], data['knee_freq'], color=colors[1])

ax[0,1].plot(data['ankle_time'], data['ankle_angle_filt'] -
    data['ankle_angle_filt'][0], color=colors[0])

ax_twin[1].plot(data['ankle_pks_time'], data['ankle_freq'], color=colors[1])
ax_twin[1].set_ylabel('Approx Freq (Hz)', color=colors[1])
ax_twin[1].tick_params('y', colors=colors[1])

line_props_torque_measured = {'color':'black','linewidth':0.25}
ax[1,0].plot(data['knee_time'], data['knee_torque_measured_filt'], 
    **line_props_torque_measured)
ax[1,0].set_ylabel('Measured\nTorque (N-m)')

ax[1,1].plot(data['ankle_time'], data['ankle_torque_measured_filt'], 
    **line_props_torque_measured)

ax[1,0].set_xlabel('Time (s)')
ax[1,1].set_xlabel('Time (s)')

#turn off bottom axes on top row
for axis in ax[0,:].flatten():
    axis.get_xaxis().set_visible(False)

for axis in ax[:,1].flatten():
    axis.get_yaxis().set_visible(False)

for axis in ax_twin:
    axis.get_xaxis().set_visible(False)

#turn off y axes on right column
ax_twin[0].get_yaxis().set_visible(False)

for axis in ax.flatten():
    axis.tick_params('x', which='both',direction='out')
    axis.tick_params('y', which='both',direction='out')

for axis in ax_twin:
    axis.tick_params('x', which='both',direction='out')
    axis.tick_params('y', which='both',direction='out')

ax[0,0].set_yticks([-25, 0, 25])

ax_twin[0].set_ylim(0, 4.3)
ax_twin[1].set_ylim(0, 4.3)
ax_twin[1].set_yticks([0, 2, 4])

ax[1,0].set_yticks([-20, 0, 20])

fig.savefig('zero_torque.pdf', bbox_inches='tight')

ax[0,0].set_xticks(np.arange(0, 40, 10))
ax[1,1].set_xticks(np.arange(0, 50, 10))

ax[0,0].set_title('Knee')
ax[0,1].set_title('Ankle')
fig.suptitle('Zero Torque Tracking', y = 1.05)

fig.subplots_adjust(hspace = 0.4)

#adjust label pos
#adjust label pos
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

for axis in ax_twin:
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

fig.savefig('../zero_torque.pdf', bbox_inches='tight')
