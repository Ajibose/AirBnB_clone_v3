#!/usr/bin/python3
"""
    Create Blueprint routes
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status():
    """Testing flask"""
    return jsonify({"status": "OK"})

@app_views.route("/stats")
def stats():
    """retrieves the number of each objects by type"""
    countDict = {
            "amenities": Amenity,
            "cities":  City,
            "places": Place,
            'reviews': Review,
            "states": State,
            "users": User
    }


    for key, value in countDict.items():
        countDict[key] = storage.count(value)
    return jsonify(countDict)

