from db import db
from models.user import Users


class UsersRepository:

    @staticmethod
    def get_user_by_username(username: str):
        user = Users.query.filter_by(
            username=username
        ).first()

        return user
