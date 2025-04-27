from flask import jsonify


def success(message=None, data=None):
    response = {"status": "success"}
    if message is not None:
        response["message"] = message
    if data is not None:
        response["data"] = data
    return jsonify(response)


def error(message=None):
    response = {"status": "error"}
    if message is not None:
        response["message"] = message
    else:
        response["message"] = "An error occurred"
    return jsonify(response), 400
