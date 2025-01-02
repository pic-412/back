from pathlib import Path
from datetime import timedelta
import environ
import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(env_file=os.path.join(BASE_DIR, ".env"))


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "corsheaders",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.kakao",
    "pic.accounts",
    "pic.places",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

ASGI_APPLICATION = "config.asgi.application"

AUTH_USER_MODEL = "accounts.User"


# Password validation https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend"
]


LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True


STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"


MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"


DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}

SPECTACULAR_SETTINGS = {
    # https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#openapi-object
    'TITLE': 'Pic046 API Document',
    'DESCRIPTION': 'drf-specatular 를 사용해서 만든 API 문서입니다.',
    'CONTACT': {'name': 'test', 'url': 'http://www.example.com/support', 'email': 'test@gmail.com'},
    'SWAGGER_UI_SETTINGS': {
        # https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/
        'dom_id': '#swagger-ui',
        'layout': 'BaseLayout',
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
        'filter': True,
    },
    # Optional: MUST contain "name", MAY contain URL
    'LICENSE': {
        'name': 'pic064 License',
        'url': 'https://github.com/pic-412/back/main/LICENSE',
    },
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # https://www.npmjs.com/package/swagger-ui-dist
    'SWAGGER_UI_DIST': '//unpkg.com/swagger-ui-dist@3.38.0',
}

SITE_ID = 1

KAKAO_REST_API_KEY = env("KAKAO_REST_API_KEY")

SOCIALACCOUNT_PROVIDERS = {
    'kakao': {
        'APP': {
            'client_id': KAKAO_REST_API_KEY,
            },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'}
        }
    }

SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = True 