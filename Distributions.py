import numpy as np
import matplotlib.pyplot as plt
import scipy

file = "OurRawData/test-sodium-long"
file = "OurRawData/test-sodium-short"
# file = 'OurRawData/test-noise-long'
filenoise = 'OurRawData/test_noise_new'
file = 'OurRawData/test_sodium_new'


# Define the frame size (must match recording):
width = 1280
height = 976

# Get video file into memory:
video = np.fromfile(file, dtype='uint8')
videonoise = np.fromfile(filenoise, dtype='uint8')

# Get total number of pixels:
length = video.shape[0]

# Reshape into a 3D matrix where first index counts frame number,
# second and third counts pixel location, and third gives RG
video = np.reshape(video, (-1, height, width, 3))
videonoise = np.reshape(videonoise, (-1, height, width, 3))
# video = np.reshape(video, (-1, width, height, 3))

frames = np.copy(video[0:9, :, :, 1])
framesnoise = np.copy(videonoise[0:9, :, :, 1])

pixels = np.reshape(frames, (-1, )) 
pixelsnoise = np.reshape(framesnoise, (-1, )) 

bin_low = np.array(range(0, 256, 2))
bin_hi = bin_low + 2

hist = np.array([ np.sum((pixels >= bin_low[i]) & (pixels < bin_hi[i])) for i in range(len(bin_low)) ])
histnoise = np.array([ np.sum((pixelsnoise >= bin_low[i]) & (pixelsnoise < bin_hi[i])) for i in range(len(bin_low)) ])

while 0 in histnoise:
    for i in range(len(bin_low)):
        if histnoise[i] == 0:
            # combine bins
            hist[i-1] += hist[i]
            hist = np.delete(hist, i)
            histnoise = np.delete(histnoise, i)
            bin_low = np.delete(bin_low, i)
            bin_hi = np.delete(bin_hi, i)
            break


fit, _ = scipy.optimize.curve_fit(lambda t,a,b: a*np.exp(b*t),  bin_low+1,  hist, p0=(4000000, -5))

print(fit)

predicted = fit[0] * np.exp(fit[1] * (bin_low+1))

chisq = np.mean((hist - predicted) ** 2 / predicted)

print(chisq)

chisq_noise = np.mean((hist - histnoise) ** 2 / histnoise)

print(chisq_noise)

plt.bar(bin_low + 1, predicted, width = 2)
plt.bar(bin_low + 1, hist, width = 2)

plt.xlim(0, 50)

plt.show()