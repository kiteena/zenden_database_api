from flask import Flask 
from marshmallow import Schema, fields, validate 
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from models.baseModel import ma, db


class Match(db.Model): 
    __tablename__="matches"
    users = db.relationship('User')
    houses = db.relationship('House')
    match_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.user_id', ondelete='CASCADE'),
        nullable=False,
    )
    house_id = db.Column(
        db.Integer,
        db.ForeignKey('houses.house_id', ondelete='CASCADE'),
        nullable=False,
    )
    predicted_score = db.Column(db.Integer, default=1)
    actual_score = db.Column(db.Integer)
    viewed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    modified_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())


class MatchSchema(ma.Schema):
    match_id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    house_id = fields.Integer(required=True)
    predicted_score = fields.Integer()
    actual_score = fields.Integer()
    viewed = fields.Boolean()
    created_at = fields.DateTime()
    modified_at = fields.DateTime()

        

