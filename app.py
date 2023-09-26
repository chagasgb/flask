from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flask_mongoengine import MongoEngine

app = Flask(__name__)
api = Api(app)

app.config['MONGODB_SETTINGS'] = {
    "db": "users",
    "host": "mongodb",
    "port": 27017,
    "username": "admin",
    "password": "admin"
}

db = MongoEngine(app)


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help='Nome do objeto')

class UserModel(db.Document):
    cpf = db.StringField(required=True, unique=True)
    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    email = db.EmailField(required=True)
    birth_date = db.DateTimeField(required=True)

class Users(Resource):
    def get(self):
        args = parser.parse_args()
        name = args['name']     
        return {'nome': name} 
    
    #   return {"message": "user 1"}

#class User(Resource):
#    def post(self):
#        #data = _user_parser.parse_args()
#        return {"message": "CPF"}
#        #return data
#    def post(self, name):
#        args = parser.parse_args()
#        name = args['name']
#        
#        return {'nome': name}


api.add_resource(Users, "/users")
#api.add_resource(User, "/user", "/user/<string:cpf>")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
