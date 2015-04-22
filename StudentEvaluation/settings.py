#-*-encoding:utf-8-*-
"""
Django settings for StudentEvaluation project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
reload(sys)
sys.setdefaultencoding('gbk')

from django.conf.global_settings import MEDIA_ROOT, STATICFILES_FINDERS,\
    TEMPLATE_DIRS, LOGGING
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sw#awbm3umd+q5w!ma19@cg6-@@ccbg!dj-6*!=(a0ihvap63n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

ADMINS = (
          ('baoan_008', '1025804905@qq.com'),
          )

MANAGFRS = ADMINS

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'engine',
    'captcha',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'StudentEvaluation.urls'

WSGI_APPLICATION = 'StudentEvaluation.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'StudentEvaluation.db'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-CN'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static').replace('\\', '/')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

#验证码
#CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'

STATICFILES_DIRS = (
                   ('images', os.path.join(STATIC_ROOT, 'images').replace('\\', '/')),
                   ('css', os.path.join(STATIC_ROOT, 'css').replace('\\', '/')),
                   ('js', os.path.join(STATIC_ROOT, 'js').replace('\\', '/')),
                   ('custom-plugins', os.path.join(STATIC_ROOT, 'custom-plugins').replace('\\', '/')),
                   ('jui', os.path.join(STATIC_ROOT, 'jui').replace('\\', '/')),
                   ('plugins', os.path.join(STATIC_ROOT, 'plugins').replace('\\', '/')),
                   ('bootstrap', os.path.join(STATIC_ROOT, 'bootstrap').replace('\\', '/')),
                   ('swf', os.path.join(STATIC_ROOT, 'swf').replace('\\', '/')),
                   # Put strings here, like "/home/html/static" or "C:/www/django/static".
                   # Always use forward slashes, even on Windows.
                   # Don't forget to use absolute paths, not relative paths.
    )

STATICFILES_FINDERS = (
                    'django.contrib.staticfiles.finders.FileSystemFinder',
                    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
                    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
    )

TEMPLATE_DIRS = (
                 'templates',
    )

LOGGING = {
           'version' : 1,
           'disable_existing_loggers' : False,
           'formatters' : {
                           'simple' : {
                                       'format' : '%(levelname)s %(name)s %(asctime)s %(message)s'
                                       },
                           'verbose' : {
                                        'format' : "%(levelname)s %(name)s %(asctime)s %(pathname)s %(module)s %(lineno)d %(message)s",
                                        'datefmt' : '%Y-%m-%d %H:%M:%S'
                                        },
                           'django_request' : {
                                        'format' : '%(levelname)s %(asctime)s %(pathname)s %(module)s %(lineno)d %(message)s status_code:%(status_code)d',
                                         'datefmt' : '%Y-%m-%d %H:%M:%S'
                                        },
                           'django_db_backends' : {
                                        'format' : '%(levelname)s %(asctime)s %(pathname)s %(module)s %(lineno)d %(message)s duration:%(duration).3f sql:%(sql)s params:%(params)s',
                                        'datefmt' : '%Y-%m-%d %H:%M:%S'
                                        },
                    },
           'handlers' : {
                         'null' : {
                                   'level' : 'DEBUG',
                                   'class' : 'django.utils.log.NullHandler',
                                   },
                         'console' :{
                                    'level' : 'DEBUG',
                                    'class' : 'logging.StreamHandler',
                                    'formatter' : 'simple'
                                    },
                         'custom_log_file' : {
                                    'level' : 'WARNING',
                                    'class' : 'logging.handlers.RotatingFileHandler',
                                    'filename' : os.path.join(BASE_DIR, 'logs/django.log'),
                                    'backupCount' : 5,
                                    'maxBytes' : '1000000',
                                    'formatter' : 'verbose'
                                    },
                        'django_request_logfile':{
                                    'level': 'WARNING',
                                    'class': 'logging.handlers.RotatingFileHandler',
                                    'filename': os.path.join(BASE_DIR, 'logs/django_request_logfile.log'),#you need define your VAR_ROOT variable that points to your project path,and mkdir a logs directory in your project root path.
                                    'backupCount': 5,
                                    'maxBytes': '1000000', # 16megabytes(16M)
                                    'formatter': 'django_request'
                                    },
        
                        'django_db_backends_logfile':{
                                    'level': 'WARNING',
                                    'class': 'logging.handlers.RotatingFileHandler',
                                    'filename': os.path.join(BASE_DIR, 'logs/django_db_backends_logfile.log'),#you need define your VAR_ROOT variable that points to your project path,and mkdir a logs directory in your project root path.
                                    'backupCount': 5,
                                    'maxBytes': '1000000', # 16megabytes(16M)
                                    'formatter': 'django_db_backends'
                                    },
                         
                        'mail_admins': {
                                    'level': 'ERROR',
                                    'class': 'django.utils.log.AdminEmailHandler',
                                    'include_html': True,
                                    }
                    },
           
           'loggers' : {
                        'django' : {
                                    'handlers' : ['console'],
                                    'level' : 'DEBUG',
                                    'propagate' : False,
                                },
                        'django.request' : {
                                    'handlers' : ['mail_admins', 'django_request_logfile'],
                                    'level' : 'WARNING',
                                    'propagate' : True,
                                },
                        'django.db.backends': {
                                    'handlers': ['django_db_backends_logfile',],
                                    'level': 'WARNING',
                                    'propagate': True,
                                },
                        'customapp': {#then you can change the level to control your custom app whether to output the debug infomation
                                    'handlers': ['console'],
                                    'level': 'DEBUG',
                                    'propagate': False,
                                },
                    },
    }