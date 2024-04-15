#!/usr/bin/python3
"""
Create city api
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews_of_place(place_id):
    """Get reviews of place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = [c.to_dict() for c in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """GET review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(Review.to_dict(review))


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """DELETE review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        review.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Add review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.is_json:
        data = request.get_json()
        if 'name' in data:
            review = Review(**data)
            setattr(review, 'place_id', place_id)
            storage.new(review)
            storage.save()
            return jsonify(place.to_dict()), 201
        else:
            abort(400, 'Missing name')
    else:
        abort(400, 'Not a JSON')


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """Put review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if request.is_json:
        data = request.get_json()
        for k, v in data.items():
            if k == 'id' or k == 'created_at' or k == 'updated_at':
                continue
            else:
                setattr(review, k, v)
                storage.save()
        return jsonify(review.to_dict()), 200
    else:
        abort(400, 'Not a JSON')
