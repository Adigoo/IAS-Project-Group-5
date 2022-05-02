import numpy as np

def preprocessing(images):
    for idx in range(len(images)):
        images[idx] = images[idx].flatten()
        images[idx] = np.array(images[idx])
    return images