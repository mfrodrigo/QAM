import numpy as np
from scipy.fft import fft, fftfreq, ifft
from qam.qam import QuadratureAmplitudeModulation
from plotter.plotter import Plotter

message = np.random.randint(2, size=65536)
SNR = np.arange(0, 30, 5)
QAM = np.array([4, 16, 64, 256])
BER = []
for M in QAM:
    qam_modulator = QuadratureAmplitudeModulation(M)
    t, pulse, message = qam_modulator._build_signal_message(message, 10e3, 1e6)
    for snr in SNR:
        qam_signal = qam_modulator.modulation(t, message, 20e3)
        qam_signal = qam_modulator.add_noise(qam_signal, snr)
        amplitude_phase, amplitude_quadrature = qam_modulator.demodulation(t, 10e3, 1e6, 20e3, qam_signal)
        decode_message = qam_modulator.decode(amplitude_phase, amplitude_quadrature)
        rest_of_division = len(message) % qam_modulator.number_bits
        BER.append((np.sum(np.abs(decode_message-message)))/len(message)*100)

print(BER)