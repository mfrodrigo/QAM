import numpy as np
from scipy.fft import fft, ifft
from qam.qam import QuadratureAmplitudeModulation
from plotter.plotter import Plotter

# message = np.random.randint(2, size=8)

qam_modulator = QuadratureAmplitudeModulation(16)
Plotter.plotter_scatter(qam_modulator.constellation[0], qam_modulator.constellation[1])
print(qam_modulator.gray_code)
message = np.array([
    0, 0, 0, 0,
    0, 0, 0, 1,
    0, 0, 1, 1,
    0, 0, 1, 0,
    0, 1, 1, 0,
    0, 1, 1, 1,
    0, 1, 0, 1,
    0, 1, 0, 0,
    1, 1, 0, 0,
    1, 1, 0, 1,
    1, 1, 1, 1,
    1, 1, 1, 0,
    1, 0, 1, 0,
    1, 0, 1, 1,
    1, 0, 0, 1,
    1, 0, 0, 0
])
print(message)
t, pulse = qam_modulator._build_signal_message(message, 10e3, 1e6)
Plotter.plotter_line(t, pulse)
qam_signal = qam_modulator.modulation(t, message, 1e3)
Plotter.plotter_line(t, [qam_signal, pulse])
