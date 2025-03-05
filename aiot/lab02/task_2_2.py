import numpy as np
import os.path as osp
import pickle
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.fft import fft, fftfreq

class task_2_2:
    def __init__(self, data_root="./data/") -> None:
        """
        Initializes the task_2_2 class, loading various signal data from pickle files.

        Attributes:
            data_root (str): The root directory where data files are stored.
            spt_fn (str): Filename for the sum of pure tone signals (task_2_2_1).
            chirp_fn (str): Filename for the chirp signal (task_2_2_2).
            ecg_fn (str): Filename for the ECG signal (task_2_2_3).
            spt_data (dict): Loaded data for the sum of pure tone signals.
            chirp_data (dict): Loaded data for the chirp signal.
            ecg_data (dict): Loaded data for the ECG signal.
        """
        self.data_root = data_root
        self.spt_fn = "task_2_2_1.pickle"
        self.chirp_fn = "task_2_2_2.pickle"
        self.ecg_fn = "task_2_2_3.pickle"
        
        with open(osp.join(self.data_root, self.spt_fn), "rb") as f:
            self.spt_data = pickle.load(f)
        with open(osp.join(self.data_root, self.chirp_fn), "rb") as f:
            self.chirp_data = pickle.load(f)
        with open(osp.join(self.data_root, self.ecg_fn), "rb") as f:
            self.ecg_data = pickle.load(f)
        
    def get_freq_spt(self):
        """
        Analyze the sum of pure tone signals to determine the primary frequency components.

        Returns:
            freq (np.float64): An array of the three primary frequency components in descending order.
        
        >>> test = task_2_2()
        >>> f = test.get_freq_spt()
        >>> len(f) == 3
        True
        """
        s_t = self.spt_data["values"] # signal values
        fs = self.spt_data["fs"] # sampling frequency
        
        freq = np.zeros(3, dtype=np.float64) # (3,)
        
        # >>>>>>>>>>>>>>> YOUR CODE HERE <<<<<<<<<<<<<<<
        # TODO:
         # compute the frequency spectrum of the signal
        s_f = fft(s_t)
        s_f_len = len(s_f)
        s_f_freq = fftfreq(s_f_len, d=1/fs)
        s_f = np.abs(s_f[:s_f_len//2])
        s_f_freq = s_f_freq[:s_f_len//2]
        
        # find the peaks in the frequency spectrum
        peaks, _ = find_peaks(s_f)
        
        # get the frequency and magnitude of the peaks
        peak_freqs = s_f_freq[peaks]
        peak_mags = s_f[peaks]
        
        # sort the peaks in descending order of magnitude
        sorted_indices = np.argsort(peak_mags)[::-1]
        primary_freqs = peak_freqs[sorted_indices][:3]
        
        # ensure the output is of type float64
        freq = np.array(primary_freqs).astype(np.float64)
        # >>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<
        
        freq = np.sort(freq)[::-1]
        freq = np.squeeze(freq[:3]).astype(np.float64)
        return freq
    
    def get_bw_chirp(self):
        """
        Compute the bandwidth of the chirp signal.

        Returns:
            bw (float64): The bandwidth of the chirp signal in Hz. Format: float64.
            
        >>> test = task_2_2()
        >>> bw = test.get_bw_chirp()
        >>> (bw >= 100) & (bw <= 1000)
        True
        """
        s_t = self.chirp_data["values"] # signal values
        fs = self.chirp_data["fs"] # sampling frequency
        
        bw = 0
        
        # >>>>>>>>>>>>>>> YOUR CODE HERE <<<<<<<<<<<<<<<
        # TODO:
        # compute the frequency spectrum of the signal
        s_f = fft(s_t)
        s_f_len = len(s_f)
        s_f_freq = fftfreq(s_f_len, d=1/fs)
        s_f = np.abs(s_f[:s_f_len//2])
        s_f_freq = s_f_freq[:s_f_len//2]
        
        # find the peaks in the frequency spectrum
        threshold = np.max(s_f) * 0.01  # find peaks above 1% of the maximum value
        significant_indices = np.where(s_f > threshold)[0]
        if len(significant_indices) > 0:
            bw = s_f_freq[significant_indices[-1]] - s_f_freq[significant_indices[0]]
        else:
            bw = 0
        
        # ensure the output is of type float64
        bw = np.float64(bw)
        # >>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<
        
        return bw 
    
    def get_heart_rate(self):
        """
        Determine the heart rate from the ECG signal.

        Returns:
            hr (float64): The heart rate in beats per minute (BPM).
        
        >>> test = task_2_2()
        >>> hr = test.get_heart_rate()
        >>> (hr >= 60) & (hr <= 90)
        True
        """
        s_t = self.ecg_data["values"] # signal values
        fs = self.ecg_data["fs"] # sampling frequency
        
        hr = 0
        
        # >>>>>>>>>>>>>>> YOUR CODE HERE <<<<<<<<<<<<<<<
        # TODO:
        # find the peaks in the ECG signal
        peaks, _ = find_peaks(s_t, distance=fs/2)  # set the minimum distance
        
        # calculate
        peak_intervals = np.diff(peaks) / fs  # calculate the time intervals between peaks
        avg_peak_interval = np.mean(peak_intervals)  # calculate the average peak interval
        hr = 60 / avg_peak_interval  # calculate the heart rate
        # >>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<
        
        # Make sure hr is a float64
        if isinstance(hr, np.ndarray):
            if hr.size > 1:
                hr = hr[0]
            hr = hr.item()
        if isinstance(hr, list):
            if len(hr) > 1:
                hr = hr[0]
        hr = float(hr)
        return hr

if __name__ == "__main__":
    data_root = "./data/" # Change this to the directory where you store the data
    test = task_2_2(data_root=data_root)
    # ...