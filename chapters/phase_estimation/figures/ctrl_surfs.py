import numpy as np
import matplotlib as mpl
from matplotlib import rc
import scipy.io as sio
import pdb
mpl.use("pgf")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
from matplotlib import cm
#import omnigraffle

pgf_with_custom_preamble = {
    "pgf.texsystem": "xelatex",
    "font.family": "sans-serif", # use san serif/main font for text elements
    "font.size": 6,
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

colors = np.array(((217., 82., 25.),
                   (0., 114., 189.)))/255;

fig, ax = plt.subplots(2, 3, figsize=(6.5,4), subplot_kw={'projection':'3d'})

with_labels = False
if with_labels:
    ax[1,0].set_xlabel('Phase')
    ax[1,0].set_ylabel('Phase Velocity')

for axes in ax.flatten():
    axes.zaxis.set_rotate_label(False)

ax[0,0].set_zlabel('Knee Angle\n(rad)', rotation=90)
ax[0,1].set_zlabel("Knee Velocity\n"r"(\unitfrac{rad}{s})", rotation=90)
ax[0,2].set_zlabel("Knee Moment\n"r"(\unitfrac{N-m}{kg})", rotation=90)

ax[1,0].set_zlabel('Ankle Angle\n(rad)', rotation=90)
ax[1,1].set_zlabel("Ankle Velocity\n"r"(\unitfrac{rad}{s})", rotation=90)
ax[1,2].set_zlabel("Ankle Moment\n"r"(\unitfrac{N-m}{kg})", rotation=90)

knee_angle_data = sio.loadmat('knee angle_ctrl_plot_data.mat')
knee_velocity_data = sio.loadmat('knee velocity_ctrl_plot_data.mat')
knee_moment_data = sio.loadmat('knee moment_ctrl_plot_data.mat')
ankle_angle_data = sio.loadmat('ankle angle_ctrl_plot_data.mat')
ankle_velocity_data = sio.loadmat('ankle velocity_ctrl_plot_data.mat')
ankle_moment_data = sio.loadmat('ankle moment_ctrl_plot_data.mat')

surf_props = dict(cmap=cm.plasma, alpha=0.5, rstride=1, cstride=1)
#surf_props = dict(color=colors[0,:], alpha=0.5, rstride=1, cstride=1)
wire_props = dict(color='k', alpha=0.5, lw=0.25, rstride=1, cstride=1)
ax[0,0].plot_surface(knee_angle_data['x_test_phase_grid'],
    knee_angle_data['x_test_phase_vel_grid'],
    knee_angle_data['data_predict'], **surf_props)
ax[0,0].plot_wireframe(knee_angle_data['x_test_phase_grid'],
    knee_angle_data['x_test_phase_vel_grid'],
    knee_angle_data['data_predict'], **wire_props)

ax[0,1].plot_surface(knee_velocity_data['x_test_phase_grid'],
    knee_velocity_data['x_test_phase_vel_grid'],
    knee_velocity_data['data_predict'], **surf_props)
ax[0,1].plot_wireframe(knee_velocity_data['x_test_phase_grid'],
    knee_velocity_data['x_test_phase_vel_grid'],
    knee_velocity_data['data_predict'], **wire_props)

ax[0,2].plot_surface(knee_moment_data['x_test_phase_grid'],
    knee_moment_data['x_test_phase_vel_grid'],
    knee_moment_data['data_predict'], **surf_props)
ax[0,2].plot_wireframe(knee_moment_data['x_test_phase_grid'],
    knee_moment_data['x_test_phase_vel_grid'],
    knee_moment_data['data_predict'], **wire_props)

ax[1,0].plot_surface(ankle_angle_data['x_test_phase_grid'],
    ankle_angle_data['x_test_phase_vel_grid'],
    ankle_angle_data['data_predict'], **surf_props)
ax[1,0].plot_wireframe(ankle_angle_data['x_test_phase_grid'],
    ankle_angle_data['x_test_phase_vel_grid'],
    ankle_angle_data['data_predict'], **wire_props)

ax[1,1].plot_surface(ankle_velocity_data['x_test_phase_grid'],
    ankle_velocity_data['x_test_phase_vel_grid'],
    ankle_velocity_data['data_predict'], **surf_props)
ax[1,1].plot_wireframe(ankle_velocity_data['x_test_phase_grid'],
    ankle_velocity_data['x_test_phase_vel_grid'],
    ankle_velocity_data['data_predict'], **wire_props)

ax[1,2].plot_surface(ankle_moment_data['x_test_phase_grid'],
    ankle_moment_data['x_test_phase_vel_grid'],
    ankle_moment_data['data_predict'], **surf_props)
ax[1,2].plot_wireframe(ankle_moment_data['x_test_phase_grid'],
    ankle_moment_data['x_test_phase_vel_grid'],
    ankle_moment_data['data_predict'], **wire_props)

#human_line_props = dict(linewidth=0.5, color=colors[1,:], alpha=0.75)
human_line_props = dict(linewidth=0.5, color='k', alpha=0.75)
num_hum_steps = knee_angle_data['phase'].shape[1]

for i in range(num_hum_steps):
    ax[0,0].plot(knee_angle_data['phase'][:,i], 
        knee_angle_data['phase_vel'][:,i], 
        knee_angle_data['data_hum'][:,i], **human_line_props)
    ax[0,1].plot(knee_velocity_data['phase'][:,i], 
        knee_velocity_data['phase_vel'][:,i], 
        knee_velocity_data['data_hum'][:,i], **human_line_props)
    ax[0,2].plot(knee_moment_data['phase'][:,i], 
        knee_moment_data['phase_vel'][:,i], 
        knee_moment_data['data_hum'][:,i], **human_line_props)

    ax[1,0].plot(ankle_angle_data['phase'][:,i], 
        ankle_angle_data['phase_vel'][:,i], 
        ankle_angle_data['data_hum'][:,i], **human_line_props)
    ax[1,1].plot(ankle_velocity_data['phase'][:,i], 
        ankle_velocity_data['phase_vel'][:,i], 
        ankle_velocity_data['data_hum'][:,i], **human_line_props)
    ax[1,2].plot(ankle_moment_data['phase'][:,i], 
        ankle_moment_data['phase_vel'][:,i], 
        ankle_moment_data['data_hum'][:,i], **human_line_props)

for i, axes in enumerate(ax.flatten()):
    axes.grid(b=False)
    axes.zaxis._axinfo['juggled'] = (0,2,1)
    axes.view_init(elev=30, azim=225)
    axes.set_xlim((0,1))
    axes.set_ylim((0,1.5))
    axes.set_xticks([0, 0.5, 1.0])
    axes.set_yticks([0, 0.75, 1.5])
    if with_labels:
        axes.set_xticklabels([0, 0.5, 1.0], ha='left', va='center', rotation=-40)
        axes.set_yticklabels([0, 0.75, 1.5], ha='right', va='center', rotation=40)
        if i != 3:
            [label.set_visible(False) for label in axes.get_xticklabels()]
            [label.set_visible(False) for label in axes.get_yticklabels()]
    else:
        [label.set_visible(False) for label in axes.get_xticklabels()]
        [label.set_visible(False) for label in axes.get_yticklabels()]
        [label.set_visible(False) for label in axes.get_zticklabels()]
    for dirc in ['x', 'y', 'z']:
        getattr(axes, dirc+'axis').set_pane_color((1.0, 1.0, 1.0, 0.0))
        #getattr(axes, dirc+'axis').line._visible = False
        getattr(axes, dirc+'axis').line._color = [0.9, 0.9, 0.9]
        getattr(axes, dirc+'axis')._axinfo['grid']['color'] = [0.9, 0.9, 0.9]


#center all axis labels in bounds

for axis in ax.flatten():
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

    try:
        zlabelpos_axes = axis.zaxis.get_label().get_position()
        zlabelpos_display = axis.transAxes.transform(zlabelpos_axes)
        zlabelpos_data = inv_data.transform(zlabelpos_display)
        zlabelpos_data[1] = (axis.get_zticks()[0] + axis.get_zticks()[-1])/2.0
        zlabelpos_display = axis.transData.transform(zlabelpos_data)
        zlabelpos_axes = inv_axes.transform(zlabelpos_display)
        axis.zaxis.get_label().set_position(zlabelpos_axes)
    except:
        pass


fig.subplots_adjust(hspace = 0.1, wspace = 0.5, bottom = 0.15, top = 0.95,
    right = 0.95, left=0.1)
#new bounds fig/plt.tight_layout()

fig.canvas.draw()  # the angles of the text are calculated here

for i, axes in enumerate(ax.flatten()):
    labels = [label._text for label in axes.get_zticklabels()]
    axes.set_zticklabels(labels, ha='right', va='center')

if with_labels:
    fig.savefig('ctrl_surfs.pdf')
else:
    fig.savefig('ctrl_surfs_no_ticks.pdf')
plt.close(fig)
