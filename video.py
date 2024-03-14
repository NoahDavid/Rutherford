import numpy as np

#### Sigma threshold for counting:
thresh = 6

#### File name:

# filename = 'test
filename = 'test-thorium'
# filename = 'output'
# filename = 'test-noise'





# Define a stats calculator:
def getStats(arr):
    # Number of nonzeros:
    nz = np.sum(arr != 0)
    # Mean:
    mean = np.mean(arr)
    # Standard deviation:
    std = np.std(arr)
    if std == 0:
        return 0, 0, 0, 0, 0
    # Sum all pixels:
    count = np.sum(((arr - mean) / std) >= thresh)

    # return values
    return mean, std, count, nz, np.sum(arr)
    

# Define the frame size (must match recording):
width = 1280
height = 976

# Get video file into memory:
video = np.fromfile(filename, dtype='uint8')

# Get total number of pixels:
length = video.shape[0]

# Reshape into a 3D matrix where first index counts frame number,
# second counts pixel number, and third gives RGB
video = np.reshape(video, (-1, width * height, 3))

# Iterate through frames:
for i in range(video.shape[0]):
    # Select one frame:
    frame = video[i, :, :]

    # Print stats for each frame:
    print(f'Frame {i}:')
    m, s, n, nz, c = getStats(frame[:, 0])
    print(f'RED:   mean = {m}, std = {s}, count = {n}, nonzero = {nz}, sum = {c}')
    
    m, s, n, nz, c = getStats(frame[:, 1])
    print(f'GREEN: mean = {m}, std = {s}, count = {n}, nonzero = {nz}, sum = {c}')

    m, s, n, nz, c = getStats(frame[:, 2])
    print(f'BLUE:  mean = {m}, std = {s}, count = {n}, nonzero = {nz}, sum = {c}\n')