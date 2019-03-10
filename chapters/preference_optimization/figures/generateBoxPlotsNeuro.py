import numpy as np
import matplotlib as mpl
from matplotlib import rc
import scipy.io as sio
import scipy.stats as stats
import pdb
mpl.use("pgf")
import matplotlib.pyplot as plt

pgf_with_custom_preamble = {
    "pgf.texsystem": "xelatex",
    "font.family": "sans-serif", # use san serif/main font for text elements
    "text.usetex": True,    # use inline math for ticks
    "pgf.rcfonts": False,   
    "font.size": 8,
    "pgf.preamble": [
        r"\usepackage{amsmath}",
        r"\usepackage{fontspec}",
        r"\setmainfont{Avenir Next}",
        r"\setsansfont{Avenir Next}",
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

#load data
plot_data = sio.loadmat('plot_data_neuromuscular.mat')

min_dim = 2
max_dim = 3
num_dims = max_dim - min_dim + 1
num_trials = 10
num_iter = 50

y_err_pes = []
y_err_ei = []
y_err_rand = []
for i in np.arange(min_dim-1,max_dim):
    y_err_pes.append(plot_data['y_errs_vs_iter'][i][0][0])
    y_err_ei.append(plot_data['y_errs_vs_iter'][i][0][1]) 
    y_err_rand.append(plot_data['y_errs_vs_iter'][i][0][2]) 

y_errs_pes_median = []
y_errs_ei_median = []
y_errs_rand_median = []
for i in np.arange(0, num_dims):
    y_errs_pes_median.append(np.median(y_err_pes[i],0))
    y_errs_ei_median.append(np.median(y_err_ei[i],0))
    y_errs_rand_median.append(np.median(y_err_rand[i],0))

#tick positions
positions = np.arange(0,num_iter+5,5)
iters_to_plot = positions - 1
iters_to_plot[0] = 0
positions0 = positions - 1
positions1= positions
positions2= positions + 1

#create figure
for i in np.arange(0, num_dims):
    fig = plt.figure(num = i, figsize = (1.75,1.25))
    ax = plt.axes()
    data_median_pes  = y_errs_pes_median[i][iters_to_plot]
    data_median_ei   = y_errs_ei_median[i][iters_to_plot]
    data_median_rand = y_errs_rand_median[i][iters_to_plot]
    data_pes  = y_err_pes[i][:,iters_to_plot]
    data_ei   = y_err_ei[i][:,iters_to_plot]
    data_rand = y_err_rand[i][:,iters_to_plot]

    sig_indicator = np.empty(iters_to_plot.shape)
    sig_indicator[:] = np.NaN
    j = 0
    for (iter_num, data_pes_iter, data_ei_iter, 
        data_rand_iter) in zip(iters_to_plot, data_pes.T, data_ei.T, 
        data_rand.T):
    
        _, pval_pes_vs_rand = stats.mannwhitneyu(data_pes_iter,
            data_rand_iter, alternative='two-sided')

        _, pval_pes_vs_ei = stats.mannwhitneyu(data_pes_iter,
            data_ei_iter, alternative='two-sided')

        if pval_pes_vs_rand < 0.05 and pval_pes_vs_ei < 0.05:
            sig_indicator[j] = 1
        j = j + 1

    markersize = 4
    trans = mpl.transforms.blended_transform_factory(ax.transData, ax.transAxes)
    s0, = ax.plot(iters_to_plot, sig_indicator, '*', color='k', 
        markeredgecolor = 'none', markersize=markersize-1, transform=trans, 
        clip_on=False)

    #add lines connecting medians
    p0, = ax.plot(positions0, data_median_pes,'o-',linewidth=1, color=color0,
        markeredgecolor = 'none',markersize=markersize-1, zorder=10)
    p1, = ax.plot(positions1, data_median_ei,'^-',linewidth=1, color=color1,
        markeredgecolor = 'none',markersize=markersize, zorder=10)
    p2, = ax.plot(positions2, data_median_rand,'*-',linewidth=1, color=color2,
        markeredgecolor = 'none',markersize=markersize, zorder=10)

    ax.xaxis.set_label_text('Number of Queries', color='white')
    ax.yaxis.set_label_text('Immediate Regret', color='white')

    #add boxplots
    bp0= ax.boxplot(data_pes, notch = False, widths = 1,  
        patch_artist = True, positions = positions0)
    bp1= ax.boxplot(data_ei, notch = False, widths = 1, 
        patch_artist = True, positions = positions1)
    bp2= ax.boxplot(data_rand, notch = False, widths = 1, 
        patch_artist = True, positions = positions2)

    #set box colors
    for box0, box1, box2 in zip(bp0['boxes'], bp1['boxes'], bp2['boxes']):
        box0.set_facecolor(color0light)
        box0.set_edgecolor('none')
        box1.set_facecolor(color1light)
        box1.set_edgecolor('none')
        box2.set_facecolor(color2light)
        box2.set_edgecolor('none')

    # set medians
    for median0, median1, median2 in zip(bp0['medians'], bp1['medians'], 
        bp2['medians']):
        median0.set_visible(False)
        median1.set_visible(False)
        median2.set_visible(False)

    # remove outliers
    for flier0, flier1, flier2 in zip(bp0['fliers'], bp1['fliers'],
        bp2['fliers']):
        flier0.set_marker('None')
        flier1.set_marker('None')
        flier2.set_marker('None')

    # turn off lines
    for cap0, whisker0, cap1, whisker1, cap2, whisker2 in zip(
        bp0['caps'], bp0['whiskers'], bp1['caps'], bp1['whiskers'], 
        bp2['caps'], bp2['whiskers']): 
        cap0.set_visible(False)
        whisker0.set_visible(False)
        cap1.set_visible(False)
        whisker1.set_visible(False)
        cap2.set_visible(False)
        whisker2.set_visible(False)

    #set axis properties
    ax.set_yscale('log')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.yaxis.set_tick_params(which='minor', direction = 'out', width = 0)

    ax.set_xlim((-2.5,52.5))
    if i == 0:
        ax.set_ylim((0.01,10))
        ax.set_yticks([0.01, 0.1, 1, 10])
        ax.set_yticklabels([0.01, 0.1, 1, 10])
    elif i == 1:
        ax.set_ylim((0.1,10))
        ax.set_yticks([0.1, 1, 10])
        ax.set_yticklabels([0.1, 1, 10])

    xtickloc = np.arange(0,75,25)
    xtickloc = xtickloc - 1
    xtickloc[0] = 0
    ax.set_xticks(xtickloc)
    ax.set_xticklabels(xtickloc+1)

    #adjust y label pos
    #ylabelpos = ax.yaxis.get_label().get_position()
    #ylabelpos = (ylabelpos[0], ylabelpos[1] + .04)
    #ax.yaxis.get_label().set_position(ylabelpos)

    plt.tight_layout()
    filename = 'y_err' + str(i+2) + 'Neuro.pdf'
    plt.savefig(filename, bbox_inches=None)
    fig.clear()
