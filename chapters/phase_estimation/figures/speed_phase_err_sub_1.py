import numpy as np
import matplotlib as mpl
from matplotlib import rc
import scipy.io as sio
import pdb
mpl.use("pgf")
import matplotlib.pyplot as plt
import pandas
import sys

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
colors = np.array(((217., 82., 25.),
                   (0., 114., 189.)))/255;

data = sio.loadmat('speed_phase_est_sub_1_data.mat')

fig = plt.figure(figsize=(4.5,2.5))
ax = fig.add_subplot(111)

ax.set_xlabel('True Phase')
ax.set_ylabel('Estimated Phase')

linewidth = 0.5
time_handle = ax.plot(data['phase_actual'].transpose(),
    data['phase_time'].transpose(), color = colors[0,:], linewidth=linewidth)
ekf_handle = ax.plot(data['phase_actual'].transpose(), 
    data['phase_ekf'].transpose(), color = colors[1,:], linewidth=linewidth)

ax.legend((time_handle[0], ekf_handle[0]), 
    ('Time-Based Phase Estimation', 'EKF phase estimation'), frameon=False,
    loc='lower center', bbox_to_anchor=(0.45, 1.01), ncol=2)

#set spline visibility, axis limits tick marks
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

ax.set_yticks(np.arange(0.0, 1.5, 0.5))

#center all axis labels in bounds

inv_data = ax.transData.inverted()
inv_axes = ax.transAxes.inverted()

try:
    ylabelpos_axes = ax.yaxis.get_label().get_position()
    ylabelpos_display = ax.transAxes.transform(ylabelpos_axes)
    ylabelpos_data = inv_data.transform(ylabelpos_display)
    ylabelpos_data[1] = np.array(ax.get_yticks).mean()
    ylabelpos_display = ax.transData.transform(ylabelpos_data)
    ylabelpos_axes = inv_axes.transform(ylabelpos_display)
    ax.yaxis.get_label().set_position(ylabelpos_axes)
except:
    pass

try:
    xlabelpos_axes = ax.xaxis.get_label().get_position()
    xlabelpos_display = ax.transAxes.transform(xlabelpos_axes)
    xlabelpos_data = inv_data.transform(xlabelpos_display)
    xlabelpos_data[0] = np.array(ax.get_xticks).mean()
    xlabelpos_display = ax.transData.transform(xlabelpos_data)
    xlabelpos_axes = inv_axes.transform(xlabelpos_display)
    ax.xaxis.get_label().set_position(xlabelpos_axes)
except:
    pass

plt.tight_layout()

fig.savefig('speed_phase_err_sub_1.pdf', bbox_inches='tight')
plt.close(fig)
