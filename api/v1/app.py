#!/usr/bin/python3
""" Main API module Main API module Main API module """
from os import getenv
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from api.v1.views import app_views
from models import storage


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def tearing_down(self):
    """ Tear down function"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """ Handler for 404 errors """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """ Main function  """
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)
    app.run(debug=True, host=host, port=port, threaded=True)
