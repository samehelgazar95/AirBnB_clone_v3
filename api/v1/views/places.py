#!/usr/bin/python3
"""
Create place api
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place


@app_views.route('cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_of_city(city_id):
    """Get places of city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = [p.to_dict() for p in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """GET place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        return jsonify(Place.to_dict(place))


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """DELETE place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        place.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Add place"""
    city = storage.get(City, city_id)
    if place is None:
        abort(404)

    if request.is_json:
        data = request.get_json()
        if 'name' in data:
            place = Place(**data)
            setattr(place, 'state_id', city_id)
            storage.new(place)
            storage.save()
            return jsonify(place.to_dict()), 201
        else:
            abort(400, 'Missing name')
    else:
        abort(400, 'Not a JSON')


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Put Place"""
    place = storage.get(Place, place_id)
    if place_id is None:
        abort(404)

    if request.is_json:
        data = request.get_json()
        for k, v in data.items():
            if k == 'id' or k == 'created_at' or k == 'updated_at':
                continue
            else:
                setattr(place, k, v)
                storage.save()
        return jsonify(place.to_dict()), 200
    else:
        abort(400, 'Not a JSON')
