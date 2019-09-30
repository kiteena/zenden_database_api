from flask import request
from flask_restful import Resource
from models.houseModel import db, House, HouseSchema
from models.matchModel import Match, MatchSchema
from resources.matchesResource import matches_schema
from datetime import datetime
from flask_restful import request
from sqlalchemy import not_

house_schema = HouseSchema()
houses_schema = HouseSchema(many=True)

class HouseResource(Resource): 
    def get(self): 
        houses = House.query.all() 
        data = houses_schema.dump(houses)
        return {'status': 'success', "data": data}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        print(json_data)
        data = house_schema.load(json_data)
        # if errors:
        #     return errors, 422
        # houses = House.query.filter_by(name=data['name']).first()
        # if category:
        #     return {'message': 'Category already exists'}, 400
        house = House(
            latitude = json_data['latitude'],
            longitude = json_data['longitude'],
            address = json_data['address'],
            city = json_data['city'],
            state = json_data['state'],
            urls = json_data['urls'],
            usecode = json_data['usecode'],
            num_bedrooms = json_data['num_bedrooms'],
            num_bathrooms = json_data['num_bathrooms'],
            house_sqft = json_data['house_sqft'],
            lot_sqft = json_data['lot_sqft'],
            zpid = json_data['zpid'],
            zipcode = json_data['zipcode'],
            created_at = datetime.now(),
            modified_at = datetime.now()
            )

        db.session.add(house)
        db.session.commit()

        result = house_schema.dump(house)
        return { "status": 'success', 'data': result }, 201

class HouseResourceCount(Resource): 
    def get(self, count): 
        args = request.args
        user_id = args['user_id']
        # matches = Match.query.filter(Match.user_id == 1).with_entities(Match.house_id)
        # data1 = matches_schema.dump(matches)
        matches = Match.query.filter(Match.user_id == user_id).with_entities(Match.house_id).all()
        matches1 = [m for m, in matches]
        print(matches1)
        houses = House.query.filter(not_(House.house_id.in_(matches1))).limit(count).all()
        data = houses_schema.dump(houses)
        print(data)
        return {'status': 'success', "data": data}, 200
