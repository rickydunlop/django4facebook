from django.conf import settings
from django.contrib import auth
from django.middleware.csrf import _get_new_csrf_key

import facebook


class DjangoFacebook(object):
    """ Simple accessor object for the Facebook user. """
    def __init__(self, user):
        self.user = user
        self.uid = user['uid']
        self.graph = facebook.GraphAPI(user['access_token'])


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
        request.POST['signed_request'] = settings.FACEBOOK_DEBUG_SIGNEDREQ
        return None


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
        cookie_name = "fbs_" + settings.FACEBOOK_APP_ID
        request.COOKIES[cookie_name] = settings.FACEBOOK_DEBUG_COOKIE
        return None


class FacebookDebugTokenMiddleware(object):
    """
    Forces a specific access token to be used.

    This should be used instead of FacebookMiddleware. Make sure you have
    FACEBOOK_DEBUG_UID and FACEBOOK_DEBUG_TOKEN set in your configuration.

    """
    def process_request(self, request):
        user = {
            'uid': settings.FACEBOOK_DEBUG_UID,
            'access_token': settings.FACEBOOK_DEBUG_TOKEN,
        }
        request.facebook = DjangoFacebook(user)
        return None


class FacebookMiddleware(object):
    """
    Transparently integrate Django accounts with Facebook.

    If the user presents with a valid facebook cookie, then we want them to be
    automatically logged in as that user. We rely on the authentication backend
    to create the user if it does not exist.

    """
    def get_fb_user_cookie(self, request):
        """ Attempt to find a facebook user using a cookie. """
        fb_user = facebook.get_user_from_cookie(request.COOKIES,
            settings.FACEBOOK_APP_ID, settings.FACEBOOK_SECRET_KEY)
        if fb_user:
            fb_user['method'] = 'cookie'
        return fb_user

    def get_fb_user_canvas(self, request):
        """ Attempt to find a user using a signed_request (canvas). """
        fb_user = None
        signed_request = request.REQUEST.get('signed_request')
        if signed_request:
            data = facebook.parse_signed_request(signed_request,
                                                 settings.FACEBOOK_SECRET_KEY)
            if data:
                if data.get('user_id'):
                    fb_user = data['user']
                    fb_user['method'] = 'canvas'
                    fb_user['uid'] = data['user_id']
                    fb_user['access_token'] = data['oauth_token']

                if request.method == 'POST':
                    # If this is requset method is POST then prevent rising err 403
                    # from Django CSRF middleware
                    request.META["CSRF_COOKIE"] = _get_new_csrf_key()
                    request.csrf_processing_done = True
        return fb_user

    def get_fb_user(self, request):
        """
        Return a dict containing the facebook user details, if found.

        The dict must contain the auth method, uid, access_token and any
        other information that was made available by the authentication
        method.

        """
        fb_user = None
        methods = ['get_fb_user_canvas', 'get_fb_user_cookie']
        for method in methods:
            fb_user = getattr(self, method)(request)
            if (fb_user):
                break
        return fb_user

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
        fb_user = self.get_fb_user(request)
        request.facebook = DjangoFacebook(fb_user) if fb_user else None


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
            fb_user = request.facebook.user
            user = auth.authenticate(fb_uid=fb_user['uid'],
                                     fb_graphtoken=fb_user['access_token'])
            if user:
                auth.login(request, user)
