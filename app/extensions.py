import os

from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()


# Data to test database:
GAMES = [
    {'winner':None, 'is_over':False, 'current_player':'X', 'grid':'XOXXOXOXO'},
    {'winner':'O', 'is_over':True, 'current_player':None, 'grid':'XOXXOXOOX'}
]

def create_db(app):
    from models import db
    # Delete database file if it exists currently
    if os.path.exists('game.db'):
        os.remove('game.db')

    with app.app_context():
        db.create_all()

def init_db(app):
    from models import Game
    with app.app_context():
        for game in GAMES:
            g = Game(winner=game.get('winner'), is_over=game.get('is_over'), current_player=game.get('current_player'), grid=game.get('grid'))
            db.session.add(g)

        db.session.commit()

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+ os.path.join(basedir, "game.db")
    db.init_app(app)
