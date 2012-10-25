from django.conf import settings as django_settings


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

    USE_CANVAS_LOGIN = getattr(django_settings, "FACEBOOK_USE_CANVAS_LOGIN", True)

    APP_ID = django_settings.FACEBOOK_APP_ID
    SECRET_KEY = django_settings.FACEBOOK_SECRET_KEY

    def __getattr__(self, attr):
        return getattr(django_settings, attr)

settings = Settings()
