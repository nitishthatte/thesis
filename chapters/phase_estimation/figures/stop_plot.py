import numpy as np
import matplotlib as mpl
from matplotlib import rc, lines
import scipy.io as sio
import pdb
mpl.use("pgf")
import matplotlib.pyplot as plt
import sys
from palettable.cartocolors.qualitative import Prism_9 as color_pallette
#import omnigraffle

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

#colors = np.array(((217., 82., 25.),
#                   (0., 114., 189.)))/255;
colors = color_pallette.mpl_colors

fig, ax = plt.subplots(4, 1, figsize=(3,4), sharex='all')
ax[0].set_ylabel('Estimated Phase')
ax[1].set_ylabel('Estimated Phase\nVelocity (phase/s)')
ax[2].set_ylabel('Knee Angle (deg)')
ax[3].set_ylabel('Ankle Angle (deg)')
ax[3].set_xlabel('Time (s)')

for label, axes in zip(('a', 'b', 'c', 'd'), ax.flatten()):
    axes.text(-0.21, 1.05, label, horizontalalignment='left', 
        transform=axes.transAxes, fontsize=8)

data = sio.loadmat('stop_data.mat')
num_subjects = data['stop_data'].squeeze().shape[0]
for subject in range(num_subjects):
    time = data['stop_data'].squeeze()[subject][0]['time'][0].flatten()
    idx = np.logical_and(time >= -1.5,time <= 10.0)

    time = time[idx]
    phase_ekf = data['stop_data'].squeeze()[subject][0][
        'phase_ekf'][0].flatten()[idx]
    phase_time = data['stop_data'].squeeze()[subject][0][
        'phase_time'][0].flatten()[idx]
    phase_vel_ekf = data['stop_data'].squeeze()[subject][0][
        'phase_vel_ekf'][0].flatten()[idx]
    phase_vel_time = data['stop_data'].squeeze()[subject][0][
        'phase_vel_time'][0].flatten()[idx]
    knee_angle = data['stop_data'].squeeze()[subject][0][
        'knee_angle'][0].flatten()[idx]*180.0/np.pi
    ankle_angle = data['stop_data'].squeeze()[subject][0][
        'ankle_angle'][0].flatten()[idx]*180.0/np.pi

    line_props = dict(color = colors[subject], linewidth=1)

    ax[0].plot(time, phase_time, '--', **line_props)
    ax[0].plot(time, phase_ekf, '-', **line_props)
    
    ax[1].plot(time, phase_vel_time, '--', **line_props)
    ax[1].plot(time, phase_vel_ekf, '-', **line_props)

    ax[2].plot(time, knee_angle, '-', **line_props)
    ax[3].plot(time, ankle_angle, '-', **line_props)

legend_line_props = dict(linewidth=1, color = 'k')
legend_time_line = lines.Line2D([0], [0], linestyle='--', **legend_line_props)
legend_ekf_line = lines.Line2D([0], [0], linestyle='-', **legend_line_props)

ax[3].legend((legend_time_line, legend_ekf_line), 
    ('Time-Based Phase Estimation', 'EKF phase estimation'), frameon=False)

#turn off all spines
for axis in ax:
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
    axis.spines['bottom'].set_visible(False)
    axis.spines['left'].set_visible(False)

for axis in ax[0:3]:
    axis.tick_params('x', which='both',length=0)
    [label.set_visible(False) for label in axis.get_xticklabels()]

ax[3].set_xlim((-2, 10))
ax[3].set_xticks(np.arange(-1, 11, 1))
ax[1].set_yticks(np.arange(0, 2.0, 0.5))
ax[2].set_ylim((-5, 20))

ax[3].axvline(x = 0, ymin = 0.02, ymax = 4.86, linestyle = ':', clip_on = False, 
    zorder = 0, color='k', linewidth=0.8)

#center all axis labels in bounds
fig.align_ylabels()
fig.subplots_adjust(hspace = 0.3)

for i, axis in enumerate(ax):
    inv_data = axis.transData.inverted()
    inv_axes = axis.transAxes.inverted()

    try:
        ylabelpos_axes = axis.yaxis.get_label().get_position()
        ylabelpos_display = axis.transAxes.transform(ylabelpos_axes)
        ylabelpos_data = inv_data.transform(ylabelpos_display)
        if i == 2:
            ylabelpos_data[1] = (axis.get_yticks()[1] + axis.get_yticks()[-1])/2.0
        else:
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

fig.savefig('stop_plot.pdf', bbox_inches='tight')
plt.close(fig)
