"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }
    if response_body:
        return jsonify(response_body), 200
    if response_body is None:
        return jsonify({"Message": "List is empty"}), 400
    else:
        return jsonify({"Message": "Server error"}), 500


@app.route('/members/<int:id>', methods=['GET'])
def handle_member_id(id):

    member = jackson_family.get_member(id)
    if member:
        response_body = member
        return jsonify(response_body), 200
    if member is None:
        return jsonify("incorrect ID"), 400
    else:
        return jsonify("server error"), 500


@app.route('/member', methods=['POST'])
def handle_new_member():
    member = request.get_json()
    if member["first_name"] is None or member["last_name"] is None or member["age"] is None or member["lucky numbers"] is None:
        return jsonify({"Message": "Incorrect information"}), 400
    if member:
        jackson_family.add_member(member)
        return jsonify({"Message": "Member created"}), 200
    else:
        return jsonify({"Message": "Server error"}), 500


@app.route('/member/<int:member_id>', methods=['DELETE'])
def handle_delete_member(member_id):
    resultado = jackson_family.delete_member(member_id)
    if resultado == "eliminado":
        return jsonify({"Message": "Member deleted"}), 200
    if resultado == "no se encontro el elemento":
        return jsonify({"Message": "Member not found"}), 400
    else:
        return jsonify(), 500


    # this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
