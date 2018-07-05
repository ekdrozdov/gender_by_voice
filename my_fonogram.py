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

filename = "audio_sample.wav"

wv = wave.open(filename, mode='r')

(nchammels, sampwidth, framerate, nframes, comtype, compname) = wv.getparams()

frames = wv.readframes(nframes)
samples = np.frombuffer(frames, dtype=types[sampwidth])
channel = samples[0::2]
print(len(channel))
channel = channel[0:10000]

wv.close()

# Clip is a chunk of samples.

dx = 1
dy = 1
y, x = np.mgrid[slice(0, 100, 1), 
                slice(1, 100, 1)]

m = 1000
N = len(channel)
z = getSpectrogram(channel, m, N)
#z = np.fft.fft(x[:m])

z = np.sin(x**10 + np.cos(10 + y * x) * np.cos(x))
z = z[:-1, :-1]
levels = MaxNLocator(nbins=15).tick_values(z.min(), z.max())

cmap = plt.get_cmap('PiYG')
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

fig, (ax0, ax1) = plt.subplots(nrows=2)

im = ax0.pcolormesh(x, y, z, cmap=cmap, norm=norm)
fig.colorbar(im, ax=ax0)
ax0.set_title('pcolormesh with levels')

# contours are *point* based plots, so convert our bound into point
# centers
cf = ax1.contourf(x[:-1, :-1] + dx/2.,
                  y[:-1, :-1] + dy/2., z, levels=levels,
                  cmap=cmap)
fig.colorbar(cf, ax=ax1)
ax1.set_title('contourf with levels')

# adjust spacing between subplots so `ax1` title and `ax0` tick labels
# don't overlap
fig.tight_layout()

#plt.plot([1,2,3,4], [1,4,9,16])
#plt.axis([0, 6, 0, 20])
#plt.ylabel('y')
#plt.xlabel('x')
plt.show()
