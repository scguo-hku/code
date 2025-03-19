from scipy.signal import butter, sosfiltfilt
from scipy.signal import savgol_filter
from scipy.signal import find_peaks
from scipy.fft import fft, fftfreq
from hampel import hampel
import numpy as np
import os.path as osp
import pickle
import matplotlib.pyplot as plt

class task_4_3:
    def __init__(self, data_root="./data/"):
        data_p = osp.join(data_root, "task_4_3.pickle")
        with open(data_p, 'rb') as f:
            data = pickle.load(f)
        self.am_signal = data['am_signal']
        self.imu_signal = data['imu_signal']
        self.fs = data['fs']
        self.fc = data['fc']
    
    def get_freq(self, s, fs):
        """
        Calculate the dominant frequency of the signal.

        Parameters:
            s (numpy.ndarray): 1D array.
            fs (float): Sampling frequency in Hz

        Returns:
            numpy.ndarray: 1D array of the dominant frequency in Hz. You should return the dominant two frequencies in ascending order. 
            If there is only one dominant frequency, you should return the same frequency twice.
        
        >>> task = task_4_3()
        >>> s = np.sin(2*np.pi*10*np.linspace(0, 1, 1000))
        >>> frequency = task.get_freq(s, 1000)
        >>> frequency != None
        array([ True,  True])
        >>> len(frequency) == 2
        True
        >>> np.subtract(frequency[-1], 10) < 1e-6
        True
        >>> s = np.sin(2*np.pi*10*np.linspace(0, 1, 1000)) + np.sin(2*np.pi*20*np.linspace(0, 1, 1000))
        >>> frequency = task.get_freq(s, 1000)
        >>> frequency != None
        array([ True,  True])
        >>> len(frequency) == 2
        True
        >>> np.subtract(frequency[-1], 20) < 1e-6
        True
        """
        frequency = []
        # >>>>>>>>>>>>>>> YOUR CODE HERE <<<<<<<<<<<<<<<
        # TODO:
        # compute FFT
        fft_values = fft(s)
        fft_freqs = fftfreq(len(s), 1/fs)

        # compute positive frequencies
        positive_freqs = fft_freqs[:len(fft_freqs)//2]
        positive_fft_values = np.abs(fft_values[:len(fft_values)//2])

        # find peaks
        peaks, _ = find_peaks(positive_fft_values)

        # if the number of peaks is less than 2, return the same frequency twice
        if len(peaks) < 2:
            dominant_freqs = np.array([positive_freqs[peaks[0]], positive_freqs[peaks[0]]])
        else:
            peak_indices = np.argsort(positive_fft_values[peaks])[-2:]
            dominant_freqs = positive_freqs[peaks][peak_indices]
            dominant_freqs = np.sort(dominant_freqs)
        # >>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<
        frequency = np.array(dominant_freqs, dtype=np.float64)
        return frequency
        
    def demodulate_signal(self, s, fs, fc):
        """
        Demodulate an amplitude-modulated (AM) signal to extract the message signal.

        Parameters:
            s (numpy.ndarray): 1D array of the input AM signal
            fs (float): Sampling frequency in Hz
            fc (float): Carrier frequency in Hz

        Input:
            The signal s should contain a low-frequency message (e.g., 10 Hz) modulated onto
            a higher-frequency carrier (fc), with possible noise. Length should match fs*t_duration.

        Returns:
            numpy.ndarray: 1D array of the demodulated and normalized message signal.
        
        >>> task = task_4_3()
        >>> message = task.demodulate_signal(task.am_signal, task.fs, task.fc)
        >>> len(message) == len(task.am_signal)
        True
        >>> np.mean(message) - 0 < 1e-6
        True
        >>> freq = task.get_freq(message, task.fs)
        >>> np.subtract(freq[-1], 10) < 1e-6
        True
        """
        demo_signal = None
        # >>>>>>>>>>>>>>> YOUR CODE HERE <<<<<<<<<<<<<<<
        # TODO:
        # generate carrier signal
        t = np.arange(len(s)) / fs
        carrier = np.cos(2 * np.pi * fc * t)

        # multiply the signal with the carrier signal
        mixed_signal = s * carrier

        # apply low-pass filter
        cutoff = 10
        sos = butter(5, cutoff, btype='lowpass', fs=fs, output='sos')

        # apply the filter
        demodulated_signal = sosfiltfilt(sos, mixed_signal)

        # remove the DC component
        demodulated_signal -= np.mean(demodulated_signal)

        # normalize the signal
        demodulated_signal /= np.max(np.abs(demodulated_signal))
        # >>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<
        demo_signal = np.array(demodulated_signal, dtype=np.float64)
        return demo_signal
    

    
    def interpolate_signal(self, s):
        """
        Interpolate missing data points (NaN) in an IMU signal using linear interpolation.

        Parameters:
            s (numpy.ndarray): 1D array of the input signal

        Input:
            The signal s represents accelerometer data with gaps (NaNs)

        Returns:
            numpy.ndarray: 1D array of the interpolated signal, same length as input,
                           with NaN values replaced by linearly interpolated values based
                           on nearest valid neighbors.
                           
        >>> task = task_4_3()
        >>> interpolated_signal = task.interpolate_signal(task.imu_signal)
        >>> len(interpolated_signal) == len(task.imu_signal)
        True
        >>> np.isnan(interpolated_signal).sum() == 0
        True
        >>> np.subtract(interpolated_signal[1], 0.221) < 1e-3
        True
        >>> np.subtract(interpolated_signal[998], -0.311) < 1e-3
        True
        """
        interpolated_signal = None
        # >>>>>>>>>>>>>>> YOUR CODE HERE <<<<<<<<<<<<<<<
        # TODO: 
        # find the indices of non-NaN values
        not_nan_indices = np.where(~np.isnan(s))[0]
        # find the indices of NaN values
        nan_indices = np.where(np.isnan(s))[0]

        # interpolate the NaN values
        interpolated_signal = np.copy(s)
        interpolated_signal[nan_indices] = np.interp(nan_indices, not_nan_indices, s[not_nan_indices])
        # >>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<
        interpolated_signal = np.array(interpolated_signal, dtype=np.float64)
        return interpolated_signal
    
    def apply_filter(self, s, fs):
        """
        Smooth an IMU signal using a Butterworth low-pass filter to remove high-frequency noise.

        Parameters:
            s (numpy.ndarray): 1D array of the input signal.
            fs (float): Sampling frequency in Hz

        Input:
            The signal s should be a continuous IMU signal (e.g., after interpolation).

        Returns:
            numpy.ndarray: 1D array of the smoothed signal, same length as input.
        
        >>> task = task_4_3()
        >>> filtered_signal = task.apply_filter(task.imu_signal, task.fs)
        >>> len(filtered_signal) == len(task.imu_signal)
        True
        >>> freq = task.get_freq(filtered_signal, task.fs)
        >>> np.subtract(freq[-1], 1) < 1e-6
        True
        
        """
        interpolated_signal = self.interpolate_signal(s)
        filtered_signal = None
        # >>>>>>>>>>>>>>> YOUR CODE HERE <<<<<<<<<<<<<<<
        # TODO:
        cutoff = 2  # cutoff frequency
        sos = butter(5, cutoff, btype='lowpass', fs=fs, output='sos')

        # apply the filter
        filtered_signal = sosfiltfilt(sos, interpolated_signal)
        # >>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<
        filtered_signal = np.array(filtered_signal, dtype=np.float64)
        return filtered_signal
        
    