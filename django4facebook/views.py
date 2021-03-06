import logging

from django.contrib.auth.models import User
from django.contrib.auth.views import logout as django_logout
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .utils import get_signed_request_data

logger = logging.getLogger(__name__)


@csrf_exempt
def deauthorize_callback(request):
    """
    When user deauthorize this application from facebook then
    we deactivate the user from our system
    """
    logger.info('Deauthorization request from facebook')
    data = get_signed_request_data(request)
    if not (data and data.get('user_id')):
        logger.debug('Bad deauthorization request\n\t%s' % data)
        return HttpResponseBadRequest()

    if User.objects.filter(pk=data['user_id']).update(is_active=False):
        logger.info('User %s was de authorized!' % data['user_id'])
    return HttpResponse('Ok')


def logout(request, *args, **kwargs):
    response = django_logout(request, *args, **kwargs)
    response.delete_cookie('fbsr_%s' % settings.FACEBOOK_APP_ID)
    return response
