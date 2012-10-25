from django.conf.urls.defaults import *

urlpatterns = patterns('django4facebook',
    url(r'deauthorize/$', 'deauthorize_callback', name='fb_deauthorize_callback'),
)
