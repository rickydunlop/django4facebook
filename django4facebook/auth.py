import logging

from django.contrib.auth.backends import ModelBackend

from .conf import settings
from .utils import update_user_data
from .signals import facebook_registration

logger = logging.getLogger(__name__)


class FacebookBackend(ModelBackend):
    """Authenticate a facebook user."""
    def authenticate(self, django_facebook):
        """
        Try to authenticate a facebook user. If local user does not exists
        then create new if settings.FACEBOOK_AUTO_CREATE_USER is True.
        If new user is created and settings.FACEBOOK_SAVE_PROFILE_DATA is True
        then autopopulate facebook data into the user's profile.

        """
        user = None
        if not django_facebook.uid:
            return user
        user_model = settings.USER_MODEL
        facebook_uid_field = settings.UID_USER_FIELD

        try:
            user = user_model.objects.get(**{facebook_uid_field: django_facebook.uid})
        except user_model.DoesNotExist:
            if settings.AUTO_CREATE_USER:
                user = user_model(**{facebook_uid_field: django_facebook.uid})
                if settings.AUTO_ACTIVATE_USER:
                    user.is_active = True
                if settings.SAVE_PROFILE_DATA:
                    update_user_data(user, django_facebook, commit=False)
                user.save()
                facebook_registration.send(sender=user_model, user=user, django_facebook=django_facebook)
        if user:
            logger.info("Succesfully authenticate %s" % unicode(user))
        return user
