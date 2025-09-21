from werkzeug.security import generate_password_hash
class ForgotResetPasswordUser:
    def __init__(self,email, passwordHash = None):
        self.email = email
        self.passwordHash = passwordHash

    def hashPassword(self, password):
        self.passwordHash = generate_password_hash(password)