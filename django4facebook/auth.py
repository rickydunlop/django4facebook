from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

from .conf import settings
from .utils import update_user_data


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
        try:
            user = User.objects.get(username=django_facebook.uid)
        except User.DoesNotExist:
            if settings.AUTO_CREATE_USER:
                user = User(username=django_facebook.uid)
                if settings.SAVE_PROFILE_DATA:
                    update_user_data(user, django_facebook, commit=False)
                user.save()
        return user
