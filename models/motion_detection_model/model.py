import numpy as np
import pickle


def predict(images):
    pixel_diff = 0
    for idx1 in range(len(images)-1):
        for idx2 in range(len(images[idx1])):
            if(abs(images[idx1][idx2]-images[idx1+1][idx2])>50):
                pixel_diff += 1

    pixel_diff = pixel_diff/10

    if(pixel_diff>2000):
        result =  [1,1,1,1]
    elif(pixel_diff>1800):
        result =  [1,1,1,0]
    elif(pixel_diff>1700):
        result =  [1,1,0,1]
    elif(pixel_diff>1600):
        result =  [1,1,0,0]
    elif(pixel_diff>1500):
        result =  [1,0,1,1]
    elif(pixel_diff>1400):
        result =  [1,0,1,0]
    elif(pixel_diff>1300):
        result =  [1,0,0,1]
    elif(pixel_diff>1200):
        result =  [1,0,0,0]
    elif(pixel_diff>1100):
        result =  [0,1,1,1]
    elif(pixel_diff>800):
        result =  [0,1,1,0]
    elif(pixel_diff>600):
        result =  [0,1,0,1]
    elif(pixel_diff>600):
        result =  [0,1,0,0]
    elif(pixel_diff>500):
        result =  [0,0,1,1]
    elif(pixel_diff>400):
        result =  [0,0,1,0]
    elif(pixel_diff>300):
        result =  [0,0,0,1]
    else: 
        result = [0,0,0,0]

    return result

with open ("model.pkl","wb") as handle:
    pickle.dump(predict,handle)



