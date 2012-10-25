from django.middleware.csrf import _get_new_csrf_key

import facebook
from .conf import settings


class DjangoFacebook(object):
    """ Simple accessor object for the Facebook user. """
    def __init__(self, user):
        self.user = user
        self.uid = user['uid']
        self.graph = facebook.GraphAPI(user['access_token'])


def get_signed_request_data(request):
    """
    Check for signed_request argument in request and parse it

    """
    signed_request = request.REQUEST.get('signed_request')
    if signed_request:
        return facebook.parse_signed_request(signed_request,
                                             settings.SECRET_KEY)


def get_fb_user_cookie(request):
    """ Attempt to find a facebook user using a cookie. """
    fb_user = facebook.get_user_from_cookie(request.COOKIES,
        settings.APP_ID, settings.SECRET_KEY)
    if fb_user:
        fb_user['method'] = 'cookie'
    return fb_user


def get_fb_user_canvas(request):
    """ Attempt to find a user using a signed_request (canvas). """
    data = get_signed_request_data(request)
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
    methods = [get_fb_user_cookie]
    if settings.USE_CANVAS_LOGIN:
        methods.insert(0, get_fb_user_canvas)
    for method in methods:
        fb_user = method(request)
        if fb_user:
            return fb_user


def update_user_data(user, django_facebook, commit=True):
    """
    Update first_name, last_name and email of the django user
    with data from facebook

    """
    user.username = django_facebook.uid

    me = django_facebook.graph.get_object('me')
    if me:
        user.first_name = me.get('first_name') or user.first_name
        user.last_name = me.get('last_name') or user.last_name
        user.email = me.get('email') or user.email

    if commit:
        user.save()
