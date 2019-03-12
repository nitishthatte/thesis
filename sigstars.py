from matplotlib.markers import TICKDOWN
import matplotlib.transforms as transforms
import numpy as np
import pdb

def add_barplot_sigstars(ax, condition_combs, pvalues, xloc, sig_space=0.1,
    linewidth=1, color='k', star_loc='stacked'):

    trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)

    line_props = {'color':color, 'linewidth':linewidth , 'marker':TICKDOWN, 
        'markeredgewidth':linewidth, 'markersize':3, 'transform':trans, 
        'clip_on':False}
    asterisk_props = {'color':color, 'horizontalalignment':'center', 
        'verticalalignment':'center', 'fontsize':10, 'transform':trans,
        'clip_on':False}

    #add significane test resutls
    num_comps = pvalues.shape[0]


    if star_loc == 'stacked':
        xloc = xloc[condition_combs]
        y_bottom = 1.1
        yloc = np.linspace(y_bottom, y_bottom+sig_space*(num_comps-1), num_comps)
    if star_loc == '3x3':
        if pvalues[0] < 0.05 and pvalues[2] < 0.05:
            x01 = [0, 0.9]
            x12 = [1.1, 2]
        else:
            x01 = [0, 1]
            x12 = [1, 2]

        if pvalues[3] < 0.05 and pvalues[5] < 0.05:
            x34 = [4, 4.9]
            x45 = [5.1, 6]
        else:
            x34 = [4, 5]
            x45 = [5, 6]
        xloc = np.array((x01, [0, 2], x12, x34, [4, 6], x45, [0, 4], [1, 5], 
            [2, 6]))
        yloc = 1.1 + sig_space*np.array((0, 1, 0, 0, 1, 0, 2, 3, 4))
    if star_loc == 'level':
        xloc = xloc[condition_combs]
        yloc = 1.1*np.ones((xloc.shape[0], 1))

    for i, comp in enumerate(condition_combs):
        if pvalues[i] < 0.05:
            if pvalues[i] < 0.05:
                sig_asterisk = '*'
            if pvalues[i] < 0.01:
                sig_asterisk = '**'
            if pvalues[i] < 0.001:
                sig_asterisk = '***'

            ax.text((xloc[i,:].mean()), yloc[i]+0.02, sig_asterisk,
                **asterisk_props)
            ax.plot(xloc[i,:],[yloc[i], yloc[i]], '-', **line_props)

