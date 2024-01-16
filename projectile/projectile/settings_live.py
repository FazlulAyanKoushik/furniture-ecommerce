from .settings import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")

# AWS SETTINGS
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
AWS_MEDIA_BUCKET_NAME = os.environ["AWS_MEDIA_BUCKET_NAME"]
STATICFILES_STORAGE = "common.buckets.S3StaticStorage"
DEFAULT_FILE_STORAGE = "common.buckets.S3MediaStorage"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
AWS_S3_REGION_NAME = os.environ["AWS_S3_REGION_NAME"]
AWS_QUERYSTRING_AUTH = False
AWS_PRELOAD_METADATA = True
AWS_DEFAULT_ACL = None
AWS_S3_SECURE_URLS = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = STATIC_DIR
STATIC_URL = "s3.{}.amazonaws.com/{}/".format(
    AWS_S3_REGION_NAME, AWS_STORAGE_BUCKET_NAME
)

MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = "s3.{}.amazonaws.com/{}/".format(AWS_S3_REGION_NAME, AWS_MEDIA_BUCKET_NAME)

# SENTRY SETTINGS
sentry_sdk.init(
    os.environ["SENTRY_DSN"],
    environment=os.environ["SENTRY_ENVIRONMENT"],
    integrations=[CeleryIntegration(), DjangoIntegration(), RedisIntegration()],
    traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)
