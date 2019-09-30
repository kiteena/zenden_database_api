from keras.models import load_model, model_from_json
from keras.applications import ResNet50
import numpy as np 
import os
import json 
import tensorflow as tf

class Predictions: 
    def __init__(self): 
        self.model = load_model('deep_learning/serialized_models/recommender.h5')
        self.graph = tf.get_default_graph()

    def makePredictions(self, houses_column, user): 
        try:
            with self.graph.as_default():
                user_formatted = [user] * 100
                preds = self.model.predict([user_formatted, houses_column])
                idxs = [i for i,r in enumerate(preds) if r >= 0 ]
                return [houses_column[i] for i in idxs]
        except Exception as e: 
            raise Exception(str(e))


        