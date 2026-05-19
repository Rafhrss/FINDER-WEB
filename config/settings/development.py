from .base import *  # noqa: F403,F401

DEBUG = True

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "127.0.0.1,localhost")  # noqa: F405

REST_FRAMEWORK = {
    **REST_FRAMEWORK,  # noqa: F405
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
}
