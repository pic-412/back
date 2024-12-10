from .base import *

SECRET_KEY = env("PROD_SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ["211.188.59.221"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("PROD_DB_NAME"),
        "USER": env("PROD_DB_USER"),
        "PASSWORD": env("PROD_DB_PASSWORD"),
        "HOST": env("PROD_DB_HOST"),
        "PORT": env("PROD_DB_PORT"),
    }
}

CORS_ORIGIN_WHITELIST = ("http://211.188.59.221/",)