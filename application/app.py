from flask import jsonify
from flask_restful import Resource, reqparse
from mongoengine import NotUniqueError
from .model import UserModel
import re

_user_parser = reqparse.RequestParser()



_user_parser.add_argument('codigo',
                    type=str,
                    required=True,
                    help="This field cannot be blank"
                    )
_user_parser.add_argument('first_name',
                    type=str,
                    required=True,
                    help="This field cannot be blank"
                    )
_user_parser.add_argument('last_name',
                    type=str,
                    required=True,
                    help="This field cannot be blank"
                    )
_user_parser.add_argument('email',
                    type=str,
                    required=True,
                    help="This field cannot be blank"
                    )
_user_parser.add_argument('birth_date',
                    type=str,
                    required=True,
                    help="This field cannot be blank"
                    )

class Users(Resource):
    def get(self):
        return jsonify(UserModel.objects())


class User(Resource):
    def get (self, codigo):
        response = UserModel.objects(codigo=codigo)
        if response:
            return jsonify(response)
        return {"message": "user does not exists in database!"}, 400
    
    def post(self):
        data = _user_parser.parse_args()
        try:
            response = UserModel(**data).save()
            return {"message": "User %s successfully created" % response.id }
        except NotUniqueError:
            return {"message": "Codigo already exists in database"}, 400

