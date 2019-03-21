import numpy as np
import matplotlib as mpl
from matplotlib import rc
import scipy.io as sio
import scipy.integrate as integrate
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
scale_factor_trip = 202.0/np.max(winter_data[:,1])
scale_factor_walking = 85/56.7

ankle_angle  = winter_data[:,0]
ankle_torque_trip = winter_data[:,1]*scale_factor_trip
ankle_torque_walking = winter_data[:,1]*scale_factor_walking
ankle_vel = winter_data[:,2]


tau_max = 2.3
tau_rated = 0.74
max_speed = 7330
volt_lim_speed = [0, 3570, 6650, max_speed];
volt_lim_tau =   [tau_max, tau_max, tau_rated, 0];
gear_ratio = 100.
eff = 0.75

motor_speed = ankle_vel*gear_ratio/(2*np.pi)*60.
motor_torque_nospring_trip = ankle_torque_trip/gear_ratio/eff
print(np.max(ankle_torque_walking))
print(np.max(np.abs(motor_torque_nospring_trip)))


spring_const = 700.
spring_torque = spring_const*ankle_angle
spring_torque[spring_torque < 0] = 0
motor_torque_spring_trip = (ankle_torque_trip - spring_torque)/gear_ratio/eff

motor_torque_spring_walking = (ankle_torque_walking - spring_torque)/gear_ratio/eff
motor_torque_walking = ankle_torque_walking/gear_ratio/eff

torque_motor_spring_rms = np.sqrt(integrate.cumtrapz(motor_torque_spring_walking**2, x=None, 
    dx = 0.972/69)/0.972)
torque_motor_spring_rms = torque_motor_spring_rms[-1]

torque_motor_rms = np.sqrt(integrate.cumtrapz(motor_torque_walking**2, x=None, 
    dx = 0.972/69)/0.972)
torque_motor_rms = torque_motor_rms[-1]

#create figure
fig, ax = plt.subplots(1,1, figsize = (2,2))

#plot lines
p0, = ax.plot(np.abs(motor_speed), np.abs(motor_torque_nospring_trip),
    linewidth=2, color=color0)
p1, = ax.plot(np.abs(motor_speed), np.abs(motor_torque_spring_trip),
    linewidth=2, color=color1)
p2, = ax.plot([0, max_speed], [torque_motor_rms, torque_motor_rms], '--',
    linewidth=2, color='grey')
p3, = ax.plot([0, max_speed], [torque_motor_spring_rms, torque_motor_spring_rms], '--',
    linewidth=2, color='black')
p4, = ax.plot(volt_lim_speed, volt_lim_tau,
    linewidth=2, color=color2)
p5, = ax.plot([0, max_speed], [tau_rated, tau_rated], zorder=0,linewidth=2, color=color3)


ax.legend((p0, p1, p2, p3, p4, p5), ('Stumble Motor Torque no Spring', 
    'Stumble Motor Torque with Spring', 'Walking Motor RMS Torque no Spring',
    'Walking Motor RMS Torque with Spring', 'Torque Limit', 
    'Motor Rated Torque'), frameon = False, loc = (1,0), handlelength=3)
ax.xaxis.set_label_text('Motor Speed (RPM)')
ax.yaxis.set_label_text('Motor Torque (N-m)')

#set axis properties
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

ax.set_yticks((0, np.round(torque_motor_spring_rms,2), tau_rated, tau_max))
ax.set_xticks((0, volt_lim_speed[1], max_speed))

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

filename = 'ankle_motor_torque_tripping.pdf'
fig.savefig(filename, bbox_inches='tight')
