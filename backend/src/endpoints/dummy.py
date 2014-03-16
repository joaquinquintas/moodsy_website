from base import BaseHandler
from tornado.web import removeslash
from utils import handle_exceptions


class DummyOk(BaseHandler):

    @handle_exceptions
    @removeslash
    def get(self):
        self.respond(message="Everything seems to be ok! :D")


class DummyError(BaseHandler):

    @handle_exceptions
    @removeslash
    def get(self):
        raise Exception("Dummy error endpoint called.")


# TODO: something that actually polls the DB
# TODO: echo test?
