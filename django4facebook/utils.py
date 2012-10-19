from django.middleware.csrf import _get_new_csrf_key

import facebook
from .conf import settings


def get_fb_user_cookie(request):
    """ Attempt to find a facebook user using a cookie. """
    fb_user = facebook.get_user_from_cookie(request.COOKIES,
        settings.APP_ID, settings.SECRET_KEY)
    if fb_user:
        fb_user['method'] = 'cookie'
    return fb_user


def get_fb_user_canvas(request):
    """ Attempt to find a user using a signed_request (canvas). """
    signed_request = request.REQUEST.get('signed_request')
    if signed_request:
        data = facebook.parse_signed_request(signed_request,
                                             settings.SECRET_KEY)
        if data:
            if request.method == 'POST':
                # If this is requset method is POST then prevent rising err 403
                # from Django CSRF middleware
                request.META["CSRF_COOKIE"] = _get_new_csrf_key()
                request.csrf_processing_done = True

            if data.get('user_id'):
                fb_user = data['user']
                fb_user['method'] = 'canvas'
                fb_user['uid'] = data['user_id']
                fb_user['access_token'] = data['oauth_token']
                return fb_user


def get_fb_user(request):
    """
    Return a dict containing the facebook user details, if found.

    The dict must contain the auth method, uid, access_token and any
    other information that was made available by the authentication
    method.

    """
    methods = [get_fb_user_canvas, get_fb_user_cookie]
    for method in methods:
        fb_user = method(request)
        if fb_user:
            return fb_user
