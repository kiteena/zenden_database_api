from flask_restful import Resource
from flask import request
from deep_learning.cnn import CNN
from urllib.parse import unquote

cnn = CNN()
class CNNResource(Resource): 
    def get(self):
        try: 
            args = request.args
            folder_path = args['folder_path']
            folder_path = unquote(folder_path)
            folder_path = folder_path.lstrip('\"')
            folder_path = folder_path.rstrip('\"')
            data = cnn.makePredictions(folder_path)
            return {'status': 'success', "data": data}, 200 
        except Exception as e: 
            return {'status': str(e)}, 400