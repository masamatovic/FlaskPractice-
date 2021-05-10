from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask_restplus import abort

from models.user import Role
from repository.user_repository import UsersRepository
import config

users_repository = UsersRepository()


def generate_jwt(role: Role, **params):
    """
    Creates valid JWT (Json Web Token) containing the provided data.

    Args:
        role: Role of user related to the token.
        params: Necessary data that should be added to the token.

    Returns:
        Valid JWT authentication token.
    """

    if not role:
        raise ValueError('Could not generate token for unknown role.')

    elif role == Role.ADMIN:
        time_unit, exp_duration = params.get('time_unit'), params.get('exp_duration')
        is_exp_set = time_unit and exp_duration
        return __generate_super_admin_jwt() if not is_exp_set else __generate_super_admin_jwt(time_unit=time_unit,
                                                                                              exp_duration=exp_duration)
    else:
        if not params.get("username"):
            raise ValueError('Unable to generate USER auth token without username specified.')
        return __generate_user_jwt(username=params['username'], role=role.value)


def __generate_super_admin_jwt(time_unit='days', exp_duration=1):
    """
    Creates valid JWT (Json Web Token) used for authentication as SUPER_ADMIN role with validity period of 1 day.

    Returns:
        Valid JWT authentication token.
    """
    token_data = {
        'generated_at_utc': str(datetime.utcnow()),
        'role': Role.ADMIN.value,
        'exp': datetime.utcnow() + timedelta(**{time_unit: exp_duration})
    }

    api_token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    return api_token


def __generate_user_jwt(username: str, role: str):
    """
    Creates valid JWT (Json Web Token) containing the provided data.

    Args:
        username: Username of the existing user.
        role: Corresponding user role.

    Returns:
        Valid JWT authentication token.
    """
    token_data = {
        'username': username,
        'role': role
    }

    api_token = jwt.encode(token_data, config.SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    return api_token


def decode_jwt(api_token):
    """
    Decodes string representing a JWT token. Validation of the token against secret key and algorithm is included.

    Args:
        api_token: JWT token string.

    Returns:
        JWT token content as a json object.
    """
    api_token_data = jwt.decode(api_token, config.SECRET_KEY, algorithms=config.JWT_ALGORITHM, verify=True)
    return api_token_data


def enable_for_roles(request, allowed_roles):
    """
    Check if role of a user related to the provided api_token is contained in the allowed roles for the api route,
    and if not, block the action.

    Args:
        request: HTTP request content.
        allowed_roles: List of user roles allowed to access a route (whitelisting).

    Returns:
        Function that should be executed if role rule is satisfied, otherwise an error function is returned.
    """
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            api_token = get_jwt_from_request(request)
            token_data = get_jwt_data_from_token(api_token)

            try:
                role = Role.get_by_name(token_data['role'])
            except Exception:
                return abort(401, error='Unauthorized for user with no role.')

            if role is None:
                return abort(401, error='Unauthorized for user with no role.')

            if role not in allowed_roles:
                return abort(401, error=f'Unauthorized for role {role.value}.')

            if role not in [Role.ADMIN]:
                try:
                    username = token_data['username']
                except ValueError:
                    return abort(401, error='Unauthorized for user with no username in token.')

                user = users_repository.get_user_by_username(username)
                if not user:
                    return abort(401, error=f'Unknown user with username {username}.')

            return func(args, **kwargs)
        return wrapper
    return inner


def get_jwt_from_request(request):
    """
    Extracts content of authorization header that potentially contains JWT token.

    Args:
        request: Request object containing the header.

    Returns:
        JWT token string if authorization header is present or None if not.
    """
    if not request:
        return None

    if 'Authorization' not in request.headers:
        return None
    else:
        return request.headers['Authorization'].split(' ')[1]


def get_jwt_data_from_request(request):
    """
    Extracts data stored in JWT token.

    Args:
        request: Request object containing the header.

    Returns:
        Decoded JWT token data if token is valid or None if not.
    """

    api_token = get_jwt_from_request(request)
    return get_jwt_data_from_token(api_token=api_token)


def get_jwt_data_from_token(api_token):
    """
    Extracts data stored in JWT token.

    Args:
        api_token: JWT token.

    Returns:
        Decoded JWT token data if token is valid or None if not.
    """

    try:
        return decode_jwt(api_token=api_token)
    except Exception:
        return None