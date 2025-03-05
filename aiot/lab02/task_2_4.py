import numpy as np
import os.path as osp
import pickle
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.fft import fft, fftfreq

# Radar parameters
c = 3e8           # Speed of light (m/s)
fc = 1e9          # Carrier frequency (Hz) 
B = 1.5e9         # Bandwidth (Hz)
T = 100e-6        # Chirp duration (s)
Fs = 2e6          # Sampling rate (Hz)
NUM_ANTENNAS = 4  # Number of antennas

class task_2_4:
    def __init__(self, data_root="./data/") -> None:
        """
        Initializes the task_2_4 class, loading various signal data from pickle files.

        Attributes:
            data_root (str): The root directory where data files are stored.
            rx_fn (str): Filename for the received signal (task_2_4).
        """
        self.data_root = data_root
        self.rx_fn = "task_2_4.pickle"
        
        
        with open(osp.join(self.data_root, self.rx_fn), "rb") as f:
            self.rx_data = pickle.load(f)
        
        self.num_samples = self.rx_data.shape[1]
        
        
    def generate_transmitted_signal(self):
        r"""
        Generate the transmitted signal based on the received signal.
        
        The chirp signal is defined as:
        \[
            s(t) = \exp\left(j \cdot 2\pi \cdot (f_s \cdot + \dfrac{B}{2 \cdot T} \cdot t)\cdot t\right)
        \]

        
        Returns:
            tx (np.ndarray): The transmitted signal.
        
        >>> task = task_2_4()
        >>> tx = task.generate_transmitted_signal()
        >>> round(tx[-1].imag, 1)
        -0.7
        """

        # >>>>>>>>>>>>>>> YOUR CODE HERE <<<<<<<<<<<<<<<
        # TODO:
        # generate time stamp array
        t = np.linspace(0, T, int(Fs * T), endpoint=False)
        
        # generate the transmitted signal
        tx = np.exp(1j * 2 * np.pi * (fc * t + (B / (2 * T)) * t**2))
        # >>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<

        return tx
    
    def compute_if_signal(self):
        r"""
        Compute the IF signal based on the received signal.
        
        if_signal is given by:
        \[
            if_signal = s(t) \cdot r^*(t)
        \]
        
        Returns:
            if_signal (np.ndarray): The IF signal.
        
        >>> task = task_2_4()
        >>> if_signal = task.compute_if_signal()
        >>> round(if_signal[-1][-1].imag, 1)
        -1.3
        """
        
        tx = self.generate_transmitted_signal()
        if_signal = None
        # >>>>>>>>>>>>>>> YOUR CODE HERE <<<<<<<<<<<<<<<
        # TODO:
        if_signal = tx * np.conjugate(self.rx_data)
        # >>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<
        return if_signal
    
    def estimate_distance(self):
        """
        Estimate the distance based on the IF signal. In this case, there are two targets.
        
        Returns:
            distances (np.ndarray): The estimated distances (m) to the two targets in ascending order.
            range_fft (np.ndarray): The range FFT.
            range_bins (np.ndarray): The range bins corresponding to the range FFT (in meters).
        
        >>> task = task_2_4()
        >>> distances, _, _ = task.estimate_distance()
        >>> len(distances) == 2
        True
        """
        if_signal = self.compute_if_signal()
        distances = None
        range_fft = None # Range FFT
        range_bins = None # Range bins
        # >>>>>>>>>>>>>>> YOUR CODE HERE <<<<<<<<<<<<<<<
        # TODO:
        N = if_signal.shape[-1]
        # compute the FFT
        range_fft = np.fft.fft(if_signal, n=N, axis=-1)
        # compute the magnitude of the FFT
        range_fft_mag = np.abs(range_fft)
        
        # compute the average spectrum
        avg_range_spectrum = np.mean(range_fft_mag, axis=0)
        
        # compute the range bins
        freq_bins = np.arange(N) / N * Fs
        range_bins = (c * freq_bins * T) / (2 * B)
        
        # find the peaks in the average spectrum
        peaks, _ = find_peaks(avg_range_spectrum, height=np.max(avg_range_spectrum) * 0.2)  # take the peaks above 20% of the maximum value
        
        # get the range corresponding to the peaks
        top_peaks = peaks[np.argsort(avg_range_spectrum[peaks])][-2:]
        distances = range_bins[top_peaks]
        # >>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<
        distances = np.sort(distances)
        return distances, range_fft, range_bins
    
    def estimate_AoA(self):
        """
        Estimate the angle of arrival based on the received signal.
        
        Returns:
            aoas (dict): A dictionary containing the estimated AoA for each target. You should keep one decimal place for the angles.
        
        >>> task = task_2_4()
        >>> aoas = task.estimate_AoA()
        >>> len(aoas) == 2, type(aoas) == dict
        (True, True)
        >>> all(isinstance(v, float) for v in aoas.values())
        True
        """
        distances, range_fft, range_bins = self.estimate_distance()
        aoas = {}
        # >>>>>>>>>>>>>>> YOUR CODE HERE <<<<<<<<<<<<<<<
        # TODO:
        # compute the wavelength
        wavelength = c / fc
        # assume the distance to the target is the same
        s = wavelength / 2
        
        # find the top peaks in the range FFT
        top_peaks_idx = []
        for dist in distances:
            # find the index of the range bin closest to the distance
            idx = np.argmin(np.abs(range_bins - dist))
            top_peaks_idx.append(idx)

        # retrieve the AoA for each target
        for i, peak_idx in enumerate(top_peaks_idx):
            # get the range profile for the target
            antenna_values = range_fft[:, peak_idx]
            
            phase_0 = np.angle(antenna_values[0])
            phase_1 = np.angle(antenna_values[1])
            delta_phase = phase_1 - phase_0
            
            # theta = arcsin( (delta_phase * wavelength) / (2*pi*d) )
            theta = np.arcsin((delta_phase * wavelength) / (2 * np.pi * s))
            
            # convert to degrees
            aoa_degree = np.degrees(theta)
            aoas[f"target_{i+1}"] = round(aoa_degree, 1)
        # >>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<
        return aoas