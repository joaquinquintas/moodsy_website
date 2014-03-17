import functools
import cgitb
import sys

import logging
from logging.handlers import SMTPHandler


logger = logging.getLogger(__name__)


class MailLogger(SMTPHandler):
    subject = 'Moodsy Backend Logger Message!'
    fromaddr = "Moodsy Backend <app@moodsy.me>"
    toaddrs = ["Hugo Osvaldo Barrera <hugo@barrera.io>"]

    def __init__(self):
        super(MailLogger, self).__init__("127.0.0.1", self.fromaddr,
                                         self.toaddrs, self.subject)


class ForcedMailLogger(SMTPHandler):
    subject = 'User subscribed to Moodsy-Dev!'
    fromaddr = "Moodsy Backend <app@moodsy.me>"
    toaddrs = ["Joaquin Quintas <joaquin@moodsy.me>"]

    def __init__(self):
        super(ForcedMailLogger, self).__init__("127.0.0.1", self.fromaddr,
                                               self.toaddrs, self.subject)


def handle_exceptions(method):
    """Decorate RequestHandler methods with this to catch any exceptions."""

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except Exception, e:
            logger.error(cgitb.text(sys.exc_info()))
            self.respond(code=500, message=e.message)

    return wrapper
