import matplotlib.pyplot as plt
import wave
import numpy as np

types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}

def getLeftChannelSamples(frames):
    samples = frames[0::2]
    return samples

filename = "audio_sample.wav"
wv = wave.open(filename, mode='r')

info = [nchammels, sampwidth, framerate, 
        nframes, comtype, compname] = wv.getparams()

print(filename, info)
frames = wv.readframes(nframes)
samples = np.fromstring(frames, dtype=types[sampwidth])
channel = samples[0::2]
print(samples)
#samples = getLeftChannelSamples(frames)
wv.close()

plt.plot([1,2,3,4], [1,4,9,16])
plt.axis([0, 6, 0, 20])
plt.ylabel('y')
plt.xlabel('x')
#plt.show()
