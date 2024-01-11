#!/usr/bin/python3
"""
    Route for state objects
"""
from models.state import State
from models import storage
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views


@app_views.route("/states/")
@app_views.route("/states/<state_id>")
def retrieve_states(state_id=None):
    """Return all state object"""
    objs = storage.all().values()
    if state_id:
        objList = [obj for obj in objs if state_id == obj.id]
        return jsonify(objList[0].to_dict())
        abort(404)
    else:
        objList = [obj.to_dict() for obj in objs]
        return jsonify(objList)


@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete_state(state_id=None):
    """Removes a state"""
    states = storage.all().values()
    objList = [obj for obj in states if state_id == obj.id]
    if objList:
        storage.delete(objList[0])
        storage.save()
        return jsonify({})

    abort(404)


@app_views.route("/states/", methods=['POST'])
def create_state():
    """Create a state object"""
    if not request.json:
        abort(400, 'Not a JSON')

    if 'name' not in request.json:
        abort(400, 'Missing name')

    argDict = request.get_json()
    new_state = State(**argDict)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("states/<state_id>", methods=['PUT'])
def update_state(state_id):
    """Update a state object"""
    if not request.json:
        abort(400, 'Not a JSON')

    ikeys = ['id', 'created_at', 'updated_at']
    states = storage.all().values()
    objList = [obj for obj in states if state_id == obj.id]
    obj = objList[0]
    if not obj:
        abort(404)

    argDict = request.get_json()
    for k, v in argDict.items():
        if k not in ikeys:
            setattr(obj, k, v)

    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
