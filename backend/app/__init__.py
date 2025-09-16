from flask import Flask

def createApp():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "123"
    from app.routes.authRoutes import authBp
    app.register_blueprint(authBp)
    return app