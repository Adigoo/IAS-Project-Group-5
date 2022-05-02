
from flask import Flask, jsonify, request, Response
import pickle, requests, json, random, pymongo
from time import sleep
import json
app = Flask(__name__)
import numpy as np
from io import BytesIO
from PIL import Image
import pymongo
import preprocessing



class AttendanceModel:



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
            pass

    

    
    def predict(self, image1):
        dat= []

        image1p = self.preprocess(image1)
        # model = preprocessing.vgg_face()
        # print(type(image1p))

        img_annotation = random.randint(0, 10)

        
        # load model
        # model = pickle.load(open('finalized_model.sav','rb'))
        a = np.array(dat)
        
        result = []
        result.append(img_annotation)

        return json.dumps(result)



obj = AttendanceModel()
print(type(obj))
with open ("attendance_model.pkl","wb") as handle:
    pickle.dump(obj,handle)


# file = open("attendance_model.pkl", "rb")

# x = pickle.load(file)
# print(x.postprocess("hsahsa"))

