#!/usr/bin/python3
"""
Create Amenity api
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """GET amenities"""
    amenity = storage.all(Amenity)
    data = [Amenity.to_dict(e) for e in amenity.values()]
    return jsonify(data)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """GET Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        return jsonify(Amenity.to_dict(amenity))


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """DELETE amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        amenity.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """Post Amenity"""
    if request.is_json:
        data = request.get_json()
        if 'name' in data:
            amenity = Amenity(**data)
            storage.new(amenity)
            storage.save()
            return jsonify(amenity.to_dict()), 201
        else:
            abort(400, 'Missing name')
    else:
        abort(400, 'Not a JSON')



@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Put Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if request.is_json:
        data = request.get_json()
        for k, v in data.items():
            if k == 'id' or k == 'created_at' or k == 'updated_at':
                continue
            else:
                setattr(amenity, k, v)
                storage.save()
        return jsonify(amenity.to_dict()), 200
    else:
        abort(400, 'Not a JSON')
