import logging

from reviewboard.reviews.signals import (review_request_published,
                                         review_published,
                                         reply_published)

from rbnotifyirc.models import RepositoryNotification

log = logging.getLogger('rbnotifyirc')

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

        matches_review = {'repository': review_request.repository,
                          'hook_set__hook_id': 'review_request_published'}
        for notify in RepositoryNotification.objects.filter(**matches_review):
            # TODO : actually hook up IRC
            log.debug("Need to notify {0} of change to {1}".format(
              notify.irc_configuration, review_request))

    def _review_published(self, user, review, **kwargs):
        log.debug("Review published")

        matches_review = {'repository': review.review_request.repository,
                          'hook_set__hook_id': 'review_published'}
        for notify in RepositoryNotification.objects.filter(**matches_review):
            # TODO : actually hook up IRC
            log.debug("Need to notify {0} of change to {1}".format(
              notify.irc_configuration, review))

    def _reply_published(self, user, reply, **kwargs):
        log.debug("Reply published")

        matches_review = {'repository': reply.review_request.repository,
                          'hook_set__hook_id': 'reply_published'}
        for notify in RepositoryNotification.objects.filter(**matches_review):
            # TODO : actually hook up IRC
            log.debug("Need to notify {0} of change to {1}".format(
              notify.irc_configuration, reply))
