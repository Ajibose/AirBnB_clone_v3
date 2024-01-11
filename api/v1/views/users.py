#!/usr/bin/python3
"""
    Route for user objects
"""
from models.user import User
from models import storage
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views


@app_views.route("/users")
@app_views.route("/users/<user_id>")
def retrieve_user(user_id=None):
    """Return all user object"""
    objs = storage.all(User).values()
    if user_id:
        objList = [obj for obj in objs if user_id == obj.id]
        if objList:
            return jsonify(objList[0].to_dict())
        abort(404)
    else:
        objList = [obj.to_dict() for obj in objs]
        return jsonify(objList)


@app_views.route("/users/<user_id>", methods=['DELETE'])
def delete_user(user_id=None):
    """Removes a user"""
    states = storage.all(User).values()
    objList = [obj for obj in states if user_id == obj.id]
    if objList:
        storage.delete(objList[0])
        storage.save()
        return jsonify({})

    abort(404)


@app_views.route("/users/", methods=['POST'])
def create_user():
    """Create a user object"""
    if not request.json:
        abort(400, 'Not a JSON')

    if 'name' not in request.json:
        abort(400, 'Missing name')

    argDict = request.get_json()
    new_user = User(**argDict)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=['PUT'])
def update_user(user_id):
    """Update a user object"""
    if not request.json:
        abort(400, 'Not a JSON')

    ikeys = ['id', 'created_at', 'updated_at']
    users = storage.all(User).values()
    objList = [obj for obj in users if user_id == obj.id]
    if not objList:
        abort(404)

    obj = objList[0]

    argDict = request.get_json()
    for k, v in argDict.items():
        if k not in ikeys:
            setattr(obj, k, v)

    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
