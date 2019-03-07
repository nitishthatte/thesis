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
        r"\setsansfont{Avenir Next}",
        r"\setmainfont{Times}",
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

fig = plt.figure(figsize = (6,3))
ax = []
ax.append(fig.add_subplot(221))
ax.append(fig.add_subplot(222, sharey = ax[0]))
ax.append(fig.add_subplot(223, sharex = ax[0]))
ax.append(fig.add_subplot(224, sharex = ax[1], sharey = ax[2]))
ax.append(ax[0].twinx())
ax.append(ax[1].twinx())
for axis in ax[:-1]:
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
ax[-1].spines['top'].set_visible(False)

ax[0].plot(data['knee_time'], data['knee_angle_filt'] - 
    data['knee_angle_filt'][0], color=colors[0])
ax[0].set_ylabel('Angle (deg)', color=colors[0])
ax[0].tick_params('y', colors=colors[0])
ax[0].spines['left'].set_color(colors[0])

ax[4].plot(data['knee_pks_time'], data['knee_freq'], color=colors[1])

ax[1].plot(data['ankle_time'], data['ankle_angle_filt'] -
    data['ankle_angle_filt'][0], color=colors[0])

ax[5].plot(data['ankle_pks_time'], data['ankle_freq'], color=colors[1])
ax[5].set_ylabel('Approx Freq (Hz)', color=colors[1])
ax[5].tick_params('y', colors=colors[1])
ax[5].spines['right'].set_color(colors[1])

ax[2].plot(data['knee_time'], data['knee_torque_measured_filt'], 
    color = 'black')
ax[2].set_ylabel('Measured\nTorque (N-m)')

ax[3].plot(data['ankle_time'], data['ankle_torque_measured_filt'], 
    color = 'black')

ax[2].set_xlabel('Time (s)')
ax[3].set_xlabel('Time (s)')

#turn off bottom axes on top row
for i in [0 ,1, 4, 5]:
    ax[i].spines['bottom'].set_visible(False)
    ax[i].get_xaxis().set_visible(False)

#turn off y axes on right column
for i in [1, 3, 4]:
    ax[i].spines['left'].set_visible(False)
    ax[i].get_yaxis().set_visible(False)

ax[5].spines['left'].set_visible(False)

for axis in ax:
    axis.tick_params('y', which='both',direction='out')
    axis.tick_params('y', which='both',direction='out')

ax[0].set_yticks([-25, 0, 25])
ax[0].spines['left'].set_bounds(-25, 25)

ax[4].set_ylim(0, 4.3)
ax[5].set_ylim(0, 4.3)
ax[5].set_yticks([0, 2, 4])
ax[5].spines['right'].set_bounds(0, 4)

ax[2].set_yticks([-20, 0, 20])
ax[2].spines['left'].set_bounds(-20, 20)

ax[2].set_xticks(np.arange(0, 40, 10))
ax[2].spines['bottom'].set_bounds(0, 30)
ax[3].set_xticks(np.arange(0, 50, 10))
ax[3].spines['bottom'].set_bounds(0, 40)

ax[0].set_title('Knee')
ax[1].set_title('Ankle')
fig.suptitle('Zero Torque Tracking', y = 1.05)

fig.subplots_adjust(hspace = 0.4)

#adjust label pos
#adjust label pos
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
ylabel_pos0 = ax[0].yaxis.get_label().get_position()
ylabel_pos2 = ax[2].yaxis.get_label().get_position()

ax[0].yaxis.set_label_coords(-0.2, ylabel_pos0[1])
ax[2].yaxis.set_label_coords(-0.2, ylabel_pos2[1])

ax[2].legend(['20 N-m', 'RMS stance torque (11.5 N-m)'], fontsize=8,
    frameon=False, loc='upper center', bbox_to_anchor=(0.5, -0.3))
ax[3].legend(['20 N-m', 'RMS stance torque (55.6 N-m)'], fontsize=8,
    frameon=False, loc='upper center', bbox_to_anchor=(0.5, -0.3))
'''

#fig.savefig('zero_torque.pdf', bbox_inches='tight')
fig.savefig('zero_torque.png', dpi=300, bbox_inches='tight')
