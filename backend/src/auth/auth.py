"""Module for auth."""

import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

from constants import (
    AUTH0_DOMAIN, ALGORITHMS, API_AUDIENCE,
    ERROR_MESSAGES, UNAUTHORIZED, BAD_REQUEST
)


class AuthError(Exception):
    """A standardized way to comminucate auth failure modes."""

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def auth_error(msg, err):
    """
    Auth error.

    :param msg:
    :return:
    """
    raise AuthError({
        'success': False,
        'message': msg,
        'error': err
    }, err)


def get_token_auth_header():
    """
    Get token from authorization header.

    :return:
    """
    header = request.headers.get('Authorization')
    if not header:
        auth_error('Authorization header is required', UNAUTHORIZED)

    headers_arr = header.split(' ')

    if header[0].lower() != 'bearer':
        auth_error('Header expected to have "Bearer before token"', UNAUTHORIZED)
    elif len(headers_arr) != 2:
        auth_error(
            'Authorization is expected to be in following format: "Bearer <Token>"',
            UNAUTHORIZED)

    return headers_arr[1] # Token


def check_permissions(permission, payload):
    """
    Check permissions.

    :param permission:
    :param payload:
    :return:
    """

    if 'permission' in payload and permission in payload['permission']:
        return True

    auth_error(UNAUTHORIZED, ERROR_MESSAGES[UNAUTHORIZED])


def verify_decode_jwt(token):
    """
    Verify jwt integrity is reserved.

    :param token:
    :return:
    """
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    rsa_key = {}

    unverified_header = jwt.get_unverified_header(token)
    if 'kid' not in unverified_header:
        auth_error('Authorization malformed.', UNAUTHORIZED)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            auth_error('Token expired.', UNAUTHORIZED)

        except jwt.JWTClaimsError:
            auth_error(
                'Incorrect claims. Please, check the audience and issuer.', UNAUTHORIZED)
        except Exception:
            auth_error('Unable to parse authentication token.', BAD_REQUEST)

    auth_error('Unable to find the appropriate key..', BAD_REQUEST)


def requires_auth(permission=''):
    """
    Require auth.

    :param permission:
    :return:
    """
    def requires_auth_decorator(f):
        """
        Require auth decorator.

        :param f:
        :return:
        """
        @wraps(f)
        def wrapper(*args, **kwargs):
            """
            Wrapper method.

            :param args:
            :param kwargs:
            :return:
            """
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator