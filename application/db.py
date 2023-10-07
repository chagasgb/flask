from flask_mongoengine import MongoEngine
from flask.json import JSONEncoder

db = MongoEngine()


def init_db(app):
    db.init_app(app)
