from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

import facebook
from .conf import settings


@csrf_exempt
def deauthorize_callback(request):
    """
    When user deauthorize this application from facebook then
    we deactivate the user from our system
    """
    signed_request = request.REQUEST.get('signed_request')
    if not signed_request:
        return HttpResponseBadRequest()
    data = facebook.parse_signed_request(signed_request,
                                             settings.SECRET_KEY)
    if not data.get('user_id'):
        return HttpResponseBadRequest()
    User.objects.filter(pk=data['user_id']).update(is_active=False)
    return HttpResponse('Ok')
