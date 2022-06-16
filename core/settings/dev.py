from .base import *
import os

# ============ The devolopment settings only ============


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vl!t8=29ap)u_=&@t33f^o&7d9y*73v#k#3cvf9r@$j31oww-g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = ((os.path.join(BASE_DIR, 'static')), )
STATIC_URL = 'static/'

# Path where media is stored.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Base url to serve media files
MEDIA_URL = 'media/'
