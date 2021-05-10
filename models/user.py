import enum

from db import db


class Role(str, enum.Enum):

    TEST = "TEST"
    ADMIN = "ADMIN"

    @classmethod
    def get_by_name(cls, name):
        for elem in cls:
            if elem.value == name:
                return elem
        return None


class Users(db.Model):

    __tablename__ = 'users'
    __tableargs__ = {'schema': 'public'}

    user_id = db.Column(db.INTEGER(), primary_key=True, default=db.Sequence("user_id_seq"))
    username = db.Column(db.TEXT(), primary_key=True)
    password = db.Column(db.TEXT())
    name = db.Column(db.TEXT())
    last_name = db.Column(db.TEXT())
    client_id = db.Column(db.INTEGER())
    role = db.Column(db.Enum(Role), nullable=False)


