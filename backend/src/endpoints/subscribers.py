from tornado.web import removeslash
from base import BaseHandler
from model import Subscriber, SubscriberHeader

from sqlalchemy.orm import subqueryload

import datetime
import logging


class SubscriberSignUp(BaseHandler):

    @removeslash
    def post(self):
        email = self.get_argument('email')
        timestamp = datetime.datetime.now()

        session = self.Session()

        user = Subscriber(email=email, timestamp=timestamp)
        forced_mail_logger = logging.getLogger("forcedmail")
        forced_mail_logger.info("User subscribeed to Moodsy-Dev: {}".
                                format(email))

        headers = []
        for k, v in self.request.headers.iteritems():
            headers.append(SubscriberHeader(key=k, value=v))
        user.headers = headers

        session.add(user)
        session.commit()
        session.close()


class SubscribersListing(BaseHandler):

    def get(self, token):
        if token != "IBm6gRczdqHrdf0adkJQWd9CX3kpfy9f":
            self.respond(code=403, message="Access Denied")
            return

        session = self.Session()

        users = session.query(Subscriber). \
            options(subqueryload(Subscriber.headers)). \
            order_by(Subscriber.id)

        result = []
        for instance in users:
            result.append(instance)
        self.respond(data=result)

        session.close()
