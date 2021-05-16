import os

from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()


def create_db(app):
    from models import db
    with app.app_context():
        db.create_all()

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+ os.path.join(basedir, "game.db")
    db.init_app(app)
