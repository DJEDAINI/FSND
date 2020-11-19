import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'a-djedaini.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'fsnd'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
Return the Access Token from the Authorization Header
'''
def get_token_auth_header():
    authorization = request.headers.get('Authorization', None)
    if not authorization:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is missing.'
        }, 401)

    parts = authorization.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'authorization_header_malformed',
            'description': 'Authorization header malformed, Bearer string is required.'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'authorization_header_malformed',
            'description': 'Authorization header malformed, No token provided.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'authorization_header_malformed',
            'description': 'Authorization header malformed, Bearer token should be submitted.'
        }, 401)

    token = parts[1]
    return token

'''
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    raise an AuthError if permissions are not included in the payload
    raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions parameter in required in JWT payload.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Unauthorized access.'
        }, 403)
    return True

'''
    @INPUTS
        token: a json web token (string)

    should be an Auth0 token with key id (kid)
    should verify the token using Auth0 /.well-known/jwks.json
    should decode the payload from the token
    should validate the claims
    return the decoded payload
'''
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
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
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


'''
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    use the get_token_auth_header method to get the token
    use the verify_decode_jwt method to decode the jwt
    use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except:
                abort(401)

            check_permissions(permission, payload)

            return f(*args, **kwargs)
            # return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator