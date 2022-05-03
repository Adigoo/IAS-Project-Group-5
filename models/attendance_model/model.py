
from flask import Flask, jsonify, request, Response
import pickle, requests, json, random, pymongo
from time import sleep
import json
app = Flask(__name__)
import numpy as np
from io import BytesIO
from PIL import Image
import pymongo



class ModelClass:

    def preprocess(self, img):
        stream = BytesIO(img)

        # image = Image.open(stream).convert("RGB")
        image = Image.open(stream)
        imgarray = np.array(image)
        print(f"type(image) = {type(imgarray)}")
        print(f"type(image) = {(imgarray.shape)}")

        # imgarray  = cv2.resize(imgarray, dsize=(224,224))
        img_annotation = random.randint(0, 10)
        print(f"type(image) = {(imgarray.shape)}")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

        
        stream.close()
        return imgarray                                                                                                                                                                                                                                                                                                                                                                                                                                           


    def postprocess(self,result):
            # print(result)
            return result
            
    
    def predict(self, image1):
        dat= []
        result = []

        image1p = self.preprocess(image1)
        
        img_annotation = random.randint(0, 10)

        
        # load model
        model = pickle.load(open('finalized_model.sav','rb'))
        a = np.array(dat)
        
        result.append(img_annotation)

        return json.dumps(result)



obj = ModelClass()
print(type(obj))
with open ("attendance_model.pkl","wb") as handle:
    pickle.dump(obj,handle)


# file = open("attendance_model.pkl", "rb")

# x = pickle.load(file)
# print(x.postprocess("hsahsa"))

