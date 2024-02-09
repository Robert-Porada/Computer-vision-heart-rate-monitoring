import numpy as np
import matplotlib.pyplot as plt
import math
import operator


def dft(x):
    """
    Function to calculate the 
    discrete Fourier Transform 
    of a 1D real-valued signal x
    """

    N = len(x)
    n = np.arange(N)
    k = n.reshape((N, 1))
    e = np.exp(-2j * np.pi * k * n / N)
    
    X = np.dot(e, x)
    
    return X



def idft_max(X, fps, start_freq, stop_freq):

    N = len(X)
    n = np.arange(N)
    T = N/fps

    # Znajdowanie indexu maksymalnej częstotliwości z zakresu
    start_index = math.ceil(start_freq * T)
    stop_index = math.ceil(stop_freq * T)
    max_index, max_value = max(enumerate(abs(X[start_index : stop_index])), key=operator.itemgetter(1))
    max_index = max_index + start_index - 1

    # Obliczanie wartości maksymalnej częstotliwości
    max_index_freq = (max_index + 1) / T

    # Obliczanie przesunięcia i amplitudy 
    phase = np.angle(X[max_index])

    amplitude = X[max_index].real / N
    # amplitude = 1

    # Wyliczanie wartości sinusoidy
    x = np.arange(0, N)
    sin_max_shifted = np.sin((x) * max_index_freq / fps * (2*np.pi) + phase) * amplitude   

    return sin_max_shifted, max_index_freq
    

def display_dft(dft_blue, dft_green, dft_red, fps):
    N = len(dft_blue)
    n = np.arange(N)
    T = N/fps
    freq = n/T
    n_oneside = N//2
    f_oneside = freq[:n_oneside]
    X_oneside_blue = dft_blue[:n_oneside]/n_oneside
    X_oneside_green = dft_green[:n_oneside]/n_oneside
    X_oneside_red = dft_red[:n_oneside]/n_oneside

    plt.figure(figsize = (12, 6))

    plt.subplot(131)
    plt.stem(f_oneside, abs(X_oneside_blue), 'b', \
             markerfmt=" ", basefmt="-b")
    plt.xlabel('Freq (Hz) blue')
    plt.ylabel('DFT Amplitude |X(freq)|')
    plt.xlim(0, fps/2)

    plt.subplot(132)
    plt.stem(f_oneside, abs(X_oneside_green), 'b', \
             markerfmt=" ", basefmt="-b")
    plt.xlabel('Freq (Hz) green')
    plt.xlim(0, fps/2)

    plt.subplot(133)
    plt.stem(f_oneside, abs(X_oneside_red), 'b', \
             markerfmt=" ", basefmt="-b")
    plt.xlabel('Freq (Hz) red')
    plt.xlim(0, fps/2)

    plt.tight_layout()
    plt.show()


def display_idft(idft_blue, idft_green, idft_red):
    x = np.arange(len(idft_blue))
    plt.plot(x, idft_blue, c="blue")
    plt.plot(x, idft_green, c="green")
    plt.plot(x, idft_red, c="red")
    plt.show()

def display_channels(blue_channel_mean, green_channel_mean, red_channel_mean, count):
    x = np.arange(len(blue_channel_mean))
    plt.plot(x, blue_channel_mean, c="blue")
    plt.plot(x, green_channel_mean, c="green")
    plt.plot(x, red_channel_mean, c="red")
    plt.show()


def substract_mean(X):
    mean = np.mean(X)
    Y = [elem - mean for elem in X]
    return Y


