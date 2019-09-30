from flask import Flask 
from marshmallow import Schema, fields, validate 
from marshmallow_enum import EnumField
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from models.baseModel import ma, db

class User(db.Model): 
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(254))
    address = db.Column(db.String(80)) 
    city = db.Column(db.String(40))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.Integer)
    age = db.Column(db.Integer)
    income = db.Column(db.Float(13,2)) 
    sjsu_affiliated = db.Column(db.Boolean, default = False)
    # ed_level = db.Column(db.Enum(Education, 
    #     values_callable=lambda obj: [e.value for e in obj]),
    #     default=Education.UNSPECIFIED.value,
    #     server_default=Education.UNSPECIFIED.value)
    # gender = db.Column(db.Enum(Gender,
    #     values_callable=lambda obj: [e.value for e in obj]),
    #     default=Gender.UNSPECIFIED.value,
    #     server_default=Gender.UNSPECIFIED.value)

    education = db.Column(db.Enum('Some High School', 'High School', 'Some College', 'Bachelors Degree', 'Masters Degree', 'Doctorate', 'Unspecified', name='education_levels'), default='Unspecified')
    gender = db.Column(db.Enum('Male', 'Female', 'Other', 'Unspecified', name='gender_types'), default='Unspecified')

    ownership = db.Column(db.Enum('Rent', 'Own', 'Other', 'Unspecified', name='ownership_types'), default='Unspecified')
    housing_method = db.Column(db.Enum('House', 'Condominium','Apartment','Room','Shared Room','Mobile Home','Unspecified', name='housing_types'), default='Unspecified')
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    modified_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class UserSchema(ma.Schema):
    user_id = fields.Integer(dump_only=True) 
    name = fields.String(required=True,validate=validate.Length(3))
    email = fields.Email()
    address = fields.String(allow_none=True, required=False, validate=validate.Length(3))
    city = fields.String(validate=validate.Length(1))
    state = fields.String(validate=validate.Length(2))
    zipcode = fields.Integer(required=True)
    age = fields.Integer(allow_none=True, required=False)
    income = fields.Float(allow_none=True, required=False) 
    sjsu_affiliated = fields.Boolean()
    education = fields.Str(validate=validate.OneOf(['Some High School', 'High School', 'Some College', 'Bachelors Degree', 'Masters Degree', 'Doctorate', 'Unspecified']))
    gender = fields.Str(validate=validate.OneOf(['Male', 'Female', 'Other', 'Unspecified']))
    ownership = fields.Str(validate=validate.OneOf(['Rent', 'Own', 'Other', 'Unspecified']))
    housing_method = fields.Str(validate=validate.OneOf(['House', 'Condominium','Apartment','Room','Shared Room','Mobile Home','Unspecified']))
    created_at = fields.DateTime()
    modified_at = fields.DateTime()
