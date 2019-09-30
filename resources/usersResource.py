from flask import request
from flask_restful import Resource
from datetime import datetime
from models.userModel import db, User, UserSchema
from resources.matchesResource import Match

user_schema = UserSchema() 
users_schema = UserSchema(many=True)

class UserResource(Resource): 
    def get(self): 
        users = User.query.all() 
        data = users_schema.dump(users)
        return {'status': 'success', "data": data}, 200

    def post(self): 
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400

        data = user_schema.load(json_data)

        # allow optional fields to be None
        age = json_data['age'] if 'age' in json_data else None
        income = json_data['income'] if 'income' in json_data else None
        address = json_data['address'] if 'address' in json_data else None

        user = User(
            name = json_data['name'],
            email = json_data['email'],
            address = address,
            city = json_data['city'],
            state = json_data['state'],
            zipcode = json_data['zipcode'],
            age = age,
            income = income,
            sjsu_affiliated = json_data['sjsu_affiliated'],
            education = json_data['education'],
            gender = json_data['gender'],
            ownership = json_data['ownership'], 
            housing_method = json_data['housing_method'],
            created_at = datetime.now(),
            modified_at = datetime.now()
            )

        # match = Match(
        #     house_id = 381,
        #     user_id = user.user_id,
        #     predicted_score = 1,
        #     actual_score = -1, 
        #     viewed = False
        # )

        db.session.add(user)
        db.session.commit()

        # id = User.query.filter_by(name=data['name']).first()
        # match = Match(
        #     house_id = 381,
        #     user_id = id.user_id,
        #     predicted_score = 1,
        #     actual_score = -1, 
        #     viewed = False
        # )
        # db.session.add(match)
        # db.session.commit()

        result = user_schema.dump(user)
        return { "status": 'success', 'data': result }, 201

