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

#load data
ankle_running_data = sio.loadmat('ankle_running.mat')
time          = ankle_running_data['time']
ankle_torque  = ankle_running_data['ankle_torque']
spring_torque = ankle_running_data['spring_torque']
ankle_angle   = ankle_running_data['ankle_angle']
ankle_speed   = ankle_running_data['ankle_speed']
torque_motor  = ankle_running_data['torque_motor']
motor_speed   = ankle_running_data['motor_speed']
torque_motor_rms  = ankle_running_data['torque_motor_rms'][0][0]

tau_max = 2.3
tau_rated = 0.74
volt_lim_speed = [0, 3570, 6650, 7330];
volt_lim_tau =   [tau_max, tau_max, tau_rated, 0];

#create figure
fig = plt.figure(figsize = (2,2))
ax = plt.axes()

#plot lines
p0, = ax.plot(np.abs(motor_speed)/(2*np.pi)*60., np.abs(torque_motor),
    linewidth=2, color=color0)
p1, = ax.plot(volt_lim_speed, volt_lim_tau,
    linewidth=2, color=color1)
p2, = ax.plot([0, 8000], [tau_rated, tau_rated], '--',
    linewidth=2, color=color2)
p3, = ax.plot([0, 8000], [torque_motor_rms, torque_motor_rms], '--',
    linewidth=2, color=color3)

fontsize = ax.xaxis.get_label().get_fontsize()
ax.legend((p0, p1, p2, p3), ('motor torque', 'torque limit', 
    'rated torque', 'RMS motor torque'), frameon = False, loc = (0.0, -.8), fontsize=8,
    handlelength=3)
ax.xaxis.set_label_text('Motor Speed (RPM)')
ax.yaxis.set_label_text('Motor Torque (N-m)')

#set axis properties
ax.xaxis.set_tick_params(direction = 'out', width = 1)
ax.yaxis.set_tick_params(direction = 'out', width = 1)
ax.yaxis.set_tick_params(which='minor', direction = 'out', width = 1)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

ax.axis([-250, 8000, -0.1, 2.6])
ax.spines['left'].set_bounds(0, 2.5)
ax.set_yticks(np.arange(0, 3.75, 1.25))
ax.spines['bottom'].set_bounds(0, 8000)
ax.set_xticks(np.arange(0,12000,4000))

filename = 'ankle_motor_torque_running.pdf'
fig.savefig(filename, bbox_inches='tight')

#create figure
plt.close(fig)
fig = plt.figure(figsize = (2,2))
ax = plt.axes()

#plot lines
p0, = ax.plot(ankle_angle, ankle_torque, linewidth=2, color=color0)
p1, = ax.plot(ankle_angle, spring_torque, linewidth=2, color=color1)
p2, = ax.plot(ankle_angle, ankle_torque-spring_torque, linewidth=2, color=color2)
ax.legend((p0, p1, p2), ('ankle torque', 'spring torque', 
    'net torque'), frameon = False, loc = (0.0, -.7), fontsize=8,
    handlelength=3)

ax.xaxis.set_label_text('Ankle Torque (N-m)')
ax.yaxis.set_label_text('Time (s)')

#set axis properties
ax.xaxis.set_tick_params(direction = 'out', width = 1)
ax.yaxis.set_tick_params(direction = 'out', width = 1)
ax.yaxis.set_tick_params(which='minor', direction = 'out', width = 1)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

ax.axis([-35, 40, -70, 155])
ax.spines['left'].set_bounds(-50, 150)
ax.set_yticks(np.arange(-50, 200, 50))
ax.spines['bottom'].set_bounds(-30, 30)
ax.set_xticks(np.arange(-30,60,30))

#adjust label pos
inv_data = ax.transData.inverted()
inv_axes = ax.transAxes.inverted()

ylabelpos_axes = ax.yaxis.get_label().get_position()
ylabelpos_display = ax.transAxes.transform(ylabelpos_axes)
ylabelpos_data = inv_data.transform(ylabelpos_display)
ylabelpos_data[1] = np.array(ax.spines['left'].get_bounds()).mean()
ylabelpos_display = ax.transData.transform(ylabelpos_data)
ylabelpos_axes = inv_axes.transform(ylabelpos_display)
ax.yaxis.get_label().set_position(ylabelpos_axes)

xlabelpos_axes = ax.xaxis.get_label().get_position()
xlabelpos_display = ax.transAxes.transform(xlabelpos_axes)
xlabelpos_data = inv_data.transform(xlabelpos_display)
xlabelpos_data[0] = np.array(ax.spines['bottom'].get_bounds()).mean()
xlabelpos_display = ax.transData.transform(xlabelpos_data)
xlabelpos_axes = inv_axes.transform(xlabelpos_display)
ax.xaxis.get_label().set_position(xlabelpos_axes)

filename = 'ankle_running_torque_v_angle.pdf'
fig.savefig(filename, bbox_inches='tight')

#create figure
plt.close(fig)
fig = plt.figure(figsize = (2,2))
ax = plt.axes()

#plot lines
p0, = ax.plot(time, ankle_torque, linewidth=2, color=color0)

ax.xaxis.set_label_text('ankle Torque (N-m)')
ax.yaxis.set_label_text('Time (s)')

#set axis properties
ax.xaxis.set_tick_params(direction = 'out', width = 1)
ax.yaxis.set_tick_params(direction = 'out', width = 1)
ax.yaxis.set_tick_params(which='minor', direction = 'out', width = 1)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

ax.axis([-5, 105, -55, 155])
ax.spines['left'].set_bounds(-50, 150)
ax.set_yticks(np.arange(-50, 200, 50))
ax.spines['bottom'].set_bounds(0, 100)
ax.set_xticks(np.arange(0,125,25))

filename = 'ankle_running_torque.pdf'
fig.savefig(filename, bbox_inches='tight')

#create figure
plt.close(fig)
fig = plt.figure(figsize = (2,2))
ax = plt.axes()

#plot lines
markersize = 4
p0, = ax.plot(time, ankle_speed/(2*np.pi), linewidth=2, color=color1)

ax.xaxis.set_label_text('ankle Speed (rev/s)')
ax.yaxis.set_label_text('Time (s)')

#set axis properties
ax.xaxis.set_tick_params(direction = 'out', width = 1)
ax.yaxis.set_tick_params(direction = 'out', width = 1)
ax.yaxis.set_tick_params(which='minor', direction = 'out', width = 1)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

ax.axis([-5, 105, -1.6, 1.6])
ax.spines['left'].set_bounds(-1.5, 1.5)
ax.set_yticks(np.arange(-1.5, 3, 1.5))
ax.spines['bottom'].set_bounds(0, 100)
ax.set_xticks(np.arange(0,125,25))

filename = 'ankle_running_speed.pdf'
fig.savefig(filename, bbox_inches='tight')
