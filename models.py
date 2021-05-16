from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from app.extensions import db


class Mark(db.Model):
    __tablename__="mark"
    mark_id = db.Column(db.Integer, primary_key=True)
    row = db.Column(db.Integer, nullable=False)
    col = db.Column(db.Integer, nullable=False)
    player = db.Column(db.String(1), nullable=False)

class MarkSchema(ModelSchema):
    class Meta:
        model = Mark
        sqla_session = db.session


class Game(db.Model):
    __tablename__="game"
    game_id = db.Column(db.Integer, primary_key=True)
    winner = db.Column(db.String(1)) #TODO: Replace with Enum
    is_over = db.Column(db.Boolean)
    current_player = db.Column(db.String(1)) #TODO: Replace with Enum
    grid = db.Column(db.String(9)) #TODO: Replace with array

class GameSchema(ModelSchema):
    class Meta:
        model = Game
        sqla_session = db.session