import matplotlib.pyplot as plt
import numpy as np

from chrip_generator import FMCWChirpGenerator


# -------------------------------------------------------------------------#
#            THIS PART SIMULATE THE VITAL SIGN SIGNALS FOR FMCW            #
# -------------------------------------------------------------------------#
class VitalSignSimulator:
    def __init__(self, chirp_gen: FMCWChirpGenerator, fs=2000, duration=5):
        self.chirp_gen = chirp_gen
        self.fs = fs
        self.duration = duration
        self.c = 3e8

    def _generate_motion(self):
        t = np.linspace(0, self.duration, int(self.fs * self.duration))
        resp_rate = np.random.uniform(12, 20) / 60
        heart_rate = np.random.uniform(60, 100) / 60
        resp = 7e-3 * np.sin(2 * np.pi * resp_rate * t)
        heart = 0.5e-3 * np.sin(2 * np.pi * heart_rate * t)
        disp = resp + heart
        return t, disp, resp_rate * 60, heart_rate * 60

    def generate_vital_sign_signal(self):
        t_disp, disp, resp_bpm, hr_bpm = self._generate_motion()
        t_chirp, base_chirp = self.chirp_gen.generate_chirp()
        lambda_c = self.c / self.chirp_gen.fc
        n_chirps = int(self.duration / self.chirp_gen.T_chirp)
        iq_matrix = np.zeros((n_chirps, len(base_chirp)), dtype=complex)
        for i in range(n_chirps):
            idx = min(int(i * self.chirp_gen.T_chirp * self.fs), len(disp) - 1)
            d = disp[idx]
            phase_shift = np.exp(1j * (4 * np.pi / lambda_c) * d)
            iq_matrix[i, :] = base_chirp * phase_shift
        return {
            "time_disp": t_disp,
            "disp": disp,
            "resp_bpm": resp_bpm,
            "hr_bpm": hr_bpm,
            "chirp_time": t_chirp,
            "iq_matrix": iq_matrix,
        }


# -------------------------------------------------------------------------#
#                           EXAMPLE OF USAGE                               #
# -------------------------------------------------------------------------#

# Recreate the chirp generator
# chirp_gen = FMCWChirpGenerator(fc=60e9, B=4e9, T_chirp=1e-3, fs=20e6)
# # Simulate and plot
# sim = VitalSignSimulator(chirp_gen)
# data = sim.generate_vital_sign_signal()

# plt.figure(figsize=(8, 3))
# plt.plot(data["time_disp"], data["disp"] * 1e3)
# plt.title(
#     f"Chest Displacement (Resp: {data['resp_bpm']:.1f} BPM, Heart: {data['hr_bpm']:.1f} BPM)"
# )
# plt.xlabel("Time (s)")
# plt.ylabel("Displacement (mm)")
# plt.tight_layout()
# plt.show()

# plt.figure(figsize=(8, 3))
# plt.plot(data["chirp_time"] * 1e3, np.abs(data["iq_matrix"][0]))
# plt.title("Magnitude of First Chirp with Vital Motion Phase Shift")
# plt.xlabel("Time (ms)")
# plt.ylabel("Amplitude")
# plt.tight_layout()
# plt.show()
