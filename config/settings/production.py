from .base import *  # noqa: F403,F401

DEBUG = False

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "")  # noqa: F405

SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", True)  # noqa: F405
SESSION_COOKIE_SECURE = env_bool("SESSION_COOKIE_SECURE", True)  # noqa: F405
CSRF_COOKIE_SECURE = env_bool("CSRF_COOKIE_SECURE", True)  # noqa: F405
