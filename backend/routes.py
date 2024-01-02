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
   """Return all pictures"""
   if data:
       return jsonify(data), 200

   return {"message": "No pictures found"}, 404


######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
   """Return picture with given id"""
   for item in data:
       if item['id'] == id:
           return jsonify(item), 200

   return {"message": f"Picture with id {id} not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
  """Create a new picture"""
  picture = request.get_json()

  for item in data:
      if item['id'] == picture['id']:
          return {"Message": f"picture with id {picture['id']} already present"}, 302

  data.append(picture)
  return jsonify(picture), 201


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
  """Update a picture"""
  updated_picture = request.get_json()

  for i, item in enumerate(data):
      if item['id'] == id:
          data[i] = updated_picture
          return jsonify(updated_picture), 200

  return {"message": "picture not found"}, 404


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
 """Delete a picture"""
 for i, item in enumerate(data):
     if item['id'] == id:
         del data[i]
         return '', 204

 return {"message": "picture not found"}, 404

