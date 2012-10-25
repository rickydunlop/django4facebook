from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest


def deauthorize_callback(request):
    """
    When user deauthorize this application from facebook then
    we deactivate the user from our system
    """
    if not request.facebook:
        return HttpResponseBadRequest()
    User.objects.filter(pk=request.facebook.uid).update(is_active=False)
    return HttpResponse('Ok')
