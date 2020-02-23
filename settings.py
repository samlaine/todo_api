""" general settings for the api """

import logging
import os
import sys
from datetime import timedelta

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger()

_VALID_ENVS = ["local", "test", "stg", "prod"]
_SQLALCHEMY_TRACK_MODIFICATIONS = False
_JWT_TOKEN_EXPIRATION_DAYS = 1
_JWT_AUTH_USERNAME_KEY = "email"

ENV = os.getenv("ENVIRONMENT")
if ENV not in _VALID_ENVS:
    logger.error(
        f"{ENV} is not valid environment, valid environments are: {_VALID_ENVS}"
    )
    sys.exit(1)

logger.info("ENVIRONMENT is '%s'", ENV)
load_dotenv(f"./{ENV}.env")

# general
PORT = os.getenv("PORT")

# logging configuration
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL")
CONSOLE_FORMAT = os.getenv("CONSOLE_FORMAT")
CONSOLE_DATE_FORMAT = os.getenv("CONSOLE_DATE_FORMAT")

# init SQLAlchemy
DB = SQLAlchemy()

# SQLAlchemy & JWT
APP_CONFIGURATION = [
    ("SQLALCHEMY_DATABASE_URI", os.getenv("DATABASE_URI")),
    ("SQLALCHEMY_TRACK_MODIFICATIONS", _SQLALCHEMY_TRACK_MODIFICATIONS),
    ("JWT_SECRET_KEY", os.getenv("SECRET_KEY")),
    ("JWT_ACCESS_TOKEN_EXPIRES", timedelta(days=_JWT_TOKEN_EXPIRATION_DAYS)),
    ("JWT_AUTH_USERNAME_KEY", _JWT_AUTH_USERNAME_KEY),
]

