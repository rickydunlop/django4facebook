from django.conf.urls.defaults import *

urlpatterns = patterns('django4facebook.views',
    url(r'deauthorize/$', 'deauthorize_callback', name='fb_deauthorize_callback'),
)
