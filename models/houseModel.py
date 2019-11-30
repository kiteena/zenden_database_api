from flask import Flask 
from marshmallow import Schema, fields, validate 
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from models.baseModel import db, ma


class House(db.Model): 
    __tablename__ = 'houses'
    house_id = db.Column(db.Integer, primary_key=True)   # defaults to autoincrement 
    latitude = db.Column(db.Float(2,6), nullable=False)
    longitude = db.Column(db.Float(3,6), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(40), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    urls = db.Column(db.Text, nullable=False)
    usecode = db.Column(db.String(20))
    num_bedrooms = db.Column(db.Integer)
    num_bathrooms = db.Column(db.Float(2,1))
    house_sqft = db.Column(db.Integer)
    lot_sqft = db.Column(db.Integer)
    zpid = db.Column(db.Integer)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    modified_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class HouseSchema(ma.Schema): 
    house_id = fields.Integer(dump_only=True)    # dump_only = ignored from input 
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    address = fields.String(required=True, validate=validate.Length(5))
    city = fields.String(required=True, validate=validate.Length(2))
    state = fields.String(required=True, validate=validate.Length(2))
    zipcode = fields.Integer(required=True)
    urls = fields.String(required=True, validate=validate.Length(5))
    usecode = fields.String(validate=validate.Length(1))
    num_bedrooms = fields.Integer()
    num_bathrooms = fields.Float()
    house_sqft = fields.Integer()
    lot_sqft = fields.Integer()
    zpid = fields.Integer()
    created_at = fields.DateTime()
    modified_at = fields.DateTime()





