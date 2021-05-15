from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask import render_template

from app import create_app
from app.extensions import db

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    manager.run()
