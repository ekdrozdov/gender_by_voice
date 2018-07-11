import sys
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


def printusage(myname):
    print(f'Usage: {myname} filename.wav')


def printinfo(wv, filename):
    print(f'INFO about {filename}:')
    (nchannels, sampwidth, framerate, nframes, comtype, compname) = wv.getparams()
    nsecs = nframes / framerate
    print(f'Duration: {nsecs:2.3} (secs)\t{nframes} (samples)')
    print(f'Framerate: {framerate} (samps/sec)')


def getcpstrgram(FX):
    m = 2
    FX = np.add(FX, j(2 * np.pi * m))
    FX = np.log(FX)
    CX = []
    for i in range(N):
        v = (np.fft.ifft(FX[i]))
        #absv = np.absolute(v)
        CX.append(v)

    return CX


# Funciton get lengths in milliseconds and converts it to samples lengths.
def getspctgram(wv, durms, windowsizems, stepms, *argv):
    offsetms = 0
    if len(argv) > 0:
        offsetms = argv[0]
    isverbose = 0
    if len(argv) > 1:
        isverbose  = argv[1]

    # Get file info.
    (nchannels, sampwidth, framerate, nframes, comtype, compname) = wv.getparams()
    frames = wv.readframes(nframes)
    samples = np.frombuffer(frames, dtype=types[sampwidth])
    # Get samples for a left channel.
    channel = samples[0::2]

    # Convert ms to nsamples.
    msframert = framerate / 1000
    duration = int(msframert * durms)
    windowsize = int(msframert * windowsizems)
    offset = int(msframert * offsetms)
    step = int(msframert * stepms)
    print("step", step)

    # TODO: check that (step * k + offset + windowsize + duration < nframes)
    # Check offset for out of range.
    if offset > nframes - 100:
        print("getspctgram warning: offset gets out of range, cutted off") 
        offset = nframes - 100

    # Check duration for out of range.
    if duration + offset > nframes:
        print("getspctgram warning: duration gets out of range, cutted off")
        duration = nframes - offset

    m = windowsize
    N = int(duration / step)

    X = []
    for i in range(N):
        X.append(channel[i * step + offset: i * step + offset + m])

    FX = []
    if isverbose == 0:
        for i in range(N):
            v = (np.fft.fft(X[i]))
            absv = np.absolute(v)
            FX.append(absv)
    else:
        for i in range(N):
            v = (np.fft.fft(X[i]))
            absv = np.absolute(v)
            FX.append(absv)
            print(i + 1,"/", N)

    complexm = np.fft.fft(channel[offset: offset + duration + windowsize])
    realm = np.absolute(complexm)
    m = np.min(realm)
    print(f'min: {m}')

    return FX, m


def normalize(FX, m):
    FX = np.transpose(FX)
    FX = FX[int(len(FX) / 2):]

    FX = np.multiply(FX, 1 / m)
    FX = np.log10(FX)
    FX = np.multiply(FX, 20)

    return FX


def plotspctrgram(wv, FX, durms, wszms):
    (nchannels, sampwidth, framerate, nframes, comtype, compname) = wv.getparams()
    wsz = wszms / 1000 * framerate
    freqmax = framerate / 2
    freqmin = framerate / wsz
    scale = 1
    im = plt.imshow(FX, interpolation='bilinear', extent=[0, durms * scale, freqmin, freqmax])
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

offsetms = 0
durms = 900
windowsizems = 100
isverbose = 1
stepms = 0.8 # 0.05 ms ~ 2 samples
FX, m = getspctgram(wv, durms, windowsizems, stepms, offsetms, isverbose)
FX = getcpstrgram(FX)
#FX = normalize(FX, m)
printinfo(wv, filename)
plotspctrgram(wv, FX, durms, windowsizems)

wv.close()
quit()



