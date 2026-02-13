from datetime import timedelta
from pathlib import Path
from typing import Any, Dict, cast

import dj_database_url
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

SECRET_KEY = config("SECRET_KEY", default="dev-key-change-in-production")
DEBUG = config("DEBUG", default=False, cast=bool)
_allowed_hosts_str = cast(str, config("ALLOWED_HOSTS", default="", cast=str))
ALLOWED_HOSTS = [host.strip() for host in _allowed_hosts_str.split(",") if host.strip()]

# Add localhost for development when DEBUG is True
if DEBUG and not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]
# In production, allow localhost/127.0.0.1 for in-container healthchecks
if not DEBUG and ALLOWED_HOSTS:
    for h in ("localhost", "127.0.0.1"):
        if h not in ALLOWED_HOSTS:
            ALLOWED_HOSTS = list(ALLOWED_HOSTS) + [h]

# Security headers (only enabled in production with HTTPS)
if DEBUG:
    # Explicitly disable HTTPS/SSL settings in development
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0  # Disable HSTS in development
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
else:
    # Production: Enable HTTPS when SSL is configured (set SECURE_SSL_REDIRECT=true after certbot)
    SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=False, cast=bool)
    SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=True, cast=bool)
    CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=True, cast=bool)
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    # HSTS - only if SSL is properly configured
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Owned apps
    "motion",
    "user",
    "user_profile",
    "follow",
    "post",
    "image",
    # Third party apps
    "rest_framework",
    "drf_yasg",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "motion.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "motion.wsgi.application"


# Database - Use PostgreSQL in production
_database_url = config("DATABASE_URL", default=None)
if _database_url:
    # Parse database URL and add SSL requirements for cloud databases
    db_config = cast(
        Dict[str, Any], dj_database_url.config(default=cast(str, _database_url))
    )
    # Add SSL requirement for PostgreSQL (required by Render, Heroku, etc.)
    if db_config.get("ENGINE") == "django.db.backends.postgresql":
        # Configure SSL for PostgreSQL connections
        options: Dict[str, Any] = db_config.get("OPTIONS", {}) or {}
        # Only require SSL in production (local Docker doesn't support SSL)
        # In development, use prefer (will use SSL if available, but won't fail if not)
        if not DEBUG:
            options["sslmode"] = "require"
        elif "sslmode" not in options:
            # In development, prefer SSL but don't require it
            options["sslmode"] = "prefer"

        # Use PostgreSQL schema to isolate this project's tables when sharing a database
        # Set DB_SCHEMA environment variable (default: "test")
        # This allows multiple Django projects to share the same PostgreSQL database
        db_schema = config("DB_SCHEMA", default="test")
        if db_schema:
            # Set search_path to use the schema for all queries
            # This ensures all tables are created and accessed in the specified schema
            # Format: "-c option=value" for PostgreSQL connection options
            existing_options = options.get("options", "")
            search_path_option = f"-c search_path={db_schema},public"
            if existing_options:
                options["options"] = f"{existing_options} {search_path_option}"
            else:
                options["options"] = search_path_option

        db_config["OPTIONS"] = options
    DATABASES = {"default": db_config}
else:
    # Development: SQLite3
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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

# user should be the name of your app, User should be the name of your model
AUTH_USER_MODEL = "user.User"


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "motion.authentication.JWTAuthenticationWithoutBearer",
    ],
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "recipe": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}


SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter your JWT token (without 'Bearer' prefix)",
        }
    },
    "PERSIST_AUTH": True,
}
