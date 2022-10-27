import json
from functools import wraps
from urllib.request import urlopen

from flask import request
from jose import jwt

AUTH0_DOMAIN = 'dev-xr6hy7tkensllyoz.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'my-school'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header


def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'Missing Authorization Header',
            'description': 'Authorization header is expected.'
        }, 401)
    else:
        parts = auth.split()
        if parts[0].upper() != 'BEARER':
            raise AuthError({
                'code': 'Invalid Header',
                'description': 'Authorization header must start with "Bearer".'
            }, 401)
        elif len(parts) == 1:
            raise AuthError({
                'code': 'Invalid Header',
                'description': 'Authorization header must be bearer token.'
            }, 401)
        elif len(parts) > 2:
            raise AuthError({
                'code': 'Invalid Header',
                'description': 'Authorization header must be bearer token.'
            }, 401)
        token = parts[1]
        if not token:
            raise AuthError({
                'code': 'Invalid Header',
                'description': 'Token not found.'
            }, 401)

        return token


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'Invalid Header',
            'description': 'Permissions not included in JWT.'
        }, 400)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'Unauthorized',
            'description': 'Permission not found.'
        }, 403)

    return True


def verify_decode_jwt(token):
    url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(url.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'Invalid Header',
            'description': 'Authorization malformed.'
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
            raise AuthError({
                'code': 'Token Expired',
                'description': ''
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'Invalid Claims',
                'description': 'Incorrect claims'
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'Invalid Header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'Invalid Header',
        'description': 'Unable to find the appropriate key.'
    }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
