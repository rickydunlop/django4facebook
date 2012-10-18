from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
import facebook


class FacebookBackend(ModelBackend):
    """Authenticate a facebook user."""
    def authenticate(self, fb_uid=None, fb_graphtoken=None):
        """
        If we receive a facebook uid then the cookie has already been
        validated.

        """
        if fb_uid:
            user, created = User.objects.get_or_create(username=fb_uid)
            return user
        return None


class FacebookProfileBackend(ModelBackend):
    """
    Authenticate a facebook user and autopopulate facebook data into the
    user's profile.

    """
    def authenticate(self, fb_uid=None, fb_graphtoken=None):
        """
        If we receive a facebook uid then the cookie has already been
        validated.

        """
        if fb_uid and fb_graphtoken:
            user, created = User.objects.get_or_create(username=fb_uid)
            if created:
                # It would be nice to replace this with an asynchronous request
                graph = facebook.GraphAPI(fb_graphtoken)
                me = graph.get_object('me')
                if me:
                    user.first_name = me.get('first_name') or user.first_name
                    user.last_name = me.get('last_name') or user.last_name
                    user.email = me.get('email') or user.email
                    user.save()
            return user
        return None


class LoginOnlyFacebookBackend(ModelBackend):
    """
    This backend only try to log in a user without auto creating it

    """
    def authenticate(self, fb_uid=None, fb_graphtoken=None):
        if fb_uid:
            try:
                user = User.objects.get(username=fb_uid)
            except User.DoesNotExist:
                pass
            else:
                return user
