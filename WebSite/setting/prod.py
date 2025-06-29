from WebSite.settings import*


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4zh26v^xd4utl)^73fzt@2s&$o85so*iy9lcy@!@lt%!)^mf$v'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG =False

ALLOWED_HOSTS = ['yourdomain.com']




#INSTALLED_APPS =[]




# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',           
        'USER': 'root',                
        'PASSWORD': '2E8rXKss3kiBv0XBDbS1OYt3', 
        'HOST': 'blog-database',       
        'PORT': '5432',                
    }
}








STATIC_ROOT = BASE_DIR / "static"
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [
    BASE_DIR / "STATICS"
    ]






EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mysite.blog.post@gmail.com'
EMAIL_HOST_PASSWORD = 'kipevawpylklefkk'  
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER






    # Https settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

    # HSTS settings
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    # More security settings
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "SAMEORIGIN"
SECURE_REFERRER_POLICY = "strict-origin"
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")



