mass = 80; %mass of person
gear_eff = 0.75;
gear_ratio = 100;

t_switch = 40; %end of stance, %cycle
t_end = 100;
t_cycle = 0.7;

%load ankle data
load('ankle_moment_running.mat')
torque = ankle_moment_running;
load('ankle_angle_running.mat')
angle = ankle_angle_running;
speed = gradient(angle(:,2),angle(:,1))*(pi/180)*(t_end/t_cycle);
speed_poly = polyfit(angle(:,1), speed, 10);

time =  linspace(0,t_end,10*t_end+1)';
ankle_torque = spline(torque(:,1), torque(:,2), time)*mass;
ankle_angle  = spline(angle(:,1),  angle(:,2),  time);
ankle_speed = polyval(speed_poly, time);

time =  linspace(0,t_end,10*t_end+1)';

ups_stiffness = 140/30;
spring_torque = ankle_angle*ups_stiffness.*(ankle_angle > 0)

figure(1)
plot(ankle_angle,ankle_torque,ankle_angle,spring_torque, ...
    ankle_angle,ankle_torque-spring_torque)
ylabel('Ankle Torque [N-m]')
xlabel('Ankle Angle (deg)')

figure(2)
plot(torque(:,1),torque(:,2)*mass,'o',time,ankle_torque)
ylabel('ankle Torque [N-m]')
xlabel('% Gait Cycle')

figure(3)
plot(angle(:,1)*t_cycle/100, speed/(2*pi), 'o', time*t_cycle/100,ankle_speed/(2*pi))
ylabel('ankle Speed [rev/s]')
xlabel('Time [s]')

%calculate motor rms torque
torque_motor = (ankle_torque - spring_torque)/gear_ratio/gear_eff; %motor torque in N-m after gear reduction and inefficiency
torque_motor_rms = sqrt(cumtrapz(time,torque_motor.^2)/t_end); 
torque_motor_rms = torque_motor_rms(end);

motor_speed = ankle_speed*gear_ratio; %speed of motor in rad/s

%motor parameters: ilm-85x13 HS SP
tau_max = 2.3;
tau_rated = 0.74;
V_max = 48;
kt = 0.065;
R = 0.0525;

Vlim_n = [0, 3570, 6650, 7330];
Vlim_t = [tau_max, tau_max, tau_rated, 0];

fprintf('Max motor torque = %f N-m\n',max(abs(torque_motor)))
fprintf('Motor RMS torque = %f N-m\n',torque_motor_rms)
fprintf('Max motor torque = %f N-m\n',max(ankle_speed))

figure(4)
plot(abs(motor_speed/(2*pi)*60),abs(torque_motor))
hold all
plot(Vlim_n,Vlim_t)
plot([0, 8000], [tau_rated, tau_rated],'--')
plot([0, 8000], [torque_motor_rms, torque_motor_rms],'-.')
hold off
legend('Speed-Torque Trajectory','Voltage Limit','Motor Rated Torque','rms(Torque)','Location','EastOutside')

ylim([0 tau_max*1.1])

xlabel('abs(Motor Speed) [rpm]')
ylabel('abs(Motor Torque) [N-m]')

save('ankle_running.mat', 'ankle_torque', 'ankle_angle', 'spring_torque', ...
    'time', 'ankle_speed', 'motor_speed', 'torque_motor', 'torque_motor_rms')
