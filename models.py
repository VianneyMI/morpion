import enum
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

from app.extensions import db
class Player(enum.Enum):
    X = 'X'
    O = 'O'

class Mark(db.Model):
    __tablename__="mark"
    mark_id = db.Column(db.Integer, primary_key=True)
    row = db.Column(db.Integer, nullable=False)
    col = db.Column(db.Integer, nullable=False)
    #player = db.Column(db.String(1), nullable=False)
    player = db.Column(db.Enum(Player), nullable=False)

class MarkSchema(ModelSchema):
    player = fields.Method('get_player')
    def get_player(self,obj):
        return obj.current_player.value

    class Meta:
        model = Mark
        sqla_session = db.session

class Game(db.Model):
    __tablename__="game"
    game_id = db.Column(db.Integer, primary_key=True)
    winner = db.Column(db.Enum(Player)) #Could not get marshmallow_enum to work used custome serialized instead...
    #... thanks to : https://stackoverflow.com/questions/44717768/how-to-serialise-a-enum-property-in-sqlalchemy-using-marshmall
    is_over = db.Column(db.Boolean)
    current_player = db.Column(db.Enum(Player))
    grid = db.Column(db.String(9)) # I chose to use a simple string rather than an array

class GameSchema(ModelSchema):
    winner = fields.Method('get_winner')
    current_player = fields.Method('get_player')

    def get_winner(self,obj):
        return obj.winner.value

    def get_player(self,obj):
        return obj.current_player.value

    class Meta:
        model = Game
        sqla_session = db.session
