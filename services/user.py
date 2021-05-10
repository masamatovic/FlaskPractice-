from passlib.hash import sha256_crypt

from db import db
from models.user import Users, Role
from . import user_repository
from auth_utils import generate_jwt


class UserService:
    def __init__(self):
        pass

    @staticmethod
    def create_user(username, password, name, last_name):

        new_user = user_repository.get_user_by_username(username)
        if new_user:
            raise Exception("There is already a user with this username.")

        new_user = Users()
        new_user.username = username
        new_user.password = sha256_crypt.encrypt(password)
        new_user.name = name
        new_user.last_name = last_name
        new_user.role = Role.TEST
        new_user.client_id = 1
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            return None

        return {
            'name': new_user.name,
            'last_name': new_user.last_name,
            'role': new_user.role.value
        }

    @staticmethod
    def login(username, password):

        user = user_repository.get_user_by_username(username)

        has_valid_password = user is not None and sha256_crypt.verify(password, user.password)

        if not has_valid_password:
            raise Exception("No user with specified credentials in the DB.")

        api_token = generate_jwt(role=user.role, username=username)
        return {
            'api_token': api_token,
            'name': user.name,
            'last_name': user.last_name,
            'role': user.role.value if user.role else None
        }
