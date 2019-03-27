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
colors = ['#365D8A' ,'#973384' ,'#ABC944' ,'#D39C47']

data = sio.loadmat('grf_plot_data.mat', squeeze_me=True)

idx = np.logical_and(data['time'] > 115.9, data['time'] < 117.5)
data['time'] = data['time'] - data['time'][idx][0]

fig, ax = plt.subplots(1, 1, figsize=(2,3))
ax_twin = ax.twinx()
ax.set_zorder(ax_twin.get_zorder()+1) 
ax.patch.set_visible(False)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

ax_twin.spines['top'].set_visible(False)
ax_twin.spines['right'].set_visible(False)
ax_twin.spines['bottom'].set_visible(False)
ax_twin.spines['left'].set_visible(False)

actual_grf_handle, = ax_twin.plot(data['time'][idx], 
    data['grf_actual'][idx]*1000.0, color=colors[1], linewidth=1)
ax_twin.set_ylabel('Actual GRF (N)', color=colors[1])
ax_twin.tick_params('y', colors=colors[1])

color_main = colors[0];
heel_grf_handle, = ax.plot(data['time'][idx], data['grf_heel'][idx], 
    color=color_main, linewidth=1)
toe_grf_handle, = ax.plot(data['time'][idx], data['grf_toe'][idx], '--',
    color=color_main, linewidth=1)
ax.set_ylabel('GRF Sensor Value', color=color_main)
ax.tick_params('y', colors=color_main)

ax.set_xlabel('Time (s)')

ax_twin_ylim = ax_twin.get_ylim()
ax_ylim = ax.get_ylim()
ax_twin.set_ylim((ax_ylim[0]*ax_twin_ylim[1]/ax_ylim[1], ax_twin_ylim[1]))

ax.set_xticks([0, 0.75, 1.5])
ax.set_yticks(np.arange(0,2000,500))
ax_twin.set_yticks(np.arange(0,1000,200))

ax.legend([actual_grf_handle, heel_grf_handle, toe_grf_handle], 
    ['Actual GRF', 'Heel Sensor', 'Toe Sensor'], frameon=False, 
    loc='lower center', bbox_to_anchor=(0.5, 1.1))

#adjust label pos
#adjust label pos
inv_data = ax.transData.inverted()
inv_axes = ax.transAxes.inverted()

ylabelpos_axes = ax.yaxis.get_label().get_position()
ylabelpos_display = ax.transAxes.transform(ylabelpos_axes)
ylabelpos_data = inv_data.transform(ylabelpos_display)
ylabelpos_data[1] = (ax.get_yticks()[0] + ax.get_yticks()[-1])/2.0
ylabelpos_display = ax.transData.transform(ylabelpos_data)
ylabelpos_axes = inv_axes.transform(ylabelpos_display)
ax.yaxis.get_label().set_position(ylabelpos_axes)

xlabelpos_axes = ax.xaxis.get_label().get_position()
xlabelpos_display = ax.transAxes.transform(xlabelpos_axes)
xlabelpos_data = inv_data.transform(xlabelpos_display)
xlabelpos_data[0] = (ax.get_xticks()[0] + ax.get_xticks()[-1])/2.0
xlabelpos_display = ax.transData.transform(xlabelpos_data)
xlabelpos_axes = inv_axes.transform(xlabelpos_display)
ax.xaxis.get_label().set_position(xlabelpos_axes)

inv_data = ax_twin.transData.inverted()
inv_axes = ax_twin.transAxes.inverted()

ylabelpos_axes = ax_twin.yaxis.get_label().get_position()
ylabelpos_display = ax_twin.transAxes.transform(ylabelpos_axes)
ylabelpos_data = inv_data.transform(ylabelpos_display)
ylabelpos_data[1] = (ax_twin.get_yticks()[0] + ax_twin.get_yticks()[-1])/2.0
ylabelpos_display = ax_twin.transData.transform(ylabelpos_data)
ylabelpos_axes = inv_axes.transform(ylabelpos_display)
ax_twin.yaxis.get_label().set_position(ylabelpos_axes)

plt.tight_layout()
fig.savefig('grf_sensing.pdf', bbox_inches='tight')
