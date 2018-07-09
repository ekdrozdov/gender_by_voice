import matplotlib.pyplot as plt
import numpy as np

#x = y = np.arange(0, 1, 0.1)
#X, Y = np.meshgrid(x, y)
#print(X)
#Z = np.sin(X)
#im = plt.imshow(Z, interpolation='bilinear', extent=[0, 1, 0, 1])
#plt.show()
#

x = list(range(1000))

N = 100 
m = 10
X = []
for i in range(N - 1):
    X.append(x[i:i + m])

FX = []
for i in range(N - 1):
    v = (np.fft.rfft(X[i]))
    absv = np.absolute(v)
    FX.append(absv)

#print(np.fft.fft(np.arange(1, 6)).real)

im = plt.imshow(FX, interpolation='bilinear', extent=[0, 10, 0, 10])

plt.show()
