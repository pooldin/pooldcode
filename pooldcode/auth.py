from functools import wraps
from flask import request, Response
from flask import current_app as app


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    _username = app.config.get('AUTH_USERNAME')
    _password = app.config.get('AUTH_PASSWORD')
    is_username = username == _username
    is_password = password == _password
    return _username and is_username and _password and is_password


def authenticate():
    msg = 'Could not verify your access level.\n' + \
          'You have to login with proper credentials.'

    return Response(msg, 401, {
        'WWW-Authenticate': 'Basic realm="Login Required"'
    })


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
