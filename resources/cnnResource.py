from flask_restful import Resource
from flask import request
from deep_learning.cnn import CNN
from urllib.parse import unquote
from config import AccessKeyID, SecretAccessKey
import boto3
import os
import base64

cnn = CNN()
folder_path = 'deep_learning/serialized_models/data/'

class CNNResource(Resource): 
    def get(self):
        try: 
            args = request.args
            filenames = unquote(args['filenames'])
            filenames = [f.strip('\' ') for f in filenames.split(',')]
            print(filenames)
            # download files
            for f in filenames: 
                if not f: 
                    continue
                s3 = boto3.client ('s3', aws_access_key_id=AccessKeyID, aws_secret_access_key=SecretAccessKey)
                try: 
                    s3.download_file('zenden-cnn',f'{f}', folder_path + f'{f}')
                except Exception as e:
                    raise Exception('File not found in AWS bucket. Please verify file was uploaded.') 

            # make predictions
            data = cnn.makePredictions(folder_path)
            # remove downloaded files 
            for f in filenames:
                if not f: 
                    continue
                os.remove(folder_path + f'{f}')
            return {'status': 'success', "data": data}, 200 
        except Exception as e: 
            return {'status': str(e)}, 400