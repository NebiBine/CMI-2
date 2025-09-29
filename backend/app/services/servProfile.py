from .servProfileDb import newProfile
from flask import jsonify
import os

def servNewProfile(userId, name, username, birth, phone, street, city, country, zip, pfp):
    try:
        pfpDir = os.path.join("databases", "pfps")
        os.makedirs(pfpDir, exist_ok=True)
        extension = os.path.splitext(pfp.filename)[1]
        pfpName = f"pfp{userId}{extension}"
        pfpPath = os.path.join(pfpDir, pfpName)
        pfp.save(pfpPath)
        pfpPathg = f"../../databases/pfps{pfpName}"
    except:
        pass
        
    try:
        newProfile(userId, name, username, birth, phone, street, city, country, zip, pfpPath)
        return jsonify({"success": True, "message":"Profile added!"}), 200
    except:
        return jsonify({"success": False, "message": "Error with adding the profile!"}), 501
    