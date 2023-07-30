
from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api, reqparse
from bson.objectid import ObjectId
from db import db

user_bp = Blueprint('user_bp', __name__)
api = Api(user_bp)

user_fields = ['name', 'email', 'password']

def id_to_string(user):
    user['_id'] = str(user['_id'])
    return user

class UsersResource(Resource):
    def get(self):
        users = list(db.users.find())
        users = [id_to_string(user) for user in users]
        return jsonify(users)

    def post(self):
        _json = request.json
        for field in user_fields:
            if field not in _json:
                return jsonify({'message': f'Missing {field} field'}), 400
        user_id = db.users.insert_one({'name': _json['name'], 'email': _json['email'], 'password': _json['password']}).inserted_id
        new_user = db.users.find_one({'_id': user_id})
        return{"message": "user inserted successfully","new user":id_to_string(new_user)}

class UserResource(Resource):
    def get(self, user_id):
        user = db.users.find_one({'_id': ObjectId(user_id)})
        if user:
            user = id_to_string(user)
            return jsonify(user)
        else:
            return jsonify({'message': 'User not found'}), 404

    def put(self, user_id):
        _json = request.json
        updated_user = db.users.find_one_and_update(
            {'_id': ObjectId(user_id)},
            {'$set': _json},
            return_document=True
        )
        if updated_user:
            updated_user = id_to_string(updated_user)
            return jsonify(updated_user)
        else:
            return jsonify({'message': 'User not found'}), 404

    def delete(self, user_id):
        result = db.users.delete_one({'_id': ObjectId(user_id)})
        if result.deleted_count > 0:
            return jsonify({'message': 'User deleted successfully'})
        else:
            return jsonify({'message': 'User not found'}), 404

api.add_resource(UsersResource, '/users')
api.add_resource(UserResource, '/users/<string:user_id>')
