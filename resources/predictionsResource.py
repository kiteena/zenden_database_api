from flask_restful import Resource
from flask import request
from models.userModel import User, UserSchema
from models.matchModel import Match, MatchSchema
from models.houseModel import House, HouseSchema
from deep_learning.recommender import Predictions
import json
import cv2

user_schema = UserSchema(only=['user_id'])
houses_schema = HouseSchema(many=True)
matches_schema = MatchSchema(many=True)
preds = Predictions()

class PredResource(Resource): 
    def get(self):
        try: 
            args = request.args
            user_id = args['user_id']

        # temp hack until nearest neighbor problem resolved
            data = User.query.first()
            sim_user = user_schema.dumps(data)
            sim_user_id = json.loads(sim_user)['user_id']
            
            matches = Match.query.with_entities(Match.house_id).all()
            matches1 = [m for m, in matches]
            houses = House.query.with_entities(House.house_id).filter(House.house_id.in_(matches1)).limit(100).all()
            houses1 =[h for h, in houses]
            results = preds.makePredictions(houses1, sim_user_id)
            results=[]
            if results:
                predicted_houses = House.query.filter(House.house_id.in_(results)).limit(25).all()
            else:
                predicted_houses = House.query.limit(25).all()          

            # not sure if problem is on my side or Marshmallow, but json coming back double-encoded
            data = houses_schema.dumps(predicted_houses)
            j = json.JSONDecoder()
            data = j.decode(data)
            return {'status': 'success', "data": data}, 200 
        except Exception as e: 
            return {'status': str(e)}, 400