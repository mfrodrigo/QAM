import numpy as np
from math import pi
from scipy import signal
from scipy.fft import fft, fftfreq, ifft
from plotter.plotter import Plotter

t = 1 / 1e6
N = 80
T = np.linspace(0.0, N * t, N, endpoint=False)
fc = 20e3
freq_s = 1e6
y = 2 * np.sin(2 * pi * fc * T) + 2 * np.cos(2 * pi * fc * T)
fft_qam_signal = fft(y)[:len(y) // 2]
fs = fftfreq(N, t)[:len(y) // 2]
Plotter.plotter_line(fs, np.abs(fft_qam_signal))

b, a = signal.butter(1, 8 * fc / freq_s, btype='low', analog=False)

y = y * np.sin(2 * pi * fc * T)
fft_qam_signal = fft(y)[:len(y) // 2]

Plotter.plotter_line(fs, np.abs(fft_qam_signal))
Plotter.plotter_line(T, y)
y = signal.lfilter(b, a, y)
fft_qam_signal = fft(y)[:len(y) // 2]
Plotter.plotter_line(T, y)
Plotter.plotter_line(fs, np.abs(fft_qam_signal))
