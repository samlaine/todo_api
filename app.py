"""Entry point for the api"""

import logging
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from handlers import RegisterUser, LoginUser, GetTodos, PostTodos, ModifyTodos
from settings import (
    DB,
    ENV,
    PORT,
    CONSOLE_FORMAT,
    CONSOLE_DATE_FORMAT,
    LOGGING_LEVEL,
    APP_CONFIGURATION,
)

app = Flask(__name__)


def _configure_app(config):
    """Fill app.config"""
    for key, value in config:
        app.config[key] = value
    return app


@app.before_first_request
def create_tables():
    """create local database if it doesn't exist"""
    if ENV == "local":
        DB.create_all()


def _init_logging(text_format: str, date_format: str, level: str) -> None:
    """configure logger"""
    logging.basicConfig(level=level)
    log_handler = logging.StreamHandler()
    formatter = logging.Formatter(text_format, date_format)
    log_handler.setFormatter(formatter)


_init_logging(CONSOLE_FORMAT, CONSOLE_DATE_FORMAT, LOGGING_LEVEL)
_configure_app(APP_CONFIGURATION)

logger = logging.getLogger(__name__)
api = Api(app)
jwt = JWTManager(app)


@jwt.expired_token_loader
def expired_token_handler_callback(expired_token):
    """set response status and body for when jwt token expires"""
    token_type = expired_token["type"]
    return jsonify({"status": 401, "message": f"{token_type}_token_expired"}), 401


# routes
api.add_resource(RegisterUser, "/register")
api.add_resource(LoginUser, "/authenticate")

api.add_resource(GetTodos, "/todos")
api.add_resource(PostTodos, "/todo")
api.add_resource(ModifyTodos, "/todo/<string:todo_id>")


if __name__ == "__main__":
    debug = ENV != "prod"
    DB.init_app(app)
    app.run(port=PORT, debug=debug)
