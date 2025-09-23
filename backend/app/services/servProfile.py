from .servProfileDb import newProfile
from flask import jsonify

def servNewProfile(userId, name, username, birth, phone, street, city, country, zip):
    try:
        newProfile(userId, name, username, birth, phone, street, city, country, zip)
        return jsonify({"success": True, "message":"Profile added!"}), 200
    except:
        return jsonify({"success": False, "message": "Error with adding the profile!"}), 500
    