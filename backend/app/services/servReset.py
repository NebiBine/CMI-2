from datetime import datetime, timedelta
from .servAuthDb import requestReset, getResetId, delResetId, newPassword
from .servEmail import sendEmail
from werkzeug.security import generate_password_hash
from flask import jsonify

def requestPassReset(email, resetId, link):
    expire = datetime.now() + timedelta(hours=1) # aktivn bo eno uro
    try:
        requestReset(resetId, email, expire)
        print("reset v db")
    except:
        return jsonify({"success": False, "message": "DB error with requesting a reset!"}), 500
    try:
        sendEmail(email, link)
        print("email poslan")
    except:
        return jsonify({"success": False, "message": "Sendgrid error with sending an email"}), 500
    return jsonify({"success":True, "message": "Reset email sent successfully!"}), 200

def resetPassword(resetId, password):
    try:
        uporabnik = getResetId(resetId)
    except:
        print("error v get resetId")
    if not uporabnik:
        return jsonify({"success:": False, "message": "account does not exist yet!"}),500
    
    if datetime.now() > datetime.fromisoformat(uporabnik["expire"]):
        try:
            delResetId(resetId)
            print("expired")
        except:
            return jsonify({"success": False, "message": "error in del ResetId"}), 500

    hashPass = generate_password_hash(password)
    print("hashpass v resetpassword"+ hashPass)
    try:
        newPassword(hashPass, uporabnik["email"])
        delResetId(resetId)
    except:
        return jsonify({"success": True, "message": "erorr in updating password!"}), 500
    return jsonify({"success": True, "message": "password reseted successfuly!"})