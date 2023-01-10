from flask import make_response, jsonify
from app.api import bp
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES



def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return make_response(response, status_code)


def bad_request(message):
    return error_response(400, message)

from flask import json
from werkzeug.exceptions import HTTPException

# @bp.errorhandler(HTTPException)
# def handle_exception(e):
#     """Return JSON instead of HTML for HTTP errors."""
#     # start with the correct headers and status code from the error
#     response = e.get_response()
#     # replace the body with JSON
#     response.data = json.dumps({
#         "code": e.code,
#         "name": e.name,
#         "description": e.description,
#     })
#     response.content_type = "application/json"
#     return response

@bp.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({"message": e.description}), e.code