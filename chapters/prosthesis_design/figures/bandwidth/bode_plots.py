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

knee_data = {}
ankle_data = {}
knee_data['20']   = sio.loadmat('bandwidth_test_knee_20.mat')
knee_data['rms']  = sio.loadmat('bandwidth_test_knee_11.5.mat')
ankle_data['20']  = sio.loadmat('bandwidth_test_ankle_20.mat')
ankle_data['rms'] = sio.loadmat('bandwidth_test_ankle_55.6.mat')

fig, ax = plt.subplots(2, 2, figsize=(4.5,3), sharex='all', sharey='row')

#plot experiment data
for i, key in enumerate(knee_data.keys()):
    exp_fill_props = {'color':colors_light[i]}
    exp_line_props = {'color':colors[i]}
    ax[0,0].fill_between(knee_data[key]['freq_vec'].flatten(),
        np.nanmean(knee_data[key]['gain_mat'],1)
            -np.nanstd(knee_data[key]['gain_mat'],1),
        np.nanmean(knee_data[key]['gain_mat'],1)
            +np.nanstd(knee_data[key]['gain_mat'],1), **exp_fill_props)
    ax[0,0].plot(knee_data[key]['freq_vec'].flatten(), 
        np.nanmean(knee_data[key]['gain_mat'],1), **exp_line_props)

    ax[0,1].fill_between(ankle_data[key]['freq_vec'].flatten(),
        np.nanmean(ankle_data[key]['gain_mat'],1)
            -np.nanstd(ankle_data[key]['gain_mat'],1),
        np.nanmean(ankle_data[key]['gain_mat'],1)
            +np.nanstd(ankle_data[key]['gain_mat'],1), **exp_fill_props)
    ax[0,1].plot(ankle_data[key]['freq_vec'].flatten(), 
        np.nanmean(ankle_data[key]['gain_mat'],1), **exp_line_props)

    ax[1,0].fill_between(knee_data[key]['freq_vec'].flatten(),
        180/np.pi*np.nanmean(knee_data[key]['phase_mat'],1)
            -180/np.pi*np.nanstd(knee_data[key]['phase_mat'],1),
        180/np.pi*np.nanmean(knee_data[key]['phase_mat'],1)
            +180/np.pi*np.nanstd(knee_data[key]['phase_mat'],1), **exp_fill_props)
    ax[1,0].plot(knee_data[key]['freq_vec'].flatten(), 
        180/np.pi*np.nanmean(knee_data[key]['phase_mat'],1), **exp_line_props)

    ax[1,1].fill_between(ankle_data[key]['freq_vec'].flatten(),
        180/np.pi*np.nanmean(ankle_data[key]['phase_mat'],1)
            -180/np.pi*np.nanstd(ankle_data[key]['phase_mat'],1),
        180/np.pi*np.nanmean(ankle_data[key]['phase_mat'],1)
            +180/np.pi*np.nanstd(ankle_data[key]['phase_mat'],1), **exp_fill_props)
    ax[1,1].plot(ankle_data[key]['freq_vec'].flatten(), 
        180/np.pi*np.nanmean(ankle_data[key]['phase_mat'],1), **exp_line_props)

#turn off all spines and set x axis to log scale
for axis in ax.flatten():
    axis.set_xscale('log')
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
    axis.spines['bottom'].set_visible(False)
    axis.spines['left'].set_visible(False)

for axis in ax[0,:].flatten():
    axis.tick_params('x', which='both',length=0)
    [label.set_visible(False) for label in axis.get_xticklabels()]

for axis in ax[:,1].flatten():
    axis.tick_params('y', which='both',length=0)
    [label.set_visible(False) for label in axis.get_yticklabels()]

ax[0,0].set_yticks([0, -3, -9])
ax[1,0].set_yticks([0, -90, -180])

ax[0,0].set_title('Knee Bode Plot')
ax[0,1].set_title('Ankle Bode Plot')

ax[0,0].set_ylabel('Gain (dB)')
ax[1,0].set_ylabel('Phase Lag (deg)')
ax[1,0].set_xlabel('Frequency (Hz)')
ax[1,1].set_xlabel('Frequency (Hz)')

#plot bandwidth limit lines
bandwidth_line_props = {'clip_on':False, 'color':(0.5, 0.5, 0.5), 'linestyle':'--', 
    'linewidth':0.8, 'zorder': 10}
ax[0,1].axhline(-3, -1.15, 1, **bandwidth_line_props)
ax[1,1].axhline(-180, -1.15, 1, **bandwidth_line_props)

ax[1,0].axvline(24.75, 0, 1.8, **bandwidth_line_props)
ax[1,1].axvline(7, 0, 1.8, **bandwidth_line_props)


fig.subplots_adjust(hspace = -0.2)

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

    ''' 
    try:
        xlabelpos_axes = axis.xaxis.get_label().get_position()
        xlabelpos_display = axis.transAxes.transform(xlabelpos_axes)
        xlabelpos_data = inv_data.transform(xlabelpos_display)
        xlabelpos_data[0] = (axis.get_xticks()[0] + axis.get_xticks()[-1])/2.0
        xlabelpos_display = axis.transData.transform(xlabelpos_data)
        xlabelpos_axes = inv_axes.transform(xlabelpos_display)
        axis.xaxis.get_label().set_position(xlabelpos_axes)
        pdb.set_trace()
    except:
        pass
    '''

fig.align_ylabels()

ax[1,0].legend(['20 N-m', 'RMS stance torque (11.5 N-m)'], fontsize=8,
    frameon=False, loc='upper center', bbox_to_anchor=(0.5, -0.3))
ax[1,1].legend(['20 N-m', 'RMS stance torque (55.6 N-m)'], fontsize=8,
    frameon=False, loc='upper center', bbox_to_anchor=(0.5, -0.3))

fig.savefig('bode_plots.pdf', bbox_inches='tight')
