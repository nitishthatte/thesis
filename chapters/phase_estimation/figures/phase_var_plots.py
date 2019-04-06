import numpy as np
import matplotlib as mpl
from matplotlib import rc, cm, colors
from matplotlib.collections import LineCollection
import scipy.io as sio
import pdb
mpl.use("pgf")
import matplotlib.pyplot as plt
import sys 
sys.path.append('..')
from sigstars import add_barplot_sigstars
from mpl_toolkits.axes_grid1.colorbar import colorbar
#import omnigraffle

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

color0 = '#476A92'
color1 = '#A0468F'
color2 = '#BAD55E'
color3 = '#DFAE62'
stance_color = 0.85*np.ones(3)

data = sio.loadmat('phase_var_plot_data.mat', squeeze_me=True)
#time_idx = np.argwhere(np.logical_and(data['time']>64.9, data['time']<72.3))
stance_on = np.argwhere((data['stance'][0:-1].flatten() == 0)
    & (data['stance'][1:].flatten() == 1)
    & (data['time'][1:].flatten() > 64.9)
    & (data['time'][1:].flatten() < 74)).flatten()

stance_off = np.argwhere((data['stance'][0:-1].flatten() == 1)
    & (data['stance'][1:].flatten() == 0)
    & (data['time'][1:].flatten() > 64.9)
    & (data['time'][1:].flatten() < 74)).flatten()

idx_plt = np.arange(stance_on[0], stance_on[-1]) + 1

data['time'] -= data['time'][idx_plt[0]]
num_steps = stance_on.shape[0] - 1

fig, ax = plt.subplots(3, 1, figsize=(6.5,5), sharex='all')

text_loc = (-0.15, 1)
text_prop = {'fontsize':10}
legend_prop = {'frameon':False, 'bbox_to_anchor':(1.03,0.5), 
    'loc':'center left'}

plt_hndl_phase_bnd, = ax[0].plot(data['time'][idx_plt], 
    data['phase_lb'][idx_plt], 'k')
ax[0].plot(data['time'][idx_plt], data['phase_ub'][idx_plt], 'k')
plt_hndl_phase_norm, = ax[0].plot(data['time'][idx_plt], 
    data['phase_norm'][idx_plt], color=color0)
plt_hndl_constrained_phase_norm, = ax[0].plot(data['time'][idx_plt],
    data['constrained_phase_norm'][idx_plt], color=color1)
ax[0].legend([plt_hndl_phase_norm, plt_hndl_constrained_phase_norm,
    plt_hndl_phase_bnd], ['Normalized Phase\nUnconstrained', 
    'Normalized Phase\nConstrained', 'Phase Bounds'], **legend_prop)
ax[0].text(text_loc[0], text_loc[1], 'a)', transform=ax[0].transAxes,
    **text_prop)

plt_hndl_hip_angle, = ax[1].plot(data['time'][idx_plt], 
    data['hip_angle'][idx_plt], color=color0)
plt_hndl_hip_angle_shifted, = ax[1].plot(data['time'][idx_plt], 
    data['hip_angle_shifted'][idx_plt], color=color1)
plt_hndl_hip_angle_zero_mean, = ax[1].plot(data['time'][idx_plt], 
    data['hip_angle_zero_mean'][idx_plt], color=color2)
ax[1].legend([plt_hndl_hip_angle, plt_hndl_hip_angle_shifted,
    plt_hndl_hip_angle_zero_mean], ['Hip Angle', 'Hip Angle\nShifted', 
    'Hip Angle\nZero Mean'], **legend_prop)
ax[1].text(text_loc[0], text_loc[1], 'b)', transform=ax[1].transAxes,
    **text_prop)


plt_hndl_hip_integral, = ax[2].plot(data['time'][idx_plt], 
    data['hip_integral'][idx_plt], color=color0)
plt_hndl_hip_integral_shifted, = ax[2].plot(data['time'][idx_plt],
    data['hip_integral_shifted'][idx_plt], color=color1)
ax[2].legend([plt_hndl_hip_integral, plt_hndl_hip_integral_shifted],
    ['Hip Angle\nIntegral', 'Hip Angle\nIntegral Shifted'], **legend_prop)
ax[2].text(text_loc[0], text_loc[1], 'c)', transform=ax[2].transAxes,
    **text_prop)

for axis in ax:
    for stance_on_step, stance_off_step in zip(stance_on[0:-1], stance_off[0:-1]):
        patch_handle = axis.add_patch(mpl.patches.Rectangle(
            (data['time'][stance_on_step], axis.get_ylim()[0]), 
            data['time'][stance_off_step] - data['time'][stance_on_step], 
            axis.get_ylim()[1] - axis.get_ylim()[0],
            color=stance_color, zorder=0))

#turn off all spines
for axis in ax:
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
    axis.spines['bottom'].set_visible(False)
    axis.spines['left'].set_visible(False)

for axis in ax[0:-1]:
    axis.tick_params('x', which='both',length=0)
    [label.set_visible(False) for label in axis.get_xticklabels()]

ax[0].set_yticks(np.arange(0, 1.2, 0.2))
ax[1].set_yticks(np.arange(-0.4, 0.8, 0.4))
ax[2].set_yticks(np.arange(-0.2, 0.2, 0.1))

ax[0].set_ylabel('Phase')
ax[1].set_ylabel('Hip Angle (rad)')
ax[2].set_ylabel('Hip Angle\nIntegral (rad-s)')
ax[2].set_xlabel('Time (s)')

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

fig.align_ylabels()
fig.subplots_adjust(hspace = 0.5)
plt.tight_layout()

fig.savefig('phase_var_plot_vs_time.pdf', bbox_inches='tight')
plt.close(fig)

''' polar plot of phase and radius '''
fig, ax = plt.subplots(1, 1, figsize=(4.5,5),
    subplot_kw={'projection':'polar'})

#ax.plot(data['phase'][idx_plt], data['radius'][idx_plt])
num_pts = idx_plt.shape[0]
res = 10
time = data['time'][idx_plt][0::res]
phase = data['phase'][idx_plt][0::res]
radius = data['radius'][idx_plt][0::res]

cnorm = mpl.colors.Normalize(vmin=0, vmax=8)
points = np.array([phase, radius]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
lc = LineCollection(segments, cmap=cm.plasma, norm = cnorm)
lc.set_array(time)
lc.set_capstyle('round')
ax.add_collection(lc)
ax.set_rgrids(np.arange(0.4, 1.6, 0.4))
ax.set_rmax(1.2)
ax.set_xlabel('Hip Angle Axis',labelpad=10)
ax.set_ylabel('Hip Integral Axis',labelpad=35)


# add an axes above the main axes.
cax = fig.add_axes([0.11, 1.0, 0.8, 0.05])
cb = mpl.colorbar.ColorbarBase(cax, cmap=cm.plasma, norm=cnorm,
    orientation='horizontal', drawedges=False)
# change tick position to top. Tick position defaults to bottom and overlaps
# the image.
cb.outline._visible=False
cax.xaxis.set_ticks_position("bottom")
cax.set_xlabel('Time (s)')

fig.savefig('phase_var_plot_vs_polar.pdf', bbox_inches='tight')
plt.close(fig)
