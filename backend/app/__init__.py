from flask import Flask

def createApp():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "123"

    from app.routes.authRoutes import authBp
    app.register_blueprint(authBp)

    from app.routes.dataRoutes import dataBp
    app.register_blueprint(dataBp)

    return app