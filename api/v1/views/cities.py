#!/usr/bin/python3
"""
    Route for state objects
"""
from models.city import City
from models.state import State
from models import storage
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities")
@app_views.route("/cities/<city_id>")
def retrieve_cities(state_id=None, city_id=None):
    """Return city object"""
    states = storage.all(State).values()
    if state_id:
        objList = [obj for obj in states if state_id == obj.id]
        if objList:
            cities = objList.cities
            cities = [obj.to_dict for obj in cities]
            return jsonify(cities)
    else:
        cities = storage.all(City).values()
        objList = [obj for obj in cities if city_id == obj.id]
        if objList:
            return jsonify(objList[0].to_dict())

    abort(404)
