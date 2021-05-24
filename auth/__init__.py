import os
from flask import request
from flask.json import jsonify
from functools import wraps
from dotenv import load_dotenv
from urllib.request import urlopen
from icecream import ic
from jose import jwt
import json

load_dotenv()


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    if "Authorization" not in request.headers:
        raise AuthError(
            {"code": "not_found", "description": "Bearer Token Not Found"}, 401
        )

    authString = request.headers["Authorization"]
    parts = authString.split(" ")
    if parts[0] != "Bearer" or len(parts) != 2:
        raise AuthError(
            {"code": "invalid_token", "description": "Invalid Bearer Token"},
            401,
        )

    jwtToken = parts[1]
    components = jwtToken.split(".")
    if len(components) != 3:
        raise AuthError(
            {"code": "invalid_token", "description": "Invalid Bearer Token"},
            401,
        )

    return jwtToken


def verify_decode_jwt(token):
    # Get JSON web key set (jwks) from Auth0
    jsonurl = urlopen(
        "https://{}/.well-known/jwks.json".format(os.environ["AUTH0_DOMAIN"])
    )
    jwks = json.loads(jsonurl.read())

    # Read token header
    unverified_header = jwt.get_unverified_header(token)

    # Ensure the unique identifier for the key existed
    if "kid" not in unverified_header:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Unable to parse authentication token",
            },
            401,
        )

    # Find the correct key set
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
            break

    if rsa_key == {}:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Unable to find the appropriate key.",
            },
            401,
        )

    try:
        payload = jwt.decode(
            token,
            key=rsa_key,
            algorithms=[os.environ["AUTH0_ALGORITHM"]],
            audience=os.environ["AUTH0_IDENTIFIER"],
            issuer="https://{}/".format(os.environ["AUTH0_DOMAIN"]),
        )

        return payload
    except jwt.ExpiredSignatureError:
        raise AuthError({"code": "token_expired", "description": "Token expired."}, 401)

    except jwt.JWTClaimsError:
        raise AuthError(
            {
                "code": "invalid_claims",
                "description": "Incorrect claims. Please, check the audience and issuer.",
            },
            401,
        )
    except Exception:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Unable to parse authentication token",
            },
            401,
        )


def check_permissions(permission, payload):
    if "permissions" not in payload:
        raise AuthError(
            {
                "code": "invalid_token_playload",
                "description": "Missing permissions",
            },
            401,
        )

    if permission == "":
        return True

    if permission in payload["permissions"]:
        return True

    raise AuthError(
        {"code": "unauthorized", "description": "Permission not granted"},
        403,
    )


def requires_auth(permission=""):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
