import json
import os
import sys
from flask import request, _request_ctx_stack, abort, session
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from os import environ

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = os.getenv('ALGORITHMS')
AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')


# AuthError Exception
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header: Obtains the Access Token from the Authorization Header
def get_token_auth_header():
    if "Authorization" in request.headers:
        auth_header = request.headers["Authorization"]
        if auth_header:
            bearer_token_array = auth_header.split(' ')
            if (bearer_token_array[0] and
                    bearer_token_array[0].lower() == "bearer" and
                    bearer_token_array[1]):
                return bearer_token_array[1]

    raise AuthError({
        'success': False,
        'message': 'JWT not found',
        'error': 401
    }, 401)


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        print('permissions not in payload')
        abort(400)

    if permission not in payload['permissions']:
        print(f'{permission} not in {payload["permissions"]}')
        raise AuthError({
            'success': False,
            'message': 'Permission not found in JWT',
            'error': 401
        }, 401)

    return True


def verify_decode_jwt(token):
    """Decodes and verifies the provided token
    Args:token
    Returns: the decoded payload of the token
    """
    # get the public key from Auth0
    AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
    ALGORITHMS = os.getenv('ALGORITHMS')
    AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')
    print(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # get the data in the header
    unverified_header = jwt.get_unverified_header(token)
    # choose key
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'success': False,
            'message': 'Authorization malformed',
            'error': 401,
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    # Finally, verify
    if rsa_key:
        print('rsa_key exists')
        try:
            # use the key to validate the JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=AUTH0_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'success': False,
                'message': 'Token expired',
                'error': 401,
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'success': False,
                'message': 'Incorrect claims.',
                'error': 401,
            }, 401)

        except Exception:
            raise AuthError({
                'success': False,
                'message': 'Unable to parse authentication token',
                'error': 400,
            }, 400)

    raise AuthError({
        'success': False,
        'message': 'Unable to find the appropriate key',
        'error': 400,
    }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = None
                if "Test" in request.headers:
                    token = get_token_auth_header()
                elif session['token']:
                    token = session['token']
                else:
                    token = get_token_auth_header()
                if token is None:
                    abort(400)
                payload = verify_decode_jwt(token)
                
                return f(payload, *args, **kwargs)
            except Exception:
                abort(401)

        return wrapper
    return requires_auth_decorator