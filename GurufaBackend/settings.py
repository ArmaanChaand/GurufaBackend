"""
Django settings for GurufaBackend project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path
import dotenv
import dj_database_url

# Load environment variables from .env file
dotenv.load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'ovnx(kzvfkgl%&4m#hox9ln=+hiwusdfsdfwrt24f!qj4h9kl(u)!@ja9j7=un')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', False) == '1'

ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1', 
    'armaanchaand.pythonanywhere.com'
    ]

"""PRODUCTION SETTINGS"""
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1', 
    'http://localhost', 
    'https://armaanchaand.pythonanywhere.com/'
    ]
CSRF_COOKIE_SECURE = True

# SECURE_HSTS_SECONDS = 31536000
# SECURE_SSL_REDIREC=True #Unless your site should be available over both SSL and non-SSL connections, you may want to either set this setting True or configure a load balancer or reverse-proxy server to redirect all connections to HTTPS.
# SESSION_COOKIE_SECURE=True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # EXTERNAL APPS
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    "phonenumber_field",
    "corsheaders",
    # Internal Apps
    'api.apps.ApiConfig',
    'user.apps.UserConfig',
    'home.apps.HomeConfig',
    'course.apps.CourseConfig',
    'guru.apps.GuruConfig',
    'purchase.apps.PurchaseConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # django-cors-headers 
    "corsheaders.middleware.CorsMiddleware",

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Railway
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'GurufaBackend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates")
        ],
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

WSGI_APPLICATION = 'GurufaBackend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}
# if DEBUG:
#      DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#         },
#     }
# else:
#     DATABASES = {
#             'default': dj_database_url.config(default='postgresql://postgres:Uh7lxv6LA2XxV8StzVfg@containers-us-west-150.railway.app:5858/railway')
#         }



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

"""Image Field Setting"""
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')    


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CUSTOM USER
AUTH_USER_MODEL = 'user.User'


"""DJANO REST FRAMEWORK"""
REST_FRAMEWORK = {
  
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
  
}


"""SIMPLE JWT"""
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=20),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=90),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    'AUTH_HEADER_TYPES': ('Bearer'),
}


"""DJANGO-CORS-HEADERS"""
CORS_URLS_REGEX = r"^/api/.*$"

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'https://gurufa.netlify.app',
    'https://armaanchaand.pythonanywhere.com',
]

CORS_ALLOW_CREDENTIALS = True


"""DJANGO_PHONE_NUMBERFIELD"""
PHONENUMBER_DB_FORMAT = "NATIONAL"
PHONENUMBER_DEFAULT_REGION = "IN"


"""RAZORPAY CREDENTIALS"""
RAZORPAY_KEY_ID     = os.getenv('RAZORPAY_KEY_ID', "None")
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', "None")


"""EMAIL"""
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', None)
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', None)
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

"TWILIO"
TWILIO_ACCOUNT_SID  = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN   = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_PHONE_NUMBER = os.environ['TWILIO_PHONE_NUMBER']