from flask import Flask

def createApp():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "123"
    return app