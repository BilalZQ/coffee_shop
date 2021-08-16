"""Constants module for coffee app."""


AUTH0_DOMAIN = 'fsnd-bilal.eu.auth0.com/'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffee-shop'

NOT_FOUND = 404
NO_CONTENT = 204
BAD_REQUEST = 400
CREATED = 201
UNPROCESSABLE_ENTITY = 422
INTERNAL_SERVER_ERROR = 500
METHOD_NOT_ALLOWED = 405
OK = 200
UNAUTHORIZED = 401


ERROR_MESSAGES = {
    NOT_FOUND: 'Resource Not Found',
    BAD_REQUEST: 'Bad Request',
    UNPROCESSABLE_ENTITY: 'Unprocessable Entity',
    INTERNAL_SERVER_ERROR: 'Internal Server Error',
    METHOD_NOT_ALLOWED: 'Method Not Allowed',
    UNAUTHORIZED: 'UNAUTHORIZED'
}
