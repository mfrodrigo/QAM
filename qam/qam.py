"""
Class with methods for M-query Quadrature Amplitude Modulation (QAM).
"""
from math import log2, sqrt, sin, cos, pi
from scipy.fft import fft, fftfreq, ifft
from scipy import signal
import numpy as np
from sympy.combinatorics.graycode import GrayCode
from plotter.plotter import Plotter


class QuadratureAmplitudeModulation:
    """

    """

    def __init__(self, number_symbol):
        self.number_symbol = number_symbol
        self.number_bits = int(log2(number_symbol))
        self.gray_code = list(GrayCode(self.number_bits).generate_gray())
        self.constellation = None
        self.L = None
        self.start_constellation()

    def start_constellation(self):
        self.L = int(sqrt(self.number_symbol))
        ai = list(np.arange(-self.L + 1, self.L + 1, 2)) * self.L
        bi = list(np.repeat(np.arange(self.L - 1, -self.L - 1, -2), self.L))
        self.constellation = [ai, bi]

    def convert_to_grey_value(self, message):
        message = list(map(str, message))
        grey_values = []
        for i in range(0, len(message), self.number_bits):
            grey_values.append(''.join(message[i:i + self.number_bits]))
        return grey_values

    def _build_signal_message(self, message, bit_rate, sampling_rate):
        rest_of_division = len(message) % self.number_bits
        if not rest_of_division == 0:
            list_of_zeros = ([0] * (self.number_bits - rest_of_division))
            list_of_zeros.extend(message)
            message = np.array(list_of_zeros)
        bit_time = 1 / bit_rate
        pulse = np.repeat(message, int(bit_time * sampling_rate))
        return np.linspace(0, len(pulse) / sampling_rate, len(pulse), endpoint=False), pulse, message

    def modulation(self, t, message, central_frequency):
        grey_values = self.convert_to_grey_value(message)
        step = int(len(t) * self.number_bits / len(message))
        index_list = []
        for values in grey_values:
            index_list.append(self.gray_code.index(values))
        phase_amplitude = np.array([self.constellation[0][i] for i in index_list])
        phase_amplitude = np.repeat(phase_amplitude, step)
        quadrature_amplitude = np.array([self.constellation[1][i] for i in index_list])
        quadrature_amplitude = np.repeat(quadrature_amplitude, step)
        qam_phase = phase_amplitude * np.cos(2 * pi * central_frequency * t)
        qam_quadrature = quadrature_amplitude * np.sin(2 * pi * central_frequency * t)
        signal = qam_phase + qam_quadrature
        return signal

    @staticmethod
    def add_noise(signal, SNR):
        signal_watts = signal ** 2
        signal_average_watts = np.mean(signal_watts)
        signal_average_dB = 10*np.log10(signal_average_watts)
        noise_average_db = signal_average_dB - SNR
        noise_average_watts = 10 ** (noise_average_db / 10)
        noise_volts = np.random.normal(0, sqrt(noise_average_watts), len(signal))
        return signal + noise_volts

    def demodulation(self, t, bit_rate, sampling_frequency, central_frequency, qam_signal):
        number_points_per_bit = int(sampling_frequency * self.number_bits / bit_rate)
        b, a = signal.butter(1, 4 * central_frequency / sampling_frequency, btype='low', analog=False)
        qam_phase = qam_signal * 2 * np.cos(2 * pi * central_frequency * t)
        qam_phase = signal.lfilter(b, a, qam_phase)
        qam_quadrature = qam_signal * 2 * np.sin(2 * pi * central_frequency * t)
        qam_quadrature = signal.lfilter(b, a, qam_quadrature)
        amplitude_phase = []
        amplitude_quadrature = []
        for i in range(0, len(qam_signal), number_points_per_bit):
            amplitude_phase.append(np.mean(qam_phase[i:i + number_points_per_bit]))
            amplitude_quadrature.append(np.mean(qam_quadrature[i:i + number_points_per_bit]))

        return np.array(amplitude_phase), np.array(amplitude_quadrature)

    def return_closest(self, number):
        value_set = np.arange(-self.L + 1, self.L + 1, 2)
        return value_set[np.argmin(np.abs(value_set-number))]

    def decode(self, amplitude_phase, amplitude_quadrature):
        constellation = list(zip(self.constellation[0], self.constellation[1]))
        vfunc = np.vectorize(self.return_closest)
        amplitude_phase = (vfunc(amplitude_phase)).astype('int32')
        amplitude_quadrature = (vfunc(amplitude_quadrature)).astype('int32')
        amplitude_message = list(zip(list(amplitude_phase), list(amplitude_quadrature)))
        decode_message = []
        for bit in amplitude_message:
            index = constellation.index(bit)
            decode_message = decode_message + [int(i) for i in self.gray_code[index]]

        return decode_message