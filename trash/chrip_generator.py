import matplotlib.pyplot as plt
import numpy as np


# -------------------------------------------------------------------------#
#             THIS CLASS GENERATE THE CHRIP JUST LIKE FMCW RADAR           #
# -------------------------------------------------------------------------#
class FMCWChirpGenerator:
    def __init__(self, fc=60e9, B=4e9, T_chirp=1e-3, fs=20e6):
        """
        FMCW Chirp Generator
        :param fc: Carrier frequency (Hz)
        :param B: Chirp bandwidth (Hz)
        :param T_chirp: Chirp duration (seconds)
        :param fs: Sampling frequency (Hz)
        """
        self.fc = fc
        self.B = B
        self.T_chirp = T_chirp
        self.fs = fs
        self.k = B / T_chirp

    def generate_chirp(self):
        """
        Generate one FMCW chirp signal (complex baseband)
        :return: t (time axis), signal (complex IQ samples)
        """
        N = int(self.T_chirp * self.fs)
        t = np.linspace(0, self.T_chirp, N, endpoint=False)
        # Baseband chirp (complex)
        phase = 2 * np.pi * (0.5 * self.k * t**2)
        signal = np.exp(1j * phase)
        return t, signal

    def plot_time_domain(self, t, signal):
        plt.figure(figsize=(8, 3))
        plt.plot(t * 1e3, np.real(signal), label="I (Real)")
        plt.plot(t * 1e3, np.imag(signal), label="Q (Imag)")
        plt.title("FMCW Chirp Time-Domain Signal")
        plt.xlabel("Time (ms)")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_spectrum(self, signal):
        N = len(signal)
        # FFT and frequency axis
        spectrum = np.fft.fftshift(np.fft.fft(signal))
        freqs = np.fft.fftshift(np.fft.fftfreq(N, d=1 / self.fs))
        plt.figure(figsize=(8, 3))
        plt.plot(freqs / 1e6, 20 * np.log10(np.abs(spectrum)))
        plt.title("FMCW Chirp Spectrum")
        plt.xlabel("Frequency (MHz)")
        plt.ylabel("Magnitude (dB)")
        plt.tight_layout()
        plt.show()


# -------------------------------------------------------------------------#
#                           EXAMPLE OF USAGE                               #
# -------------------------------------------------------------------------#

# # Example usage with parameters inspired by the Mendeley dataset (60 GHz radar)
# generator = FMCWChirpGenerator(fc=60e9, B=4e9, T_chirp=1e-3, fs=20e6)
# t, chirp_signal = generator.generate_chirp()

# # Plotting
# # generator.plot_time_domain(t, chirp_signal)
# generator.plot_spectrum(chirp_signal)
