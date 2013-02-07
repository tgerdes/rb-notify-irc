# rb-notify-irc Extension for Review Board.
from django.conf import settings
from django.conf.urls.defaults import patterns, include
from reviewboard.extensions.base import Extension

from rbnotifyirc import handlers

class RbNotifyIrc(Extension):
    has_admin_site=True

    def __init__(self, *args, **kwargs):
        super(RbNotifyIrc, self).__init__(*args, **kwargs)
        self.signal_handlers = handlers.SignalHandlers(self)
