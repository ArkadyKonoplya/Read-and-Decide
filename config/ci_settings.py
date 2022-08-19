import os

from .settings import *

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "telepsycrx_test",
        "USER": str(os.environ.get("DATABASE_USER")),
        "PASSWORD": str(os.environ.get("DATABASE_PASSWORD")),
        "HOST": str(os.environ.get("DATABASE_HOST")),
        "PORT": "5432",
    }
}

CACHES = {
    # In tests, we use the dummy cache, which does nothing. This is so that
    # test results aren't affected by operations being cached between test
    # runs. If in the future we have tests that actually test cache
    # functionality, we would have to update this, but currently we do not have
    # any such tests.
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    },
}

IGNORE_CACHE_ERRORS = True
