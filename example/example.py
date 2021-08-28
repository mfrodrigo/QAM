
import numpy as np
from scipy.fft import fft, ifft
from qam.qam import QuadratureAmplitudeModulation
from plotter.plotter import Plotter
message = np.random.randint(2, size=8)

qam_modulator = QuadratureAmplitudeModulation(16)
Plotter.plotter_scatter(qam_modulator.constellation[0], qam_modulator.constellation[1])
print(qam_modulator.gray_code)
print(message)
signal, t, pulse = qam_modulator.modulation(message, 1e6, 1e-3, 1e3)
Plotter.plotter_line(t, [signal, pulse])
