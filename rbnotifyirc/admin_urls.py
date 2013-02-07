from django.conf.urls.defaults import patterns, url

from rbnotifyirc.extension import RbNotifyIrc


urlpatterns = patterns('rbnotifyirc.views',
    url(r'^$', 'configure'),
)
