from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200
    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data:
        for pic in data:
            if pic['id'] == id:
                return jsonify(pic), 200
        return {"message": "picture not found"}, 404
    return {"message": "Internal server error"}, 500


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    pic = request.json
    if not pic:
        return {"message": "picture content missing"}, 204
    for p in data:
        if p['id'] == pic['id']:
            return {"Message": "picture with id "+str(pic['id'])+" already present"}, 302
    data.append(pic)
    return pic, 201

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pic = request.json
    if not pic:
        return {"Message": "picture content missing"}, 204
    foundPicture = False
    for i in range(len(data)):
        if data[i]['id'] == pic['id']:
            data[i] = pic
            foundPicture = True
    if not foundPicture:
        return {"Message": "picture not found"}, 404
    return pic, 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for p in data:
        if p['id'] == id:
            data.remove(p)
            return {}, 204
    return {"message": "picture not found"}, 404
