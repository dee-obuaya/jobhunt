from decouple import config
from datetime import timedelta

SECRET_KEY = config('SECRET_KEY')
COMPANY_IMGS = config('COMPANY_IMGS')

REMEMBER_COOKIE_DURATION = timedelta(minutes=5)
PERMANENT_SESSION_LIFETIME = timedelta(minutes=5)
