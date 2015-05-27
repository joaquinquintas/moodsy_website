#!/usr/bin/env python3

import os
import random
from concurrent.futures import ThreadPoolExecutor

import arrow
from envsettings import SettingsReader
import requests
from tornado.gen import coroutine
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.netutil import bind_unix_socket
from tornado.process import fork_processes
from tornado.web import RequestHandler, Application, url, StaticFileHandler


settings = SettingsReader([
    ("MOODSY_WWW_TEMPLATE_PATH", "template_path", str),
    ("MOODSY_WWW_STATIC_PATH", "static_path", str),
    ("MOODSY_WWW_DEBUG_PORT", "debug_port", int, None),
    ("MOODSY_WWW_SOCKET", "socket", str, None),
])

if not settings.socket and not settings.debug_port:
    raise Exception('No debug port nor socket defined.')

settings.debug = settings.debug_port is not None
settings.moods_api = 'http://api.moodsy.me/2/public/post/{mood_id}/'

thread_pool = ThreadPoolExecutor(8)


class HomePageHandler(RequestHandler):

    template = os.path.join(settings.template_path, 'home.html')

    def get(self):
        number = random.randint(0, 3)
        self.render(self.template, number=number)


class MoodPageHandler(RequestHandler):

    template = os.path.join(settings.template_path, 'mood.html')

    def async_get(self, mood_id):
        url = settings.moods_api.format(mood_id=mood_id)
        resp = requests.get(url)
        if resp.status_code != 200:
            # TODO: We need a design for the 404 page.
            self.set_status(404)
            self.write('No such mood')
            return

        mood = resp.json()
        moodsies = [m['user_fname'] for m in mood['moodsies']['moodsies']]
        mood['post']['moment'] = arrow.get(
            mood['post']['datetime'],
            'YYYY-MM-DD HH:mm:ss Z'
        ).humanize()

        self.render(self.template, mood=mood, moodsies=moodsies)

    @coroutine
    def get(self, mood_id):
        yield thread_pool.submit(self.async_get, mood_id)


class StaticPageHandler(RequestHandler):

    def initialize(self, page):
        self.template = os.path.join(settings.template_path, page + '.html')

    def get(self):
        self.render(self.template)


application = Application([
    url(r'/static/(.*)', StaticFileHandler, {'path': settings.static_path}),
    url(r"/?", HomePageHandler, name='home'),
    url(r"/m/(.{10})/?", MoodPageHandler, name='mood'),
    url(r'/privacy/?', StaticPageHandler, {'page': 'privacy'}),
], debug=settings.debug)

if '__main__' == __name__:
    if settings.debug:
        print('Starting debug server on {}'.format(settings.debug_port))
        application.listen(settings.debug_port)
        IOLoop.instance().start()
    else:
        print('Starting production server.')
        socket = bind_unix_socket(settings.socket, mode=0o777)
        fork_processes(None)
        server = HTTPServer(application)
        server.add_socket(socket)
        IOLoop.instance().start()
