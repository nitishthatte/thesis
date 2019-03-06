winter_data = dlmread('winter_data_angle_torque.csv', ',', 1, 0)
tau = winter_data(1:end-1,2);
t_end = 0.958;

period= t_end/67;
time = (0:period:t_end)'

figure(1)
plot(time, tau)

%power spectral density

Fs = 1/period;
N = length(tau);

xdft = fft(tau)

xdft = xdft(1:N/2+1);
psdx = (1/(Fs*N)) * abs(xdft).^2;
psdx(2:end-1) = 2*psdx(2:end-1);
freq = 0:Fs/N:Fs/2;

figure(2)
plot(freq,10*log10(psdx))
grid on
title('Periodogram Using FFT')
xlabel('Frequency (Hz)')
ylabel('Power/Frequency (dB/Hz)')

figure(3)
plot(freq,psdx)
grid on
title('Periodogram Using FFT')
xlabel('Frequency (Hz)')
ylabel('Power/Frequency (dB/Hz)')

power_int = cumtrapz(psdx);
power_int_percent = power_int/power_int(end);

index = find(power_int_percent > 0.9)
frq_cut = freq(index(1))
