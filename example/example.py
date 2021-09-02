import numpy as np
from scipy.fft import fft, fftfreq, ifft
from qam.qam import QuadratureAmplitudeModulation
from plotter.plotter import Plotter

message = np.random.randint(2, size=65536)

qam_modulator = QuadratureAmplitudeModulation(16)
Plotter.plotter_scatter(qam_modulator.constellation[0], qam_modulator.constellation[1])
print(qam_modulator.gray_code)
# message = np.array([
#     0, 0, 0, 0,
#     0, 0, 0, 1,
#     0, 0, 1, 1,
#     0, 0, 1, 0,
#     0, 1, 1, 0,
#     0, 1, 1, 1,
#     0, 1, 0, 1,
#     0, 1, 0, 0,
#     1, 1, 0, 0,
#     1, 1, 0, 1,
#     1, 1, 1, 1,
#     1, 1, 1, 0,
#     1, 0, 1, 0,
#     1, 0, 1, 1,
#     1, 0, 0, 1,
#     1, 0, 0, 0
# ])
# message = np.array([0, 0, 0, 1, 1, 0, 1, 1])
print(message)
t, pulse = qam_modulator._build_signal_message(message, 10e3, 1e6)
# Plotter.plotter_line(t, pulse)
qam_signal = qam_modulator.modulation(t, message, 20e3)
fft_qam_signal = fft(qam_signal)[:len(qam_signal) // 2]
fs = fftfreq(len(qam_signal), 1 / 1e6)[:len(qam_signal) // 2]
# Plotter.plotter_line(fs, np.abs(fft_qam_signal))
# Plotter.plotter_line(t, [qam_signal, pulse])
# add noise in signal
qam_signal = qam_modulator.add_noise(qam_signal, -5)
fft_qam_signal = fft(qam_signal)[:len(qam_signal) // 2]
fs = fftfreq(len(qam_signal), 1 / 1e6)[:len(qam_signal) // 2]
# Plotter.plotter_line(fs, np.abs(fft_qam_signal))
# Plotter.plotter_line(t, [qam_signal, pulse])
# demodulation signal
amplitude_phase, amplitude_quadrature = qam_modulator.demodulation(t, 10e3, 1e6, 20e3, qam_signal)
Plotter.plotter_scatter(amplitude_phase, amplitude_quadrature)

# decode
decode_message = qam_modulator.decode(amplitude_phase, amplitude_quadrature)
print(decode_message)
print(np.sum(np.abs(np.array(decode_message)-message)))