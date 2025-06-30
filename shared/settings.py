import os


BASE_URL = "http://co_nginx/"

REDIS_URL = os.getenv("REDIS_URL")

AUTH_SERVICE_URL = BASE_URL + "auth/"
SOCIAL_SERVICE_URL = BASE_URL + "social/"
MEDIA_SERVICE_URL = BASE_URL + "media/"

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "some-default")

DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    var for var in os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "co_task_db",
        "USER": "co_user",
        "PASSWORD": "co_pass",
        "HOST": "co_postgres",
        "PORT": 5432,
    }
}
