import tornado
from tornado.web import RequestHandler

import json


class BaseHandler(RequestHandler):

    def initialize(self, Session, Encoder):
        self.Session = Session
        self.Encoder = Encoder

    def set_default_headers(self):
        self.set_header("Server",
                        "focusfreak tornado/{}".format(tornado.version))
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods",
                        "GET,PUT,POST,DELETE,OPTIONS")
        self.set_header("Access-Control-Max-Age", 86400)

    def respond(self, code=200, message=None, data=None):
        response = {}
        if message:
            response['message'] = message
        if data:
            response['data'] = data
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(response, indent=2, cls=self.Encoder))
        self.set_status(code)
