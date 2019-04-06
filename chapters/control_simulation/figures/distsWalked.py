import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import scipy.io as sio
import matplotlib as mpl
mpl.use("pgf")
import pdb

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

#define colors http://colorschemedesigner.com/csd-3.5/#3B400hWs0dJMP
color0      = '#AA4839'
color0light = '#D4796A'
color1      = '#2A4F6E'
color1light = '#496C89'
color2      = '#81A035'
color2light = '#ABC864'

#load data
intactData = sio.loadmat('distsWalked/intactDists.mat')
intactDists= np.array(intactData['dists']) - 10 
reflexData = sio.loadmat('distsWalked/reflexDists.mat')
reflexDists= np.array(reflexData['dists']) - 10 
impedanceData = sio.loadmat('distsWalked/impedanceDists.mat')
impedanceDists= np.array(impedanceData['dists']) - 10

#filter out nan numbers
mask = np.isnan(intactDists)
intactFiltDists = np.ma.array(intactDists,mask = mask)
intactMedians = np.ma.median(intactFiltDists, axis = 0)
intactDataList = [[y for y in row if y] for row in intactFiltDists.T]
print(intactMedians)

mask = np.isnan(reflexDists)
reflexFiltDists = np.ma.array(reflexDists,mask = mask)
reflexMedians = np.ma.median(reflexFiltDists, axis = 0)
reflexDataList = [[y for y in row if y] for row in reflexFiltDists.T]
print(reflexMedians)

mask = np.isnan(impedanceDists)
impedanceFiltDists = np.ma.array(impedanceDists,mask = mask)
impedanceMedians = np.ma.median(impedanceFiltDists, axis = 0)
impedanceDataList = [[y for y in row if y] for row in impedanceFiltDists.T]
print(impedanceMedians)

#create figure
fig = plt.figure(num = 1, figsize = (4.5,2))
ax1 = plt.axes()

#tick positions
positions = np.arange(0,16,2)
positions0 = positions + 0.4
positions1 = positions 
positions2 = positions - 0.4

#add boxplots
bp0 = ax1.boxplot(intactDataList, notch = False, widths = 0.30, 
    whis = 1.5, patch_artist = True, positions = positions0)
bp1 = ax1.boxplot(reflexDataList, notch = False, widths = 0.30, 
    whis = 1.5, patch_artist = True, positions = positions1)
bp2 = ax1.boxplot(impedanceDataList, notch = False, widths = 0.30, 
    whis = 1.5, patch_artist = True, positions = positions2)

#set box colors
for box0, box1, box2 in zip(bp0['boxes'], bp1['boxes'], bp2['boxes']):
    box0.set_facecolor(color0light)
    box0.set_edgecolor(color0light)
    box1.set_facecolor(color1light)
    box1.set_edgecolor(color1light)
    box2.set_facecolor(color2light)
    box2.set_edgecolor(color2light)

# set medians
for median0, median1, median2 in zip(bp0['medians'], bp1['medians'], 
    bp2['medians']):
    median0.set_visible(False)
    median1.set_visible(False)
    median2.set_visible(False)

# remove outliers
for flier0, flier1, flier2 in zip(bp0['fliers'], bp1['fliers'], bp2['fliers']):
    flier0.set_marker('None')
    flier1.set_marker('None')
    flier2.set_marker('None')

# turn off lines
for cap0, whisker0, cap1, whisker1, cap2, whisker2 in zip(
        bp0['caps'], bp0['whiskers'], 
        bp1['caps'], bp1['whiskers'], 
        bp2['caps'], bp2['whiskers']):
    cap0.set_visible(False)
    whisker0.set_visible(False)
    cap1.set_visible(False)
    whisker1.set_visible(False)
    cap2.set_visible(False)
    whisker2.set_visible(False)

#add lines connecting medians
lineprops = {'linewidth':2,'markeredgecolor':'none','zorder':10}
p0, = ax1.plot(positions0,intactMedians,'o-',color=color0, markersize=4,
    **lineprops)
p1, = ax1.plot(positions1,reflexMedians,'s-',color=color1,markersize=4,
    **lineprops)
p2, = ax1.plot(positions2,impedanceMedians,'^-',color=color2,markersize=5,
    **lineprops)

ax1.xaxis.set_label_text('Ground Roughness (cm)')
ax1.yaxis.set_label_text('Distance Walked (m)')

ax1.legend((p0, p1, p2), ('Intact Model', 'Neuromuscular\nControl', 
    'Impedance\nControl'), frameon = False, loc = 'upper center', ncol = 3,
    bbox_to_anchor =(0.45,1.2))

#set axis properties
ax1.xaxis.set_tick_params(direction = 'out', width = 1)
ax1.yaxis.set_tick_params(direction = 'out', width = 1)
ax1.spines['top'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_visible(False)

#ax1.axis([-1, 15, -10, 95])
ax1.set_xticks(positions1)
ax1.set_xticklabels(positions1)
ax1.set_xlim((-0.75, 14.75))
ax1.set_ylim((0, 100))
ax1.set_yticks(np.arange(0,120,30))

ax = ax1
try:
    ylabelpos_axes = ax.yaxis.get_label().get_position()
    ylabelpos_display = ax.transAxes.transform(ylabelpos_axes)
    ylabelpos_data = inv_data.transform(ylabelpos_display)
    ylabelpos_data[1] = (ax.get_yticks()[0] + ax.get_yticks()[-1])/2.0
    ylabelpos_display = ax.transData.transform(ylabelpos_data)
    ylabelpos_axes = inv_axes.transform(ylabelpos_display)
    ax.yaxis.get_label().set_position(ylabelpos_axes)
except:
    pass

try:
    xlabelpos_axes = ax.xaxis.get_label().get_position()
    xlabelpos_display = ax.transAxes.transform(xlabelpos_axes)
    xlabelpos_data = inv_data.transform(xlabelpos_display)
    xlabelpos_data[0] = (ax.get_xticks()[0] + ax.get_xticks()[-1])/2.0
    xlabelpos_display = ax.transData.transform(xlabelpos_data)
    xlabelpos_axes = inv_axes.transform(xlabelpos_display)
    ax.xaxis.get_label().set_position(xlabelpos_axes)
except:
    pass

plt.savefig('distsWalked.pdf', bbox_inches='tight')
plt.close()
