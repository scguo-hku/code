import numpy as np
from vis import *

class task_1_1:
    def __init__(self, fs=1000):
        """
        Initialize the class with a specific sampling rate.

        Args:
            fs (int): Sampling rate in Hz. Defaults to 1000Hz.
        """
        self.fs = fs
    
    # TODO: Implement this function
    def generate_signal_1(self):
        """
        Generate the first signal: a pure tone with a specified frequency and phase offset.

        Returns:
            numpy.array: Array of timestamps in seconds. Data type must be float.
            numpy.array: Array of generated signal values. Data type must be float.

        Note:
            - The returned signal array must strictly be of type float.

        Example:
            >>> gen = task_1_1(1000)
            >>> t, s_t = gen.generate_signal_1()
            >>> np.round(t[10], 5), np.round(s_t[10], 5)
            (-0.99, 0.6046)
        """
        
        # >>>>>>>>>>>>>>> YOUR CODE HERE <<<<<<<<<<<<<<<
         # set the frequency and phase offset
        f = 2  # 2 Hz
        phi = np.pi / 6  # π/6

        # generate the time stamps
        t = np.linspace(-1, 1, int(2 * self.fs), endpoint=False)

        # generate the signal
        s_t = 1 * np.sin(2 * np.pi * f * t + phi)
        # >>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<
        s_t = np.array(s_t).astype(float)
        t = np.array(t).astype(float)
        return t, s_t

    def p_tau(self, t, tau, tau_0, offset=0):
            """
            Defines the pulse signal p_tau(t). 
            It will repeat every tau_0 seconds.

            Parameters:
            t (numpy array): Time array.
            tau (float): Pulse width.
            tau_0 (float): Total period of the signal.

            Returns:
            numpy array: The pulse signal values.
            """
            period = np.floor((t + tau_0 / 2 - offset) / tau_0) * tau_0
            t_adjusted = t - period - offset
            return np.where(np.abs(t_adjusted) < tau / 2, 1, 0)
    
    # TODO: Implement this function
    def generate_signal_2(self):
        """
        Generate the second signal: a combination of rectangle and triangle waves.

        Returns:
            numpy.array: Array of timestamps in seconds. Data type must be float.
            numpy.array: Array of generated signal values. Data type must be float.

        Note:
            - The returned signal array must strictly be of type float.

        Example:
            >>> gen = task_1_1(1000)
            >>> t, s_t = gen.generate_signal_2()
            >>> np.round(t[10], 5), np.round(s_t[10], 5)
            (-0.99, 0.0)
        """
        
        # >>>>>>>>>>>>>>> YOUR CODE HERE <<<<<<<<<<<<<<<
        # generate the time stamps
        t = np.linspace(-1, 1, int(2 * self.fs), endpoint=False)

        # generate the rectangular wave
        rect_wave = self.p_tau(t, 0.4, 2, offset=-0.5)  # generate a rectangular wave with width 0.4 and period 2

        # generate the triangular wave
        tri_wave = np.zeros_like(t)
        t_mod = np.mod(t + 1, 2) - 1
        tri_wave[(t_mod >= 0.3) & (t_mod < 0.5)] = (t_mod[(t_mod >= 0.3) & (t_mod < 0.5)] - 0.3) / 0.2
        tri_wave[(t_mod >= 0.5) & (t_mod < 0.7)] = (0.7 - t_mod[(t_mod >= 0.5) & (t_mod < 0.7)]) / 0.2

        # combine the two waves
        s_t = rect_wave + tri_wave
        # >>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<
        s_t = np.array(s_t).astype(float)
        t = np.array(t).astype(float)
        return t, s_t
        
    # TODO: Implement this function
    def generate_signal_3(self):
        """
        
        Generate the third signal: a complex signal based on real and imaginary parts.

        Returns:
            numpy.array: Array of timestamps in seconds. Data type must be float.
            numpy.array: Array of generated complex signal values. Data type must be np.complex64.

        Note:
            - The returned signal array must strictly be of type np.complex64.
            
        Example:
            >>> gen = task_1_1(1000)
            >>> t, s_t = gen.generate_signal_3()
            >>> np.round(t[10], 5), np.round(s_t[10], 5)
            (-0.99, (0.99211+0.12533j))
        """
        
        # >>>>>>>>>>>>>>> YOUR CODE HERE <<<<<<<<<<<<<<<
        # generate the time stamps
        t = np.linspace(-1, 1, int(2 * self.fs), endpoint=False)

        # set the frequency
        f_1 = 2  #2 Hz

        # generate the complex signal
        s_t = np.exp(2 * np.pi * 1j * f_1 * t)
        # >>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<
        s_t = np.array(s_t).astype(np.complex64)
        t = np.array(t).astype(float)
        return t, s_t
    
    def visualize(self):
        # Generate the first signal
        t, s_t = self.generate_signal_1()
        plot1D_single(t, s_t, '1-1', 'Time (s)', 'Amplitude')
        
        # Generate the second signal
        t, s_t = self.generate_signal_2()
        plot1D_single(t, s_t, '1-2', 'Time (s)', 'Amplitude')
        
        # Generate the third signal
        t, s_t = self.generate_signal_3()
        plot1D_multiple(t, [np.real(s_t), np.imag(s_t)], ['Real', 'Imaginary'], '1-3', 'Time (s)', 'Amplitude')
    