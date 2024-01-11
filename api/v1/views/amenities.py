#!/usr/bin/python3
"""
    Route for state objects
"""
from models.state import State
from models.amenity import Amenity
from models import storage
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views


@app_views.route("/amenities/")
@app_views.route("/amenities/<amenity_id>")
def retrieve_amenties(amenity_id=None):
    """Return all amenities object"""
    objs = storage.all().values()
    if amenity_id:
        objList = [obj for obj in objs if amenity_id == obj.id]
        if objList:
            return jsonify(objList[0].to_dict())
        abort(404)
    else:
        objList = [obj.to_dict() for obj in objs]
        return jsonify(objList)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'])
def delete_amenity(amenity_id=None):
    """Removes a state"""
    amenities = storage.all().values()
    objList = [obj for obj in amenities if amenity_id == obj.id]
    if objList:
        storage.delete(objList[0])
        storage.save()
        return jsonify({})

    abort(404)


@app_views.route("/amenities/", methods=['POST'])
def create_amenity():
    """Create a amenity object"""
    if not request.json:
        abort(400, 'Not a JSON')

    if 'name' not in request.json:
        abort(400, 'Missing name')

    argDict = request.get_json()
    new_amenity = Amenity(**argDict)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=['PUT'])
def update_amenity(amenity_id):
    """Update a amenity object"""
    if not request.json:
        abort(400, 'Not a JSON')

    ikeys = ['id', 'created_at', 'updated_at']
    amenities = storage.all().values()
    objList = [obj for obj in amenities if amenity_id == obj.id]
    if not objList:
        abort(404)

    obj = objList[0]

    argDict = request.get_json()
    for k, v in argDict.items():
        if k not in ikeys:
            setattr(obj, k, v)

    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
