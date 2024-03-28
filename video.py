import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation

#### Sigma threshold for counting:
thresh = 6

#### File name:

# filename = 'test
filename = 'test-thorium-long'
# filename = 'output'
# filename = 'test-noise-long
filename = 'tape1ms_all'
filename = 'thorium1ms_all'
filename = 'noise1ms'

# Define the frame size (must match recording):
width = 1280
height = 976

# Get video file into memory:
video = np.fromfile(filename, dtype='uint8')

# Get total number of pixels:
length = video.shape[0]

# Make a figure
fig = plt.figure()

# Array of figures for the animation:
frames = []

# Reshape into a 3D matrix where first index counts frame number,
# second and third counts pixel location, and third gives RG
video = np.reshape(video, (-1, height, width, 3))
# video = np.reshape(video, (-1, width, height, 3))

# Iterate through frames:
for i in range(video.shape[0]):
    # Select one frame:
    frame = video[i, :, :, :]

    frame = np.mean(frame, axis=2)

    
    frames.append([plt.imshow(frame, animated=True)])

    # plt.colorbar(frames[-1])

    # plt.imshow(frame)
    # break

ani = animation.ArtistAnimation(fig, frames, interval=500, blit=True)
ani.save('test.gif')

plt.show()