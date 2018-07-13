import sys
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import wave

types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}


def getclip(wv, durms, offsetms):
    # Get file info.
    (nchannels, sampwidth, framerate,
            nframes, comtype, compname) = wv.getparams()
    frames = wv.readframes(nframes)
    samples = np.frombuffer(frames, dtype=types[sampwidth])
    # Get samples for a left channel.
    channel = samples[0::2]

    # Convert ms to nsamples.
    msframert = framerate / 1000
    duration = int(msframert * durms)
    offset = int(msframert * offsetms)
    clip = channel[offset: offset + duration]
    # Thus, length of the clip is duration in samples.
    return clip


fs = 10e3
N = 1e5
amp = 2 * np.sqrt(2)
noise_power = 0.01 * fs / 2
time = np.arange(N) / float(fs)
mod = 500*np.cos(2*np.pi*0.25*time)
carrier = amp * np.sin(2*np.pi*3e3*time + mod)
noise = np.random.normal(scale=np.sqrt(noise_power), size=time.shape)
noise *= np.exp(-time/5)
x = carrier + noise

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print("Error: too few arguments")
    quit()

wv = wave.open(filename, mode='r')
(nchannels, sampwidth,
        framerate, nframes, comtype, compname) = wv.getparams()

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print("Error: too few arguments")
    printusage(sys.argv[0])
    quit()

clip = getclip(wv, 1000, 0)

f, t, Sxx = signal.spectrogram(clip, framerate)
plt.pcolormesh(t, f, Sxx)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
