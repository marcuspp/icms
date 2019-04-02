import environ
from django.core.management.utils import get_random_secret_key

env = environ.Env(
  # set casting, default value
  ICMS_DEBUG=(bool, False),
  ICMS_WEB_PORT=(int, 8000),
  ICMS_DB_URL=(str, 'postgres://postgres@db:5432/postgres'),
  ICMS_SECRET_KEY=(str, get_random_secret_key()),
  ICMS_ALLOWED_HOSTS=(list, [])
)
