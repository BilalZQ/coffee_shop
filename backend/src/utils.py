"""Module for utils."""

from flask import jsonify
from .constants import ERROR_MESSAGES


def error_response(http_status):
    """
    Get error response based on http status.
    :param http_status:
    :return:
    """
    return jsonify({
        "success": False,
        "error": http_status,
        "message": ERROR_MESSAGES[http_status]
        }), http_status