from matplotlib.markers import TICKDOWN
import matplotlib.transforms as transforms
import numpy as np
import pdb

def add_barplot_sigstars(ax, condition_combs, pvalues, max_data):

    yloc = 1.1
    linewidth = 1
    color = 'k'
    trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)

    line_props = {'color':color, 'linewidth':linewidth , 'marker':TICKDOWN, 
        'markeredgewidth':linewidth, 'markersize':3, 'transform':trans, 
        'clip_on':False}
    asterisk_props = {'color':color, 'horizontalalignment':'center', 
        'verticalalignment':'center', 'fontsize':10, 'transform':trans,
        'clip_on':False}


    #add significane test resutls
    num_comps = pvalues.shape[0]
    if num_comps == 3:
        if pvalues[0] < 0.05 and pvalues[2] < 0.05:
            xloc = np.array(([0, 0.9], [0, 2], [1.1, 2]))
        else:
            xloc = np.array(([0, 1], [0, 2], [1, 2]))
        yloc = np.array([1.1, 1.2, 1.1])
    elif num_comps == 1:
        xloc = np.array([[0, 1]])
        yloc = np.array([1.1])

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

