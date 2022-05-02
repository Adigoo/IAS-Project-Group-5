import pickle
from preprocessing import preprocessing
from postprocessing import postprocessing

def predict(images):
    images = preprocessing(images)
    MD_model = open("model.pkl", 'rb')
    model = pickle.load(MD_model)
    predictions = model(images)
    return postprocessing(predictions)

