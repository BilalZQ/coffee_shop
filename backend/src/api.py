import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth
from .utils import error_response
from .constants import (
    NOT_FOUND, NO_CONTENT, BAD_REQUEST, CREATED, UNPROCESSABLE_ENTITY,
    INTERNAL_SERVER_ERROR, METHOD_NOT_ALLOWED, UNAUTHORIZED
)

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES
@app.route('/drinks')
def get_drinks():
    """
    Public endpoint to drinks.

    :return:
    """
    return jsonify({
        'success': True,
        'drinks': [drink.short() for drink in Drink.query.all()]
    })


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(token):
    """
    Get drinks with details.

    :param token:
    :return:
    """
    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in Drink.query.all()]
    })


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(token):
    """
    Add new drink.

    :param token:
    :return:
    """
    try:
        data = request.get_json()
        drink = Drink(title=data.get('title'), recipe=json.dumps(data.get('recipe')))
        drink.insert()
        return jsonify({
            'success': True,
            'drink': drink.long()
        })
    except Exception:
        abort(BAD_REQUEST)


@app.route('/drinks/<drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(token, drink_id):
    """
    Update drink.

    :param token:
    :param drink_id:
    :return:
    """
    try:
        drink = Drink.query.filter_by(id=drink_id).first()
        if not drink:
            abort(NOT_FOUND)

        data = request.get_json()
        drink.title = data.get('title')
        drink.recipe = json.dumps(data.get('recipe'))
        drink.update()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except Exception:
        abort(BAD_REQUEST)


@app.route('/drinks/<drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(token, drink_id):
    """
    Delete drink.

    :param token:
    :param drink_id:
    :return:
    """
    try:
        drink = Drink.query.filter_by(id=drink_id).first()
        if not drink:
            abort(NOT_FOUND)

        drink.delete()

        return jsonify({
            'success': True,
            'delete': drink_id
        })
    except Exception:
        abort(BAD_REQUEST)


# Error Handling
@app.errorhandler(AuthError)
def auth_error(error):
    """
    Error handling for our custom auth error class.
    :param error:
    :return:
    """
    return jsonify(error.error), error.status_code


@app.errorhandler(UNAUTHORIZED)
def not_found(error):
    """
    Error handler for status code 401.
    :param error:
    :return:
    """
    return error_response(UNAUTHORIZED)


@app.errorhandler(NOT_FOUND)
def not_found(error):
    """
    Error handler for status code 404.
    :param error:
    :return:
    """
    return error_response(NOT_FOUND)


@app.errorhandler(BAD_REQUEST)
def bad_request(error):
    """
    Error handler for status code 400.
    :param error:
    :return:
    """
    return error_response(BAD_REQUEST)


@app.errorhandler(UNPROCESSABLE_ENTITY)
def unprocessable_entity(error):
    """
    Error handler for status code 422.
    :param error:
    :return:
    """
    return error_response(UNPROCESSABLE_ENTITY)


@app.errorhandler(INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """
    Error handler for status code 500.
    :param error:
    :return:
    """
    return error_response(INTERNAL_SERVER_ERROR)


@app.errorhandler(METHOD_NOT_ALLOWED)
def method_not_allowed(error):
    """
    Error handler for status code 405.
    :param error:
    :return:
    """
    return error_response(METHOD_NOT_ALLOWED)
