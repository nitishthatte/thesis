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
    "font.size": 10,
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
winter_data = np.loadtxt(open("winter_data_angle_torque.csv","rb"),
    delimiter=",",skiprows=1)
scale_factor = 80/56.7
walking_torque = winter_data[:,1]*scale_factor

spring_const = 700
spring_torque = spring_const*winter_data[:,0]
spring_torque[spring_torque < 0] = 0
actuator_torque = scale_factor*winter_data[:,1] - spring_torque

spring_torque_angles = np.array([-20, 0, 10])
spring_torque_plot = np.array([0, 0, spring_const*10*np.pi/180])

gear_torque = 107

#create figure
fig, ax = plt.subplots(1,1, figsize = (2,2))

#add lines connecting medians
markersize = 4
p0, = ax.plot(winter_data[:,0]*180/np.pi, walking_torque,
    linewidth=2, color=color0)
p1, = ax.plot(spring_torque_angles, spring_torque_plot, linewidth=2, 
    color=color1)
p2, = ax.plot(winter_data[:,0]*180/np.pi, actuator_torque, linewidth=2, 
    color=color2)
p3 = ax.axhline(y=gear_torque, xmin=0, xmax=1, ls='--', linewidth=2, color=color3)

ax.legend((p0, p1, p2, p3), ('Ankle Torque', 'Spring Torque', 'Actuator Torque',
    'Gear Set Repeated Torque Limit'), frameon = False, loc = (-0.4, -.8),
    fontsize=8, handlelength=3)

ax.xaxis.set_label_text('Angle (deg)')
ax.yaxis.set_label_text('Torque (N-m)')

#set axis properties
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

ax.set_xticks(np.arange(-20, 20, 10))
ax.set_yticks([0, 50, gear_torque, np.round(np.max(walking_torque))])

inv_data = ax.transData.inverted()
inv_axes = ax.transAxes.inverted()

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

filename = 'ankle_torque_vs_angle_ups.pdf'
fig.savefig(filename, bbox_inches='tight')
