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

data = sio.loadmat('toe_vs_hip_data.mat')

fig = plt.figure(figsize=(3,2))
ax = fig.add_subplot(111)

ax.set_xlabel('Average Hip Height (mm)')
ax.set_ylabel('Average Toe Height (mm)')

minjerk_scatter_xpts = data['unconstrained_hip_height_pts'].flatten()
minjerk_scatter_ypts = data['unconstrained_toe_height_pts'].flatten()
mpc_scatter_xpts = data['constrained_hip_height_pts'].flatten()
mpc_scatter_ypts = data['constrained_toe_height_pts'].flatten()

line_xpts = data['hip_height_vec'].flatten()
minjerk_line_pts = data['unconfit'].flatten()
mpc_line_pts = data['confit'].flatten()

markersize = 10
minjerk_handle = ax.scatter(minjerk_scatter_xpts, minjerk_scatter_ypts,
    markersize, color = colors[0,:], linewidth=0)
ax.plot(line_xpts, minjerk_line_pts, color = colors[0,0:3], linewidth=2)
mpc_handle = ax.scatter(mpc_scatter_xpts, mpc_scatter_ypts, 
    markersize, color = colors[1,:], linewidth=0)
ax.plot(line_xpts, mpc_line_pts, color = colors[1,0:3], linewidth=2)


ax.legend((minjerk_handle, mpc_handle), 
    ('Minimum Jerk Control', 'Proposed Control'), frameon=False)

#set spline visibility, axis limits tick marks
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
'''
ylim = (-0.001, 0.011)
ax.set_ylim(ylim)
ax.spines['left'].set_bounds(ylim[0], ylim[1])
ax.set_yticks(np.arange(0.,0.015, 0.005))
ax.spines['bottom'].set_bounds(0, 90)
ax.set_xticks(np.arange(0,120,30))
'''
ax.set_xticks(np.arange(820,960+35,35))

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

fig.savefig('toe_vs_hip_height.pdf', bbox_inches='tight')
plt.close(fig)
