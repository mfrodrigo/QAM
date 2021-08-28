"""
Class with methods for M-query Quadrature Amplitude Modulation (QAM).
"""
from math import log2, sqrt, sin, cos, pi

import numpy as np
from sympy.combinatorics.graycode import GrayCode


class QuadratureAmplitudeModulation:
    """

    """

    def __init__(self, number_symbol):
        self.number_symbol = number_symbol
        self.number_bits = int(log2(number_symbol))
        self.gray_code = list(GrayCode(self.number_bits).generate_gray())
        self.constellation = None
        self.start_constellation()

    def start_constellation(self):
        L = int(sqrt(self.number_symbol))
        ai = list(np.arange(-L + 1, L + 1, 2)) * L
        bi = list(np.repeat(np.arange(L - 1, -L - 1, -2), L))
        self.constellation = [ai, bi]

    def convert_to_grey_value(self, message):
        message = list(map(str, message))
        grey_values = []
        for i in range(0, len(message), self.number_bits):
            grey_values.append(''.join(message[i:i + self.number_bits]))

        return grey_values

    def modulation(self, message, sampling_rate, bit_time, central_frequency):
        rest_of_division = len(message) % self.number_bits
        if not rest_of_division == 0:
            message = [0] * rest_of_division + message

        grey_values = self.convert_to_grey_value(message)
        t = np.arange(0, bit_time * len(grey_values) - 1 / sampling_rate, 1 / sampling_rate)
        signal = np.zeros(len(t))
        step = int(bit_time * sampling_rate)
        t1 = 0
        for values in grey_values:
            index = self.gray_code.index(values)
            signal[t1:t1 + step] = self.constellation[0][index] * np.cos(
                2 * pi * central_frequency * t[t1:t1 + step]) + \
                                   self.constellation[1][index] * np.sin(
                2 * pi * central_frequency * t[t1:t1 + step])
            t1 += step
        pulse = np.repeat(message, int(bit_time * sampling_rate) / 4)
        return signal, t, pulse
