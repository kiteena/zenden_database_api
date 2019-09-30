from keras.models import load_model, model_from_json
from keras.applications import ResNet50
import numpy as np 
import os
import cv2
import json 
import tensorflow as tf

test_path = 'deep_learning/serialized_models/data/'

class CNN:  
    def __init__(self):
        self.choices =['front', 'inside', 'house_other', 'not_house']
        self.model = load_model('deep_learning/serialized_models/cnn_keras_2_2_5.h5')
        self.graph = tf.get_default_graph()

    def makeImageArray(self, directory): 
        imgs = []
        if not os.path.isdir(directory):
            raise Exception('This endpoint requires a folder of images!')

        self.files = sorted(os.listdir(directory))
        for i in self.files: 
            path = os.path.join(directory, i)
            img = cv2.imread(path, cv2.COLOR_BGR2RGB)
            try: 
                img = cv2.resize(img, (128,128))
                imgs.append(img)
            except: 
                pass # hidden file throwing an error 

        return np.array(imgs)


        
    def humanReadableLabel(self, prediction_lbl): 
        return self.choices[prediction_lbl]

    def makePredictions(self, path): 
        arr = self.makeImageArray(path)
        try:
            with self.graph.as_default():
                preds = self.model.predict(arr)
        except Exception as e: 
            raise Exception(str(e))
        labels = {}
        for i, p in enumerate(preds): 
            maxval = np.max(p)
            labels[self.files[i]]=self.humanReadableLabel(np.squeeze(np.where(p==maxval)[0]).item(0))
        return labels
