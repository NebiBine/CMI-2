from flask import Blueprint, request, jsonify

dataBp = Blueprint("data", __name__, url_prefix="/data")

@dataBp.route("/test", methods=["POST"])
def test():
    pass