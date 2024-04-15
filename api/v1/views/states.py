#!/usr/bin/python3
"""
Create state api
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'],
                 strict_slashes=False)
def get_states():
    """GET States"""
    states = storage.all(State)
    data = [State.to_dict(e) for e in states.values()]
    return jsonify(data)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """GET State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(State.to_dict(state))


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """DELETE State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        state.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def post_state():
    """Post State"""
    if request.is_json:
        data = request.get_json()
        if 'name' in data:
            state = State(**data)
            storage.new(state)
            storage.save()
            return jsonify(state.to_dict()), 201
        else:
            abort(400, 'Missing name')
    else:
        abort(400, 'Not a JSON')


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """Put State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.is_json:
        data = request.get_json()
        for k, v in data.items():
            if k == 'id' or k == 'created_at' or k == 'updated_at':
                continue
            else:
                setattr(state, k, v)
                storage.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(400, 'Not a JSON')
