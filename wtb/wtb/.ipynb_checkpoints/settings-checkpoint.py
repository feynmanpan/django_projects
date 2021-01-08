"""
Django settings for wtb project. 

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...) test
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '37irddih2k@s=v*&u_cio$oho)@3z21lt)es)by_&h@!1mlxzb'

# SECURITY WARNING: don't run with debug turned on in production!  
DEBUG = True

ALLOWED_HOSTS = ["wtb.wtbwtb.tk", "wtb.nctu.me", "35.221.197.37", "35.221.198.157", "35.185.150.98", "104.199.171.170"]
# https://docs.djangoproject.com/en/3.0/topics/cache/
CACHES = {
    'default': {
        # 'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        # 'LOCATION': '35.185.150.98:11211',
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',  # 指定快取使用的引擎
        'LOCATION': 'unique-snowflake',         # 寫在記憶體中的變數的唯一值
        'OPTIONS': {
            'MAX_ENTRIES': 1800,            # 最大快取記錄的數量（預設300）
            'CULL_FREQUENCY': 3,           # 快取到達最大個數之後，剔除快取個數的比例，即：1/CULL_FREQUENCY（預設3）
        }
    }
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # GraphQL要
    #
    'django.contrib.humanize',  # 千分位
    'mainsite',
    'markdown_deux',
    #
    'graphene_django',  # GraphQL要
]

# GraphQL
GRAPHENE = {
    'SCHEMA': 'wtb.schema.schema',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wtb.urls'

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

WSGI_APPLICATION = 'wtb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pydb',
        'USER': 'root',
        'PASSWORD': '!QAZ2wsx',
        'HOST': '127.0.0.1',
        'PORT': '',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-Hant'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# apache設定完/etc/httpd/conf.d/django.conf，底下兩行不再有作用，由apache決定
STATIC_URL = '/mystatic/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), '/home/pan/img']
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')