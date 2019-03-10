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
    "text.usetex": True,    # use inline math for ticks
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
color0dark  = '#2F537C'
color1      = '#BAD55E'
color1light = '#E3F6A2'
color1dark  = '#9BB53F'
color2      = '#A0468F'
color2light = '#EA9ADB'
color2dark  = '#882F77'
color3      = '#DFAE62'
color3light = '#F8D6A3'
color3dark  = '#BE8D42'

#load data
pes_data = sio.loadmat('pes_data.mat')
x_grid = pes_data['x_grid_1']
true_func = pes_data['true_func'].transpose()
mu_cond = pes_data['mu_cond']
std_cond = pes_data['std_cond']
mu_cond_xstar_list = pes_data['mu_cond_xstar_list'][0]
x_star_list = pes_data['x_star_list'].flatten()
sample_points = pes_data['sample_points'].flatten()
sample_points[3] = sample_points[3] - 0.02
sample_values = pes_data['sample_values'].flatten()

fig = plt.figure(figsize = (2,2))
ax1 = fig.add_subplot(211)
ax1.plot(x_grid, true_func, color = color2)
ax1.plot(x_grid, mu_cond, color = color0)
lower_bnd = (mu_cond-std_cond).flatten()
upper_bnd = (mu_cond+std_cond).flatten()
ax1.fill_between(x_grid.flatten(), lower_bnd, upper_bnd, facecolor=color0light, 
    alpha=0.5, edgecolor='none')
for i in np.arange(0,4,2):
    ax1.plot(sample_points[i:i+2], sample_values[i:i+2], '-o', 
    color = color3, markeredgecolor = 'none', markersize=3)

ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.xaxis.set_ticks_position('none')
ax1.yaxis.set_ticks_position('none')
ax1.set_xticklabels([], visible=False)
ax1.set_yticklabels([], visible=False)
ax1.axis([-1, 1, -1.5, 1.5])
ax1.text(1.1, 1.4, 'a')

label_size = 8
ax1.text(sample_points[0]+0.03, sample_values[0]+0.00, r'$\mathsf{x_1^a}$',
    fontsize=label_size)
ax1.text(sample_points[1]-0.15, sample_values[1]-0.5,  r'$\mathsf{x_1^b}$',
    fontsize=label_size)
ax1.text(sample_points[2]+0.00, sample_values[2]+0.2,  r'$\mathsf{x_2^a}$',
    fontsize=label_size)
ax1.text(sample_points[3]+0.00, sample_values[3]+0.2,  r'$\mathsf{x_2^b}$',
    fontsize=label_size)

ax1.annotate("",
            xy=(-1, 1.5), xycoords='data',
            xytext=(-1, -1.4), textcoords='data',
            arrowprops=dict(arrowstyle='-|>', fc='k'),
            )
ax1.text(-1, 1.5, 'f', ha='center')

ax2 = fig.add_subplot(212)
ax2.plot(x_grid, mu_cond, color = color0)
for i in range(2):
    ax2.plot(x_grid, mu_cond_xstar_list[i][0:-1], color = color1)
    ax2.plot(x_star_list[i], mu_cond_xstar_list[i][-1], '*', color = color1,
        markeredgecolor = 'none')

ax2.plot(sample_points[4:6], sample_values[4:6], '-o', 
    color = color3, markeredgecolor = 'none', markersize=3)

ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.xaxis.set_ticks_position('none')
ax2.yaxis.set_ticks_position('none')
ax2.set_xticklabels([], visible=False)
ax2.set_yticklabels([], visible=False)
ax2.axis([-1, 1, -1.5, 1.5])
ax2.text(1.1, 1.4, 'b')

ax2.text(sample_points[4]+0.00, sample_values[4]+0.2, r'$\mathsf{x_3^b}$',
    fontsize=label_size)
ax2.text(sample_points[5]+0.00, sample_values[5]+0.2, r'$\mathsf{x_3^a}$',
    fontsize=label_size)

ax2.text(x_star_list[0]+0.01, mu_cond_xstar_list[0][-1] + 0.2, r'$\mathsf{x_1^*}$',
    fontsize=label_size)
ax2.text(x_star_list[1]-0.15, mu_cond_xstar_list[1][-1] + 0.25, r'$\mathsf{x_2^*}$',
    fontsize=label_size)


ax2.annotate("",
            xy=(-1, 1.5), xycoords='data',
            xytext=(-1, -1.65), textcoords='data',
            arrowprops=dict(arrowstyle='-|>', fc='k'),
            )

ax2.annotate("",
            xy=(1, -1.5), xycoords='data',
            xytext=(-1.0225, -1.5), textcoords='data',
            arrowprops=dict(arrowstyle='-|>', fc='k'),
            )

ax2.text(-1, 1.5, 'f', ha='center')
ax2.text(1, -1.5, 'x', va='center')

filename = 'pes_plot.pdf'
fig.savefig(filename, bbox_inches='tight')
