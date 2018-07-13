import sys
import matplotlib
import matplotlib.pyplot as plt
import wave
import numpy as np
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator


frcut = 2000


types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}


def printusage(myname):
    print(f'Usage: {myname} filename.wav')


def printinfo(wv, filename):
    print(f'INFO about {filename}:')
    (nchannels, sampwidth, framerate, nframes, comtype, compname) = wv.getparams()
    nsecs = nframes / framerate
    print(f'Duration: {nsecs:2.3} (secs)\t{nframes} (samples)')
    print(f'Framerate: {framerate} (samps/sec)')


def getfundfreq(FX):
    m = []
    for fx in FX:
        #print("local max:", np.max(fx))
        m.append(np.max(fx))

    maxm = sum(m) / float(len(m))
    print("arg", np.argmax(FX[100]))
    return maxm


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


def getspectre(framerate, clip, windowsizems, stepms):
    # Convert ms to nsamples.
    msframert = framerate / 1000
    windowsize = int(msframert * windowsizems)
    step = int(msframert * stepms)

    m = windowsize
    N = (len(clip) - m + step) // step

    FX = []
    k = (frcut * windowsize) // framerate
    for i in range(N):
        FX.append(np.fft.fft(clip[i * step: i * step + m]))
        # Cut all frequensies above 3500 Hz.
        FX[i] = FX[i][:k]
        FX[i] = FX[i][::-1]

    FX = np.column_stack(FX)
    #FX = FX[len(FX) // 2:]
    FX = np.abs(FX)


    #m = np.min(np.abs(np.fft.fft(clip)))
    #FX = (20 * np.log10(FX / m))

    return FX


def getcepstrum(spectrum):
    eps = 0.00000001
    FX = np.log(spectrum + eps)
    N = len(spectrum)
    CX = []
    for i in range(N):
        CX.append(np.fft.ifft(FX[i]))

    CX = np.column_stack(CX)
    CX = np.abs(CX)
    acc = 0
    count = 0
    for i in range(N):
        #print(CX[i])
        acc += np.argmax(CX[i])
        count = count + 1
        #print("loc max arg", np.argmax(CX[i]))
    print(acc // count)
    return CX


def plotspctrgram(wv, FX, durms, wszms):
    (nchannels, sampwidth, framerate, 
            nframes, comtype, compname) = wv.getparams()
    wsz = wszms / 1000 * framerate
    freqmax = framerate / 2
    freqmax = frcut
    freqmin = framerate / wsz
    #im = plt.imshow(FX, interpolation='bilinear',
    #        extent=[0, len(FX), 0, len(FX[0])])
            
    im = plt.imshow(FX, interpolation='bilinear',
            extent=[0, durms, freqmin, freqmax])
    plt.xlabel("Time, ms")
    plt.ylabel("Frequency, Hz")
    plt.show()


# Main.
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print("Error: too few arguments")
    printusage(sys.argv[0])
    quit()

wv = wave.open(filename, mode='r')
(nchannels, sampwidth, 
        framerate, nframes, comtype, compname) = wv.getparams()

offsetms = 0
durms = 2000
windowsizems = 100
stepms = 0.3 # 0.05 ms ~ 2 samples

clip = getclip(wv, durms, offsetms)
spectre = getspectre(framerate, clip, windowsizems, stepms)
cepstrum = getcepstrum(spectre)

plt.subplot(311)
plt.plot(range(len(clip[::])), clip[::])
plt.subplot(312)
plt.plot(range(len(list(spectre[200][::]))), list(spectre[200][::]))
plt.subplot(313)
plt.plot(range(len(list(cepstrum[200][::]))), list(cepstrum[200][::]))

#FX, m = getspectre(wv, clip, windowsizems, stepms, isverbose)
#plotspctrgram(wv, spectre, durms, windowsizems)
#plotspctrgram(wv, cepstrum, durms, windowsizems)
plt.show()

printinfo(wv, filename)

#plotspctrgram(wv, CX, durms, windowsizems)
#argmax = getfundfreq(cepstrum)
#print("average max:", argmax)
#print("max pos:", cepstrum.argmax())
#print("ff:", framerate // cepstrum.argmax())
#print("fundamental freq:", framerate // argmax)

wv.close()
quit()



