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

data = sio.loadmat('prob_grf_data.mat')

fig = plt.figure(figsize=(3,2))
ax = []
ax.append(fig.add_subplot(211))
ax.append(fig.add_subplot(212, sharex=ax[0]))

ax[1].set_xlabel('Integrated GRF (N-s)')
ax[1].set_ylabel('Probability of Integrated GRF')

x_pts = data['kdenpts'].flatten()
y_pts_mpc = data['kden_con'].flatten()
y_pts_minjerk = data['kden_uncon'].flatten()

linewidth = 2
minjerk_handle = ax[0].fill_between(x_pts, 0, y_pts_minjerk, color = colors[0,:],
    linewidth=0)
mpc_handle = ax[0].fill_between(x_pts, 0, y_pts_mpc, color = colors[1,:], 
    linewidth=0)
ax[1].fill_between(x_pts, 0, y_pts_minjerk, color = colors[0,:],
    linewidth=0)
ax[1].fill_between(x_pts, 0, y_pts_mpc, color = colors[1,:], linewidth=0)

ax[0].legend((minjerk_handle, mpc_handle), 
    ('Minimum Jerk Control', 'Proposed Control'), frameon=False)

#set spline visibility, axis limits tick marks
ax[0].spines['top'].set_visible(False)
ax[0].spines['right'].set_visible(False)
ax[0].spines['bottom'].set_visible(False)
ax[0].spines['left'].set_visible(False)
ax[0].tick_params('x', which='both',length=0)
[label.set_visible(False) for label in ax[0].get_xticklabels()]
ax[0].set_ylim((0.14, 0.25))
ax[0].spines['left'].set_bounds(0.14, 0.25)
ax[0].set_yticks(np.arange(0.15,0.30, 0.05))
ax[0].set_xlim((-1, 20))
ax[0].spines['bottom'].set_bounds(0, 20)
ax[0].set_xticks(np.arange(0,25,5))

ax[1].spines['top'].set_visible(False)
ax[1].spines['right'].set_visible(False)
ax[1].spines['bottom'].set_visible(False)
ax[1].spines['left'].set_visible(False)
ylim = (-0.005, 0.055)
ax[1].set_ylim(ylim)
ax[1].spines['left'].set_bounds(ylim[0], ylim[1])
ax[1].set_yticks(np.arange(0.,0.075, 0.025))
ax[1].spines['bottom'].set_bounds(0, 20)
ax[1].set_xticks(np.arange(0,25,5))

#center all axis labels in bounds

inv_data = ax[1].transData.inverted()
inv_axes = ax[1].transAxes.inverted()

try:
    ylabelpos_axes = ax[1].yaxis.get_label().get_position()
    ylabelpos_display = ax[1].transAxes.transform(ylabelpos_axes)
    ylabelpos_data = inv_data.transform(ylabelpos_display)
    ylabelpos_data[1] = 0.06
    ylabelpos_display = ax[1].transData.transform(ylabelpos_data)
    ylabelpos_axes = inv_axes.transform(ylabelpos_display)
    ax[1].yaxis.get_label().set_position(ylabelpos_axes)
except:
    pass

try:
    xlabelpos_axes = ax[1].xaxis.get_label().get_position()
    xlabelpos_display = ax[1].transAxes.transform(xlabelpos_axes)
    xlabelpos_data = inv_data.transform(xlabelpos_display)
    xlabelpos_data[0] = np.array(ax[1].spines['bottom'].get_bounds()).mean()
    xlabelpos_display = ax[1].transData.transform(xlabelpos_data)
    xlabelpos_axes = inv_axes.transform(xlabelpos_display)
    ax[1].xaxis.get_label().set_position(xlabelpos_axes)
except:
    pass

title_font_weight = 'bold'
fig.suptitle('Propensity for Foot Scuffing', fontweight=title_font_weight)

fig.align_ylabels()

# add squigly line at axis break
d = .015  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=ax[0].transAxes, color='k', clip_on=False, 
    linewidth=1.5)
axes_break_xpts = np.linspace(-d, +d)
axes_break_ypts = d*np.sin(2*np.pi*axes_break_xpts/(2*d))
ax[0].plot(axes_break_xpts , axes_break_ypts , **kwargs) # top-left diagonal
kwargs.update(transform=ax[1].transAxes)  # switch to the bottom axes
ax[1].plot(axes_break_xpts , 1+axes_break_ypts , **kwargs) # top-left diagonal

fig.subplots_adjust(hspace = 0.2)
fig.savefig('prob_grf.pdf', bbox_inches='tight')
plt.close(fig)
