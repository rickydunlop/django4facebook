from django.conf import settings as django_settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class Settings(object):
    """
    Settings wrapper between FACEBOOK settings and Django settings
    """
    DEBUG_SIGNEDREQ = getattr(django_settings, "FACEBOOK_DEBUG_SIGNEDREQ", None)
    DEBUG_COOKIE = getattr(django_settings, "FACEBOOK_DEBUG_COOKIE", None)
    DEBUG_TOKEN = getattr(django_settings, "FACEBOOK_DEBUG_TOKEN", None)
    DEBUG_UID = getattr(django_settings, "FACEBOOK_DEBUG_UID", None)
    DEBUG_COOKIE = getattr(django_settings, "FACEBOOK_DEBUG_COOKIE", None)
    DEBUG_COOKIE = getattr(django_settings, "FACEBOOK_DEBUG_COOKIE", None)

    SAVE_PROFILE_DATA = getattr(django_settings, "FACEBOOK_SAVE_PROFILE_DATA", True)
    AUTO_CREATE_USER = getattr(django_settings, "FACEBOOK_AUTO_CREATE_USER", True)
    AUTO_ACTIVATE_USER = getattr(django_settings, "FACEBOOK_AUTO_ACTIVATE_USER", True)

    USE_CANVAS_LOGIN = getattr(django_settings, "FACEBOOK_USE_CANVAS_LOGIN", True)

    SDK_VERSION = getattr(django_settings, "FACEBOOK_SDK_VERSION", '2.5')

    APP_ID = django_settings.FACEBOOK_APP_ID
    SECRET_KEY = django_settings.FACEBOOK_SECRET_KEY

    def __init__(self):
        if hasattr(django_settings, 'AUTH_USER_MODEL'):
            self.USER_MODEL = get_user_model()
            self.UID_USER_FIELD = getattr(django_settings, "FACEBOOK_UID_USER_FIELD", 'facebook_id')
        else:
            self.USER_MODEL = User
            self.UID_USER_FIELD = 'username'

    def __getattr__(self, attr):
        return getattr(django_settings, attr)

settings = Settings()
