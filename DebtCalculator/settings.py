"""
Django PRODUCTION settings for SpendTrack project.

The environment must provide the following variable:

    SECRET_KEY

                            DB_ENGINE
                            DB_NAME
                            DB_USER
    DATABASE_URL     or     DB_PASSWORD
                            DB_HOST
                            DB_PORT

    CONTACT_GITHUB
    CONTACT_EMAIL
    CONTACT_FACEBOOK

"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = False

######################################
#          DJANGO CONFIG             #
######################################

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debtcalculatorapp.apps.DebtcalculatorappConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DebtCalculator.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'DebtCalculator.wsgi.application'

SECURE_SSL_REDIRECT = True

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT')
    }
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Login logout

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

LOGIN_URL = '/login'

######################################
#             APP CONFIG             #
######################################

APP_VERSION = "1.1"

CONTACT_GITHUB = 'https://github.com/' + os.environ.get('CONTACT_GITHUB')

CONTACT_EMAIL = 'mailto:' + os.environ.get('CONTACT_EMAIL')

CONTACT_FACEBOOK = 'https://www.facebook.com/' + os.environ.get('CONTACT_FACEBOOK')

PAGE_SIZE = 7

######################################
#     HEROKU DEPLOYMENT CONFIG       #
######################################

import django_heroku

django_heroku.settings(locals())
