from flask import request
from flask_restful import Resource
from datetime import datetime
from models.matchModel import db, Match, MatchSchema


match_schema = MatchSchema() 
matches_schema = MatchSchema(many=True)

class MatchResource(Resource): 
    def get(self): 
        users = Match.query.all() 
        data = matches_schema.dump(users)
        return {'status': 'success', "data": data}, 200
    
    def post(self): 
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400

        data = match_schema.load(json_data)

        match = Match(
            house_id = json_data['house_id'],
            user_id = json_data['user_id'],
            predicted_score = json_data['predicted_score'],
            actual_score = json_data['actual_score'],
            viewed = json_data['viewed'],
            created_at = datetime.now(),
            modified_at = datetime.now()
            )

        db.session.add(match)
        db.session.commit()

        result = match_schema.dump(match)
        return { "status": 'success', 'data': result }, 201

