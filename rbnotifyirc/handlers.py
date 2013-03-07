import logging

from django.contrib.sites.models import Site
from reviewboard.reviews.signals import (review_request_published,
                                         review_published,
                                         reply_published)

from rbnotifyirc.models import RepositoryNotification

log = logging.getLogger('rbnotifyirc')

def request_url(request):
    current_site = Site.objects.get_current()
    siteconfig = current_site.config.get()
    domain_method = siteconfig.get("site_domain_method")
    return '%s://%s%s' % (domain_method, current_site.domain,
                          request.get_absolute_url())

class SignalHandlers(object):
    def __init__(self, extension):
        """Initialize and connect all the signals"""
        self.extension = extension

        # Connect the handlers.
        review_request_published.connect(self._review_request_published)
        review_published.connect(self._review_published)
        reply_published.connect(self._reply_published)

    def _review_request_published(self, user, review_request, changedesc,
                                  **kwargs):
        log.debug("Review Request published")
        users = ': '.join(review_request.target_people.values_list('username',
          flat=True))
        url = request_url(review_request)
        submitter = review_request.submitter.username
        if changedesc:
            message = "%s: %s updated Review Request %s %s" % (
                users, submitter, review_request.summary, url)
        else:
            message = "%s: %s published New Review Request %s %s" % (
                users, submitter, review_request.summary, url)

        matches_review = {'repository': review_request.repository,
                          'hook_set__hook_id': 'review_request_published'}
        for notify in RepositoryNotification.objects.filter(**matches_review):
            log.debug("Need to notify {0} of change to {1}".format(
              notify.irc_configuration, review_request))
            notify.irc_configuration.do_notify(message)

    def _review_published(self, user, review, **kwargs):
        log.debug("Review published")
        review_request = review.review_request
        url = request_url(review_request)

        message = '%s: %s reviewed %s %s' % (review_request.submitter.username,
                                             review.user.username,
                                             review_request.summary,
                                             request_url(review_request))

        matches_review = {'repository': review_request.repository,
                          'hook_set__hook_id': 'review_published'}
        for notify in RepositoryNotification.objects.filter(**matches_review):
            log.debug("Need to notify {0} of change to {1}".format(
              notify.irc_configuration, review))
            notify.irc_configuration.do_notify(message)

    def _reply_published(self, user, reply, **kwargs):
        log.debug("Reply published")
        review_request = reply.review_request
        message = '%s: %s replied to comments in  %s %s' % (
                review_request.submitter.username,
                reply.user.username,
                review_request.summary,
                request_url(review_request))

        matches_review = {'repository': review_request.repository,
                          'hook_set__hook_id': 'reply_published'}
        for notify in RepositoryNotification.objects.filter(**matches_review):
            log.debug("Need to notify {0} of change to {1}".format(
              notify.irc_configuration, reply))
            notify.irc_configuration.do_notify(message)
