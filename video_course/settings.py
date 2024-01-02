import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%p3gz$(%5puo(183jo-xyb!#nt=f86b-83w%^@lhct2jbl#@i$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'courses',
    'homepage',
    'accounts',

]

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'video_course.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors':
                [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
        },
    },
]

WSGI_APPLICATION = 'video_course.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mrc_college',
        'USER': 'mrc_college',
        'PASSWORD': 'Hello123456#',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', }, ]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Maximum file size for chunked upload (in bytes)


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

RAZOR_KEY_ID = 'rzp_test_5oHU1szIwHcSIn'
RAZOR_KEY_ID = '0Hp2F9uxYKowoM0j3Ooxlr06'

# PAYU_MERCHANT_KEY = 'vO1XySVD'
# PAYU_MERCHANT_SALT = 'MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCTU2Bku/kWsRM+u1lI0COqkHXW61ir3XJObMsLiPtYgH/T2Uv/EQ5x1g8ltLee6OKEXIzQMqE4dC4tpNxl6iunZNkIQ0awci0PYZk+NO9gbAn8yQvG//84L9gSDKUVzO0ot4rWF8mip4aJcUIaWLHkszST48UVGP27UfE458kgTFz/x8bnJ6et8asvtIEaBityvJuuSBB1nIJa20ZKgA1MFJ+tJFxjlChSdfLVu/f875BN4Y3Y48Nv1NLDGtp15hE1VM0NS6BAw4kBSGkF/I7qMesQtZgCDWvfb9IQ0v2FddGclLDwF7N2ez4tpy+STLkMJNdPGzJnLoYpCFwwV293AgMBAAECggEAHQDfCzXOVd9KcKEldKY1P1DtQgBXFo6kADh+yKiRAt1ZTPWMdox/EX4YwU2QkKI8Zd5qglpVTu3gYXABS7cMHQpHh87mzbnMkSifqJV3Qr5CQRe7T9P6BK+2k+cVYPNVBR0NIhTQx0q/u7MmVlV7wBBfm3XNyNeArC33lUJcYBUcCl3l75HZE9EiC32siahiANohpaBE3SF6vtuKXI6jFI9KW0FFpXS8zxXDOok3hlbdRCiB5xosTSxDm8OkUlI9pk0iQo7qJqjLwVvzQWbce6zf2UBhecCR7WQZlqKV0Lu3ym4k9fuiad6W5KqJMY8aQxvNIbxESZhND/y5lkqVcQKBgQDDVnS4+1J6iqi4ALC+FvWHRR6gsTJWv9Tki+mYh37z2Bwl/s0W4av/Jh7rcU5MSrGTkPwR6XAOidbbYB7AnYAZuKt3GGUmjirGS62IK0b0Q8fyqiZjR+5cMLT3wZtitx++/B+vOO0wie7LfUjPnelHBWrKtUtBbtFfcl94AN4YqwKBgQDBE+qPnkuAH4zuVHErWpbRoZwvS/Asw+Z+LHkYY9zLxKPuQthOJOFoyjDOo3ohU+f17oFwrEQO6gdQ885DtmDO9YXOwpj/o4msKnrDEI7V2Pvbd/ncjAwtmtkIXiKGEJ4MeQ1niqEJ+kyKwIgBgWEHO6nkpgHSxgh+IZJwVA8cZQKBgAjymuImUP7f/x5+mZn7fz+1ANQnicDDhML7TbX47u3IhnGPHGHh8Hj9jAkI5adE/KFf0MwZP1LLKZZe7smv7UBAX0pTSb7cYEU5Djfgk514xV3uQVfm4ZpDeOaoba+157Rd5C2ok+TXTKLxmDY6a4cfTmb+qvXSV7DhklHy6DmFAoGAAQQy0ui5awY/fq2xHtJOQvI/2TvkGsg5OWbQiGFWMzhoyINPkjG9ggi2cxAHP4+qg+/qfIZboVx4B2QRLOgT4GMIfksl9QqOWfqrRMWciuGmicQ6639NPRw4kkO0mNITkus8N9RR/rRznLNgw+lDcn9M6Kg7EDn8p3VTyQWYQsUCgYADomAMvJfPNLnXLQLL2r5hh2GpEq3xyJ3cN6D3THI4Y45hJyQTMM0qs46qV73W7OdH8PlKwzbWs5j+TSm6OCIaGk10It7KHvpIqW0ih9h3PFoMDGgKiBMDX4hiNeejx+Z26STBpihUtJd6VV1RuwEG6F9eU86Ktn6UiqywIJJWow=='
# PAYU_BASE_URL = 'https://secure.payu.in/_payment'  # or 'https://secure.payu.in/_payment' for the production environment
# PAYU_SUCCESS_URL = 'https://mrccollege.com/success/'
# PAYU_FAILURE_URL = 'https://mrccollege.com/'
