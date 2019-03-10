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
    ]
}
mpl.rcParams.update(pgf_with_custom_preamble)

#define colors http://paletton.com/#uid=73B1q0kleqtbzEKgVuIpcmGtdhZ
colors_hum = np.array(((220, 147, 175),
                         (147,  49,  87),
                         ( 73,   0,  28)))/255;
colors_hum = np.concatenate((colors_hum, 0.25*np.ones((3,1))), axis=1)

colors_fit = np.array(((196, 231, 154),
                       (107, 154,  51),
                       ( 41,  77,   0)))/255;
colors_fit = np.concatenate((colors_fit, 0.25*np.ones((3,1))), axis=1)

data = sio.loadmat('nm_fit_data.mat')

fig = plt.figure(figsize=(4.5,3))
fig, ax = plt.subplots(2, 2, figsize=(4,3), sharex=True, sharey=True)

ax[1,0].set_xlabel('Time (s)')
ax[1,1].set_xlabel('Time (s)')
ax[0,0].set_ylabel('Moment (N-m/kg)')
ax[1,0].set_ylabel('Moment (N-m/kg)')

time0 = data['sim_time'][0][0]
time1 = data['sim_time'][0][1]
linewidth = 0.5
title_font_weight = 'heavy'
for i in range(3):
    ax[0,0].plot(time0,  data['knee_torque_human_1'][0][i].T, 
        color = colors_hum[i,:], linewidth=linewidth)
    ax[0,1].plot(time0,  data['ankle_torque_human_1'][0][i].T, 
        color = colors_hum[i,:], linewidth=linewidth)
    ax[1,0].plot(time1,  data['knee_torque_human_2'][0][i].T, 
        color = colors_hum[i,:], linewidth=linewidth)
    ax[1,1].plot(time1,  data['ankle_torque_human_2'][0][i].T, 
        color = colors_hum[i,:], linewidth=linewidth)

for i in range(3):
    ax[0,0].plot(time0,  data['knee_torque_fit_1'][0][i].T,
        color = colors_fit[i,:], linewidth=linewidth)
    ax[0,1].plot(time0,  data['ankle_torque_fit_1'][0][i].T,
        color = colors_fit[i,:], linewidth=linewidth)
    ax[1,0].plot(time1,  data['knee_torque_fit_2'][0][i].T,
        color = colors_fit[i,:], linewidth=linewidth)
    ax[1,1].plot(time1,  data['ankle_torque_fit_2'][0][i].T,
        color = colors_fit[i,:], linewidth=linewidth)

title_ypos = 1.0
ax[0,0].set_title('Param 1 Knee', weight=title_font_weight, 
    position=(0.5, title_ypos))
ax[0,1].set_title('Param 1 Ankle', weight=title_font_weight, 
    position=(0.5, title_ypos))
ax[1,0].set_title('Param 2 Knee', weight=title_font_weight, 
    position=(0.5, title_ypos))
ax[1,1].set_title('Param 2 Ankle', weight=title_font_weight, 
    position=(0.5, title_ypos))

#turn off all spines and adjust xlim
#ax[i].set_xlim(-0.1,1)
#ax[i].set_ylim(-2.2,2)
for axis in ax.flatten():
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

ax[1,0].set_xticks(np.arange(0,1.5,0.5))
ax[1,1].set_xticks(np.arange(0,1.5,0.5))
ax[0,0].set_yticks(range(-2,2))
ax[1,0].set_yticks(range(-2,2))

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

fig.subplots_adjust(hspace = 1.0, wspace = 0.4)
#plt.tight_layout()
fig.savefig('nm_fit.pdf', bbox_inches='tight')
plt.close(fig)
