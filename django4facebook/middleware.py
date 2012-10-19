from django.contrib import auth

from .conf import settings
from .utils import DjangoFacebook, get_fb_user


class FacebookDebugCanvasMiddleware(object):
    """
    Emulates signed_request behaviour to test your applications embedding.

    This should be a raw string as is sent from facebook to the server in the
    POST data, obtained by LiveHeaders, Firebug or similar. This should
    initialised before FacebookMiddleware.

    """
    def process_request(self, request):
        cp = request.POST.copy()
        request.POST = cp
        request.POST['signed_request'] = settings.DEBUG_SIGNEDREQ


class FacebookDebugCookieMiddleware(object):
    """
    Sets an imaginary cookie to make it easy to work from a development
    environment.

    This should be a raw string as is sent from a browser to the server,
    obtained by LiveHeaders, Firebug or similar. The middleware takes care of
    naming the cookie correctly. This should initialised before
    FacebookMiddleware.

    """
    def process_request(self, request):
        cookie_name = "fbs_" + settings.APP_ID
        request.COOKIES[cookie_name] = settings.DEBUG_COOKIE


class FacebookDebugTokenMiddleware(object):
    """
    Forces a specific access token to be used.

    This should be used instead of FacebookMiddleware. Make sure you have
    FACEBOOK_DEBUG_UID and FACEBOOK_DEBUG_TOKEN set in your configuration.

    """
    def process_request(self, request):
        user = {
            'uid': settings.DEBUG_UID,
            'access_token': settings.DEBUG_TOKEN,
        }
        request.facebook = DjangoFacebook(user)


class FacebookMiddleware(object):
    """
    Transparently integrate Django accounts with Facebook.

    If the user presents with a valid facebook cookie, then we want them to be
    automatically logged in as that user. We rely on the authentication backend
    to create the user if it does not exist.

    """
    def process_request(self, request):
        """
        Add `facebook` into the request context.

        If no user was found, request.facebook will be None. Otherwise it will
        contain a DjangoFacebook object containing:

        uid: The facebook users UID
        user: Any user information made available as part of the
        authentication process
        graph: A GraphAPI object connected to the current user.

        """
        fb_user = get_fb_user(request)
        request.facebook = DjangoFacebook(fb_user) if fb_user else None

    def process_response(self, request, response):
        # this is required for some lame browsers (a.k.a. IE)
        # which do not accept session cookies in iframes
        response['P3P'] = 'CP="CAO PSA OUR"'
        return response


class FacebookAuthenticationMiddleware():
    """
    This middleware try to authenticate anonymous users directly

    """
    def process_request(self, request):
        """
        An attempt to authenticate the user is made. The fb_uid and
        fb_graphtoken parameters are passed and are available for any
        AuthenticationBackends.

        """
        if request.facebook and request.user.is_anonymous():
            user = auth.authenticate(django_facebook=request.facebook)
            if user:
                auth.login(request, user)
