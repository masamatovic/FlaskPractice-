from flask import Flask, Blueprint
import config
from api.actuation import ns as actuation_namespace
from api.authentication import ns as users_namespace
from api import api
from db import db

app = Flask(__name__)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = config.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = config.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = config.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = config.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = config.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)
    #blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(flask_app)
    api.add_namespace(actuation_namespace)
    api.add_namespace(users_namespace)
    #flask_app.register_blueprint(blueprint)
    db.init_app(flask_app)


def main():
    initialize_app(app)
    app.run(debug=config.FLASK_DEBUG)


if __name__ == "__main__":
    main()
