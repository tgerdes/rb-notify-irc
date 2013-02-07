import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from reviewboard.reviews.models import Repository

log = logging.getLogger('rbnotifyirc')

class IrcConfiguration(models.Model):
    """
    Configuration for an IRC server to connect to.

    Includes the nick and channels to connect to as well.
    """
    server = models.CharField(_('server'), max_length=255)
    port = models.IntegerField(_('port'), default=6667)
    password = models.CharField(_('password'), max_length=128, default=u'',
                                blank=True)
    use_ssl = models.BooleanField(_('ssl'), default=False)

    room = models.CharField(_('room'), max_length=255)
    nick = models.CharField(_('nickname'), default='reviewbot', max_length=255)


    def __unicode__(self):
        return u"{0.nick} on irc://{0.server}:{0.port}/{0.room}".format(self)

class NotifyHookManager(models.Manager):
    def get_by_natural_key(self, hook_id):
        return self.get(hook_id=hook_id)

class NotifyHook(models.Model):
    """
    A named hook that can be connected.
    """
    hook_id = models.CharField(_("hook type"), max_length=128)
    description = models.CharField(_("description"), max_length=255,
                                   default=u"")

    def natural_key(self):
        return (hook_id,)

    def __unicode__(self):
        return self.description

class RepositoryNotification(models.Model):
    """
    Map IRC connections to repositories and Notification Hooks.
    """
    irc_configuration = models.ForeignKey(IrcConfiguration)
    repository = models.ForeignKey(Repository)
    hook_set = models.ManyToManyField(NotifyHook, blank=True)

    def __unicode__(self):
        return u"({0.repository}): {0.irc_configuration}".format(self)
