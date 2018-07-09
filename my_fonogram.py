import matplotlib
import matplotlib.pyplot as plt
import wave
import numpy as np
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator

types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}

def getSpectrogram(x, m, N):
    z = []
    for i in range(len(x) - m + 1):
        column = x[i:i + m]
        newcolumn = np.fft.fft(column)
        z.append(newcolumn)
        #z[i] = newcolumn
    return z

filename = "sample_female.wav"

wv = wave.open(filename, mode='r')

info = (nchammels, sampwidth, framerate, 
        nframes, comtype, compname) = wv.getparams()

print(info)

frames = wv.readframes(nframes)
samples = np.frombuffer(frames, dtype=types[sampwidth])
channel = samples[0::2]
print(len(channel))
#channel = channel[0:10000]

wv.close()

shift = 130000
m = windowsize = 7
spectdursec = 1/100
N = framerate * spectdursec
N = 1000

X = []
for i in range(N - 1):
    X.append(channel[i + shift:i + shift + m + 1])

FX = []
for i in range(N - 1):
    v = (np.fft.fft(X[i]))
    absv = np.absolute(v)
    FX.append(absv)
    print(i,"/", N - 2)

im = plt.imshow(FX, interpolation='bilinear', extent=[0, 1000, -100, 100])
matplotlib.colors.Normalize(vmin=-0.5, vmax=0.5)

print(len(channel))
start = 10000
N = 10
end = start + N
print(channel[start:end])

plt.show()

# Clip is a chunk of samples.

