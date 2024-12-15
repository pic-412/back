from .base import *

SECRET_KEY = env("PROD_SECRET_KEY")
DEBUG = False

ALLOWED_HOSTS = ["*"]
# CORS_ORIGIN_WHITELIST = ("http://211.188.59.221/",)
CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGIN_REGEXES = [
#     r"^https://\w+\.example\.com$",
# ]
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

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