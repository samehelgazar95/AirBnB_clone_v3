#!/usr/bin/python3
"""
Create User api
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_users():
    """GET users"""
    user = storage.all(User)
    data = [User.to_dict(e) for e in user.values()]
    return jsonify(data)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """GET User"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        return jsonify(User.to_dict(user))


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """DELETE user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        user.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_user():
    """Post user"""
    if request.is_json:
        data = request.get_json()
        if 'name' in data:
            user = User(**data)
            storage.new(user)
            storage.save()
            return jsonify(user.to_dict()), 201
        else:
            abort(400, 'Missing name')
    else:
        abort(400, 'Not a JSON')



@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """Put User"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if request.is_json:
        data = request.get_json()
        for k, v in data.items():
            if k == 'id' or k == 'created_at' or k == 'updated_at':
                continue
            else:
                setattr(user, k, v)
                storage.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(400, 'Not a JSON')
