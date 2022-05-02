# -*- coding: utf-8 -*-
"""sample_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bn5dORdLgKWP8HXu-C9u6towEMvB6gJc
"""

import random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import pickle
import warnings
import numpy as np
warnings.filterwarnings("ignore")
class FireDetection:
  def __init__(self):
    self.temp_data, self.fire_alarm_data = self.generate_data()
    self.input_data = self.create_Df( )
    self.X_train, self.X_test, self.y_train, self.y_test = self.split_data(  )
    self.decision_tree_model = self.Decison_Tree()

  def generate_data(self):

    # generate temperature data
    temp_data = []
    for i in range( 10000 ):
      temp = random.uniform(10, 50)
      temp_data.append( temp )

    # generate fire_alarm data
    fire_alarm_data = []
    for i in range( 10000 ):
      fire_alarm = random.randint(0,1)
      if fire_alarm == 0:
        fire_alarm_data.append( False )
      else:
        fire_alarm_data.append( True )

    return temp_data, fire_alarm_data

  

  def create_Df(self):
    input_data = pd.DataFrame(list(zip(self.temp_data, self.fire_alarm_data)), columns=['Temperature', 'Fire_Alarm'])
    return input_data

  

  def split_data(self ):
    #X = input_data.drop(columns="Fire_Alarm")
    X = self.input_data["Temperature"]
    
    y = self.input_data["Fire_Alarm"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.80)
    return X_train, X_test, y_train, y_test

  

  def Decison_Tree( self ):
    self.X_train = np.array( self.X_train )
    self.X_train = self.X_train.reshape(-1, 1)
    decision_tree_model = DecisionTreeClassifier(max_depth =3, random_state = 42)
    decision_tree_model.fit(self.X_train, self.y_train)
    return decision_tree_model

  def predict(self, data):
    result =self.decision_tree_model.predict([[data]])
    return result[0]


# obj = FireDetection()

# pickle_file = open('fire_detection_model.pkl', 'wb')
# pickle.dump( obj, pickle_file )
# pickle_file.close()


# file = open("fire_detection_model.pkl", "rb")
# x = pickle.load(file)

#print(x.predict(47.857214))
#decision_tree_model.predict([[47.857214]])