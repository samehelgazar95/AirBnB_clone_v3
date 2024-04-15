#!/usr/bin/python3
"""
Create city api
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_of_state(state_id):
    """Get cities of state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities = [c.to_dict() for c in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """GET city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(City.to_dict(city))


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """DELETE city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        city.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Add city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.is_json:
        data = request.get_json()
        if 'name' in data:
            city = City(**data)
            setattr(city, 'state_id', state_id)
            storage.new(city)
            storage.save()
            return jsonify(state.to_dict()), 201
        else:
            abort(400, 'Missing name')
    else:
        abort(400, 'Not a JSON')


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """Put City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.is_json:
        data = request.get_json()
        for k, v in data.items():
            if k == 'id' or k == 'created_at' or k == 'updated_at':
                continue
            else:
                setattr(city, k, v)
                storage.save()
        return jsonify(city.to_dict()), 200
    else:
        abort(400, 'Not a JSON')
