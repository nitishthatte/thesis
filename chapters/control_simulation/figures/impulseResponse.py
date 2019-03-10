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

def center_ylabel(axbnds, ytickbnds, axis):
    axrange = (axbnds[-1] - axbnds[0])/2
    newmdpt = (ytickbnds[-1] + ytickbnds[0])/2 - axbnds[0]
    ylabelpos = (-0.175, 0.5*newmdpt/axrange)
    axis.yaxis.set_label_coords(ylabelpos[0], ylabelpos[1])

def shift_axes(axis, shift):
    axpos_old = axis.get_position()
    axpos_new = [axpos_old.x0, axpos_old.y0 + shift, axpos_old.width, axpos_old.height]
    axis.set_position(axpos_new)

#plot boxplots
refImpulseData = sio.loadmat('reflexTrip.mat')
impImpulseData = sio.loadmat('impedanceTrip.mat')

refDisturbedBallPos = refImpulseData['RBallPosDisturbed']['signals'][0][0][0][0]['values']
refDisturbedTime    = refImpulseData['RBallPosDisturbed']['time'][0][0]

refUndisturbedBallPos = refImpulseData['RBallPosUndisturbed']['signals'][0][0][0][0]['values']
refUndisturbedTime    = refImpulseData['RBallPosUndisturbed']['time'][0][0]

impDisturbedBallPos = impImpulseData['RBallPosDisturbed']['signals'][0][0][0][0]['values']
impDisturbedTime    = impImpulseData['RBallPosDisturbed']['time'][0][0]

impUndisturbedBallPos = impImpulseData['RBallPosUndisturbed']['signals'][0][0][0][0]['values']
impUndisturbedTime    = impImpulseData['RBallPosUndisturbed']['time'][0][0]

#set times
tbuffer = 0.2

ref_start = 10.026
ref_end = 10.593
refT0 = ref_start - tbuffer
refT1 = ref_end + tbuffer
refImpulseT1 = ref_start + 0.05*(ref_end - ref_start)

imp_start = 9.401
imp_end = 10.062
impT0 = imp_start - tbuffer;
impT1 = imp_end + tbuffer;
impImpulseT1 = imp_start + 0.05*(imp_end - imp_start)

#Size of impulse Box 
refImpulsePos = refDisturbedBallPos[np.logical_and(refDisturbedTime > refImpulseT1,
    refDisturbedTime < (refImpulseT1 + 0.01))[:,0], :]
refDisturbedBallPos = refDisturbedBallPos[np.logical_and(refDisturbedTime > refT0, 
    refDisturbedTime < refT1)[:,0],:] 
refUndisturbedBallPos = refUndisturbedBallPos[np.logical_and(refUndisturbedTime > refT0, 
    refUndisturbedTime < refT1)[:,0], :]

impImpulsePos = impDisturbedBallPos[np.logical_and(impDisturbedTime > impImpulseT1,
    impDisturbedTime < (impImpulseT1 + 0.01))[:,0], :]
impDisturbedBallPos   = impDisturbedBallPos[np.logical_and(impDisturbedTime > impT0, 
    impDisturbedTime < impT1)[:,0],:] 
impUndisturbedBallPos = impUndisturbedBallPos[np.logical_and(impUndisturbedTime > impT0, 
    impUndisturbedTime < impT1)[:,0], :]

#make x values relative to begining
refX1 = refUndisturbedBallPos[0,0]
refDisturbedBallPos[:,0]   = refDisturbedBallPos[:,0]   - refX1
refUndisturbedBallPos[:,0] = refUndisturbedBallPos[:,0] - refX1
refImpulsePos[:,0] = refImpulsePos[:,0] - refX1

impX1 = impUndisturbedBallPos[0,0]
impDisturbedBallPos[:,0]   = impDisturbedBallPos[:,0]   - impX1
impUndisturbedBallPos[:,0] = impUndisturbedBallPos[:,0] - impX1
impImpulsePos[:,0] = impImpulsePos[:,0] - impX1

''' plot reflex controller'''
fig, ax = plt.subplots(2,1, sharex = True, figsize=(3,2.5))

p11, = ax[0].plot(refUndisturbedBallPos[:,0],refUndisturbedBallPos[:,2],'k--',linewidth=2)
p12, = ax[0].plot(refDisturbedBallPos[:,0],refDisturbedBallPos[:,2],'k',linewidth=2)
ax[0].legend((p11, p12), ('Undisturbed', 'Disturbed'), frameon = False, 
    loc=(0.4,0.9), fontsize = 10)

'''plot impedance controller'''
p21, = ax[1].plot(impUndisturbedBallPos[:,0],impUndisturbedBallPos[:,2],'k--',linewidth=2)
p22, = ax[1].plot(impDisturbedBallPos[:,0],impDisturbedBallPos[:,2],'k',linewidth=2)

axis_lims = [-0.25, 2.5, -0.05, 0.3]
for axis in ax:
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
    axis.spines['bottom'].set_visible(False)
    axis.spines['left'].set_visible(False)
    axis.axis(axis_lims)
    axis.yaxis.set_label_text('Y Position (m)')
    axis.set_yticks(np.arange(0, 0.60, 0.3))


ax[0].tick_params('x', which='both',length=0)
ax[1].set_xticks(np.arange(0.0, 3.0, 1.0))
ax[1].xaxis.set_label_text('X Position (m)')

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

fig.tight_layout()
plt.savefig('impulseResponse.pdf', bbox_inches='tight', transparent=True)
