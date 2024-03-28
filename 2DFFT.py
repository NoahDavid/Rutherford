import numpy as np
import matplotlib.pyplot as plt

file = "OurRawData/test-sodium-long"
file = "OurRawData/test-sodium-short"
# file = 'OurRawData/test-noise-long'
file = 'OurRawData/test_noise_new'
# file = 'OurRawData/test_sodium_new'

def calculate_2dft(input):
    ft = np.fft.ifftshift(input)
    ft = np.fft.fft2(ft)
    return np.fft.fftshift(ft)

def idft(input):
    ft = np.fft.ifftshift(input)
    ft = np.fft.ifft2(ft)
    return np.fft.fftshift(ft)

def filterFreq(nlow, nhigh, im):
    midx = im.shape[0] / 2
    midy = im.shape[1] / 2

    dist_sq = lambda x, y: (x - midx) ** 2 + (y - midy) ** 2

    return im * np.array([ [ 0 if dist_sq(i, j) < nlow or dist_sq(i, j) > nhigh else 1 for j in range(im.shape[1]) ] for i in range(im.shape[0]) ])

# Define the frame size (must match recording):
width = 1280
height = 976

# Get video file into memory:
video = np.fromfile(file, dtype='uint8')

# Get total number of pixels:
length = video.shape[0]

# Reshape into a 3D matrix where first index counts frame number,
# second and third counts pixel location, and third gives RG
video = np.reshape(video, (-1, height, width, 3))
# video = np.reshape(video, (-1, width, height, 3))

frame = np.copy(video[0, :, :, 1])

frame_fftr = calculate_2dft(video[0, :, :, 0])
frame_fftg = calculate_2dft(video[0, :, :, 1])
frame_fftb = calculate_2dft(video[0, :, :, 2])

frame_filt_r = np.abs(idft(filterFreq(100, 3000, frame_fftr))) 
frame_filt_g = np.abs(idft(filterFreq(100, 3000, frame_fftg))) 
frame_filt_b = np.abs(idft(filterFreq(100, 3000, frame_fftb))) 

frame_filt_b[:30, :] = 0
frame_filt_b[-30:, :] = 0
# plt.imshow(np.abs(idft(filterFreq(100, 3000, frame_fftb))))

# frame[frame > 25] = 0
# plt.imshow(video[0, :, :, 2])
plt.hist(np.reshape(frame, width*height), bins = 25)
# plt.imshow(video[40, :, :, 1])
# plt.hist(frame_filt_b)
# plt.imshow(np.log(np.abs(frame_fftb)))
# plt.imshow(filterFreq(5, 300, frame_fftb))
# plt.imshow(np.log(np.abs(filterFreq(5, 300, frame_fftb))))

plt.show()