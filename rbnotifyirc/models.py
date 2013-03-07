import logging
import re
import socket


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


    def connect(self):
        # TODO : support SSL
        self.socket = socket.create_connection((self.server, int(self.port)))
        self.read = self.socket.makefile('r')
        self.write = self.socket.makefile('w', bufsize=0)
        self.write.write('NICK %s\n' % self.nick)
        self.write.write('USER %s * * :IRC Bot\n' % (self.nick))
        # Read until connected
        while True:
            line = self.read.readline()
            if re.search('00[1-4] reviewbot', line):
                break

    def disconnect(self):
        self.write.write('QUIT\n')
        while True:
            line = self.read.readline()
            if not line: break
        self.read.close()
        self.write.close()
        self.socket.close()
        del(self.socket)
        del(self.read)
        del(self.write)

    def notify(self, message):
        for room in self.room.split(','):
            room = room.strip()
            if room[0] != '#':
                room = '#' + room
            self.write.write('NOTICE {room} :{message}\n'.format(
              room=room, message=message))

    def do_notify(self, message):
        self.connect()
        self.notify(message)
        self.disconnect()


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
