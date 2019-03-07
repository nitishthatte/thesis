import numpy as np
import matplotlib as mpl
from matplotlib import rc
import scipy.io as sio
import pdb
mpl.use("pgf")
import matplotlib.pyplot as plt
import sys

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

knee_data = {}
ankle_data = {}
knee_data['20']   = sio.loadmat('bandwidth_test_knee_20.mat')
knee_data['rms']  = sio.loadmat('bandwidth_test_knee_11.5.mat')
ankle_data['20']  = sio.loadmat('bandwidth_test_ankle_20.mat')
ankle_data['rms'] = sio.loadmat('bandwidth_test_ankle_55.6.mat')

fig = plt.figure(figsize = (6,3))
ax = []
ax.append(fig.add_subplot(221))
ax.append(fig.add_subplot(222, sharey = ax[0]))
ax.append(fig.add_subplot(223, sharex = ax[0]))
ax.append(fig.add_subplot(224, sharex = ax[1], sharey = ax[2]))


for i, key in enumerate(knee_data.keys()):
    ax[0].fill_between(knee_data[key]['freq_vec'].flatten(),
        np.nanmean(knee_data[key]['gain_mat'],1)
            -np.nanstd(knee_data[key]['gain_mat'],1),
        np.nanmean(knee_data[key]['gain_mat'],1)
            +np.nanstd(knee_data[key]['gain_mat'],1), color=colors_light[i])
    ax[0].plot(knee_data[key]['freq_vec'].flatten(), 
        np.nanmean(knee_data[key]['gain_mat'],1), color=colors[i])

    ax[1].fill_between(ankle_data[key]['freq_vec'].flatten(),
        np.nanmean(ankle_data[key]['gain_mat'],1)
            -np.nanstd(ankle_data[key]['gain_mat'],1),
        np.nanmean(ankle_data[key]['gain_mat'],1)
            +np.nanstd(ankle_data[key]['gain_mat'],1), color=colors_light[i])
    ax[1].plot(ankle_data[key]['freq_vec'].flatten(), 
        np.nanmean(ankle_data[key]['gain_mat'],1), color=colors[i])

    ax[2].fill_between(knee_data[key]['freq_vec'].flatten(),
        180/np.pi*np.nanmean(knee_data[key]['phase_mat'],1)
            -180/np.pi*np.nanstd(knee_data[key]['phase_mat'],1),
        180/np.pi*np.nanmean(knee_data[key]['phase_mat'],1)
            +180/np.pi*np.nanstd(knee_data[key]['phase_mat'],1), color=colors_light[i])
    ax[2].plot(knee_data[key]['freq_vec'].flatten(), 
        180/np.pi*np.nanmean(knee_data[key]['phase_mat'],1), color=colors[i])

    ax[3].fill_between(ankle_data[key]['freq_vec'].flatten(),
        180/np.pi*np.nanmean(ankle_data[key]['phase_mat'],1)
            -180/np.pi*np.nanstd(ankle_data[key]['phase_mat'],1),
        180/np.pi*np.nanmean(ankle_data[key]['phase_mat'],1)
            +180/np.pi*np.nanstd(ankle_data[key]['phase_mat'],1), color=colors_light[i])
    ax[3].plot(ankle_data[key]['freq_vec'].flatten(), 
        180/np.pi*np.nanmean(ankle_data[key]['phase_mat'],1), color=colors[i])

for axis in ax:
    axis.set_xscale('log')
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)

#turn off spines except left
ax[0].spines['bottom'].set_visible(False)
ax[1].spines['bottom'].set_visible(False)
ax[0].get_xaxis().set_visible(False)
ax[1].get_xaxis().set_visible(False)

ax[1].spines['left'].set_visible(False)
ax[3].spines['left'].set_visible(False)
ax[1].get_yaxis().set_visible(False)
ax[3].get_yaxis().set_visible(False)

ax[0].tick_params('y', which='both',direction='out')
ax[2].tick_params('y', which='both',direction='out')
ax[2].tick_params('x', which='both',direction='out')
ax[3].tick_params('x', which='both',direction='out')

# the x coords of this transformation are axes, and the
# y coord are data
ax[1].axhline(-3, -1.15, 1, clip_on = False, color='black', linestyle = '--')
ax[3].axhline(-180, -1.15, 1, clip_on = False, color='black', linestyle = '--')

ax[0].set_yticks([0, -3, -9])
ax[0].spines['left'].set_bounds(0, -9)
ax[2].set_yticks([0, -90, -180])
ax[2].spines['left'].set_bounds(0, -180)

ticks = ax[2].set_xticks(np.append(np.arange(1, 10),np.arange(10, 50, 10)), minor=True)
for tick in ticks:
    tick.label1.set_visible(False)
ticks[-1].label2.set_visible(True)
ax[2].spines['bottom'].set_bounds(1, 40)
ticks = ax[3].set_xticks(np.append(np.arange(1, 10),np.arange(10, 50, 10)), minor=True)
for tick in ticks:
    tick.label1.set_visible(False)
ticks[-1].label2.set_visible(True)
ax[3].spines['bottom'].set_bounds(1, 40)

ax[0].set_title('Knee Bode Plot')
ax[1].set_title('Ankle Bode Plot')

ax[0].set_ylabel('Gain (dB)')
ax[2].set_ylabel('Phase Lag (deg)')
ax[2].set_xlabel('Frequency (Hz)')
ax[3].set_xlabel('Frequency (Hz)')

fig.subplots_adjust(hspace = -0.2)

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
        xlabelpos_data[0] = (
            10**np.log10(np.array(ax[2].spines['bottom'].get_bounds())).mean())
        xlabelpos_display = axis.transData.transform(xlabelpos_data)
        xlabelpos_axes = inv_axes.transform(xlabelpos_display)
        axis.xaxis.get_label().set_position(xlabelpos_axes)
    except:
        pass

ylabel_pos0 = ax[0].yaxis.get_label().get_position()
ylabel_pos2 = ax[2].yaxis.get_label().get_position()

ax[0].yaxis.set_label_coords(-0.2, ylabel_pos0[1])
ax[2].yaxis.set_label_coords(-0.2, ylabel_pos2[1])

ax[2].legend(['20 N-m', 'RMS stance torque (11.5 N-m)'], fontsize=8,
    frameon=False, loc='upper center', bbox_to_anchor=(0.5, -0.3))
ax[3].legend(['20 N-m', 'RMS stance torque (55.6 N-m)'], fontsize=8,
    frameon=False, loc='upper center', bbox_to_anchor=(0.5, -0.3))

fig.savefig('bode_plots.pdf', bbox_inches='tight')
