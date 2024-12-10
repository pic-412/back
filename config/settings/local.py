from .base import *

SECRET_KEY = env("LOCAL_SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("LOCAL_DB_NAME"),
        "USER": env("LOCAL_DB_USER"),
        "PASSWORD": env("LOCAL_DB_PASSWORD"),
        "HOST": env("LOCAL_DB_HOST"),
        "PORT": env("LOCAL_DB_PORT"),
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}
