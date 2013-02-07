# rb-notify-irc Extension for Review Board.
from django.conf import settings
from django.conf.urls.defaults import patterns, include
from reviewboard.extensions.base import Extension

class RbNotifyIrc(Extension):
    def __init__(self, *args, **kwargs):
        super(RbNotifyIrc, self).__init__(*args, **kwargs)
