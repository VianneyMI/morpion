from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/lc-test.db'
    db.init_app(app)

