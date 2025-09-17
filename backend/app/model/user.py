from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self,username, email, passwordHash = None, id=None):
        self.id = id
        self.username = username
        self.email = email
        self.passwordHash = passwordHash

    def hashPassword(self, password):
        self.passwordHash = generate_password_hash(password)

    
    def checkPassword(self, password):
        return check_password_hash(self.passwordHash, password)