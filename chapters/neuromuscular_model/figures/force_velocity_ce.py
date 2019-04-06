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
        r"\setsansfont{Avenir Next}",
        r"\setmainfont{Times}",
    ]
}
mpl.rcParams.update(pgf_with_custom_preamble)


#define colors http://colorschemedesigner.com/csd-3.5/#3B400hWs0dJMP
color0      = '#476A92'
color0light = '#9EC0E7'
color1      = '#BAD55E'
color1light = '#E3F6A2'
color2      = '#A0468F'
color2light = '#EA9ADB'
color3      = '#DFAE62'
color3light = '#F8D6A3'

K = 5
N = 1.5
sigma_ce_neg = np.linspace(-1, 0) #normalized fiver length
sigma_ce_pos = np.linspace( 0, 1) #normalized fiver length
fv_neg = (1 + sigma_ce_neg)/(1 - K*sigma_ce_neg)
fv_pos = N + (N - 1)*(1 - sigma_ce_pos)/(-7.56*K*sigma_ce_pos - 1)

#create figure
fig = plt.figure(figsize = (2,2))
ax = plt.axes()

#add lines connecting medians
markersize = 4
p0, = ax.plot(sigma_ce_neg, fv_neg, linewidth=2, color=color1)
p1, = ax.plot(sigma_ce_pos, fv_pos, linewidth=2, color=color1)

ax.set_title('CE Force-Velocity', y=1.08)
ax.xaxis.set_label_text('Velocity')
ax.yaxis.set_label_text('Force Multiplier')

#set axis properties
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

ax.axis([-1.2, 1.1, -0.15, 1.6])
ax.set_yticks([0, 1, N])
ax.set_yticklabels(['0', 1, 'N'])

ax.set_xticks(np.arange(-1,2,1))
ax.set_xticklabels(['$\mathsf{v_{max}}$', '0', '$\mathsf{|v_{max}|}$'])

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

filename = 'force_velocity_ce.pdf'
fig.savefig(filename, bbox_inches='tight')
