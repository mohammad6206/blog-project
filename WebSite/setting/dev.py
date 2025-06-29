from WebSite.settings import*


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4zh26v^xd4utl)^73fzt@2s&$o85so*iy9lcy@!@lt%!)^mf$v'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

ALLOWED_HOSTS = ['*']


#INSTALLED_APPS = []




# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}




STATIC_ROOT = BASE_DIR / "static"
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [
    BASE_DIR / "STATICS"
    ]






#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'





EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mysite.blog.post@gmail.com'
EMAIL_HOST_PASSWORD = 'kipevawpylklefkk'  
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER



