from tornado.ioloop import IOLoop
from tornado.web import Application

from model import Session, ModelEncoder, init_schema
from endpoints import SubscriberSignUp, SubscribersListing, DummyOk, DummyError

import logging
import logging.config
import json
import socket

### Configure Logging ###

logging_config = json.load(open('logging.json', 'r'))
logging.config.dictConfig(logging_config)


logger = logging.getLogger(__name__)

db_string = 'postgresql+psycopg2://moodsy:YSEIY3wRmevzllItfKeqLfnF@' + \
            'localhost:5432/moodsy'
logger.info("Initializing schema: {}".format(db_string))
init_schema(db_string)

# Prepare the Tornado application
args = {'Session': Session, 'Encoder': ModelEncoder}

application = Application([
    ("/subscribers/signup", SubscriberSignUp, args),
    ("/subscribers/admin/(\w*)", SubscribersListing, args),
    ("/dummy/ok", DummyOk, args),
    ("/dummy/error", DummyError, args),
], debug=True)

# Fire it up!
if __name__ == "__main__":
    application.listen(7555)
    # This is a warning because it implies the server had been STOPPED!
    # And I want to force an email in this scenario.
    logger.warn("Starting http://0.0.0.0:7555 {}".format(socket.gethostname()))
    IOLoop.instance().start()
