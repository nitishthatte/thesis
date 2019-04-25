import numpy as np
import matplotlib as mpl
from matplotlib import rc, lines
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
color0      = '#476A92'
color0light = '#9EC0E7'
color1      = '#BAD55E'
color1light = '#E3F6A2'
color2      = '#A0468F'
color2light = '#EA9ADB'
color3      = '#DFAE62'
color3light = '#F8D6A3'
color_grey = [0.85, 0.85, 0.85]

data = sio.loadmat('nm_fit_data.mat', squeeze_me=True)

fig, ax = plt.subplots(1, 2, figsize=(4,2), sharex=True, sharey=True)

num_steps = data['sim_torques'].shape[0]

hum_line_props = {'color':color_grey, 'zorder':1, 'alpha':.5}
nm_line_props = {'color':color0, 'alpha':0.5}
ax[0].plot(data['sim_time'], data['sim_torques'][0].T, 
    **hum_line_props)
ax[0].plot(data['sim_time'], data['sim_torques'][2].T, 
    **nm_line_props)

ax[1].plot(data['sim_time'], data['sim_torques'][1].T, 
    **hum_line_props)
ax[1].plot(data['sim_time'], data['sim_torques'][3].T, 
    **nm_line_props)

hum_leg_line = lines.Line2D([0], [0], color=color_grey)
nm_leg_line = lines.Line2D([0], [0], color=color0)

ax[0].legend((hum_leg_line, nm_leg_line), ('subject data', 
    'neuromuscular fit'), frameon=False)

title_props = {'weight':'heavy', 'position':(0.5,1.0)}
ax[0].set_title('Knee', **title_props) 
ax[1].set_title('Ankle', **title_props) 

ax[0].set_xlabel('Time (s)')
ax[1].set_xlabel('Time (s)')
ax[0].set_ylabel(r'Moment (\unitfrac{N-m}{kg})')

#turn off all spines and adjust xlim
for axis in ax:
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
    axis.spines['bottom'].set_visible(False)
    axis.spines['left'].set_visible(False)

ax[0].set_yticks(np.arange(-1.5,1.0,0.5))
ax[0].set_xticks(np.arange(0,1.2,0.4))
ax[1].set_xticks(np.arange(0,1.2,0.4))

ax[1].tick_params('y', which='both',length=0)

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

#fig.subplots_adjust(hspace = 1.0, wspace = 0.4)
plt.tight_layout()
fig.savefig('nm_fit.pdf', bbox_inches='tight')
plt.close(fig)
