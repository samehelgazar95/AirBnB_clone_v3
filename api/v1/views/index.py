#!/usr/bin/python3
""" Index module Index module Index module """
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.city import City
from models.user import User


@app_views.route('/status', methods=['GET'],
                 strict_slashes=False)
def status():
    """
    Api Status route
    """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'],
                 strict_slashes=False)
def stat():
    """
    Api stat route
    """
    objs = {'amenities': Amenity, 'cities': City, 'states': State,
            'places': Place, 'reviews': Review, 'users': User}
    res = {}
    for k, v in objs.items():
        res[k] = storage.count(v)
    return jsonify(res)
