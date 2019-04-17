import numpy as np
import scipy.io as sio
import pdb

data = sio.loadmat('torque_tracking_plot_data.mat', squeeze_me=True)

step_num = 10


idx = data['time_pros_stride'][step_num] > data['toeoff_time'][step_num] 
max_knee_swing_torque = np.max(np.abs(
    data['knee_torque_measured_stride'][step_num][idx]))
max_ankle_swing_torque = np.max(np.abs(
    data['ankle_torque_measured_stride'][step_num][idx]))

print(max_knee_swing_torque)
print(max_ankle_swing_torque)
print(5.7/max_knee_swing_torque)
print(10.89/max_ankle_swing_torque)
