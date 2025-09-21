from datetime import datetime, timedelta
from .servDb import requestReset, getResetId, delResetId, newPassword
from .servEmail import sendEmail
from werkzeug.security import generate_password_hash

def requestPassReset(email, resetId, link):
    expire = datetime.now() + timedelta(hours=1) # aktivn bo eno uro
    requestReset(resetId, email, expire)
    sendEmail(email, link)
    return "dela"

def resetPassword(resetId, password):
    uporabnik = getResetId(resetId)
    if not uporabnik:
        return "invalid or expired Id"
    
    if datetime.now() > datetime.fromisoformat(uporabnik["expire"]):
        delResetId(resetId)

    hashPass = generate_password_hash(password)
    newPassword(uporabnik["email"], hashPass)
    delResetId(resetId)
    return "dela"