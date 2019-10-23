from flask_restful import Resource
from flask import request
from models.userModel import User, UserSchema
from models.matchModel import Match, MatchSchema
from models.houseModel import House, HouseSchema
import json
import cv2
import datetime

user_schema = UserSchema(only=['user_id'])
houses_schema = HouseSchema(many=True)
matches_schema = MatchSchema(many=True)

class PredResource(Resource): 
    def get(self):
        try: 
            args = request.args
            user_id = args['user_id']
            predicted_houses = []

            find_user = User.query.filter_by(user_id = user_id).first()

            # if the user has rated houses, find their predictions
            if find_user: 
                find_user_json = user_schema.dumps(find_user)
                find_user_id = json.loads(find_user_json)['user_id']
                matches = Match.query.filter_by(user_id=find_user_id, viewed=False).with_entities(Match.house_id).limit(20).all()
                matches1 = [m for m, in matches]
                predicted_houses = House.query.filter(House.house_id.in_(matches1)).limit(20).all()

            # if the user has not rated anything or there are no predictions the user hasn't seen
            # suggest any houses
            # TODO: need better solution for the cold-start problem 
            if not find_user or not predicted_houses: 
                predicted_houses = House.query.limit(25).all()                 

            data = houses_schema.dumps(predicted_houses)
            j = json.JSONDecoder()
            data = j.decode(data)

            return {'status': 'success', "data": data}, 200 
        except Exception as e: 
            return {'status': str(e)}, 400