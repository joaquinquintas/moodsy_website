import os
import random
from concurrent.futures import ThreadPoolExecutor

import arrow
import requests
import tornado.ioloop
from tornado.web import RequestHandler, Application, url
from tornado.gen import coroutine

# TODO: These will have to be configurable.
PORT = 5000
MOOD_ENDPOINT = 'http://api.moodsy.me/2/public/post/{mood_id}/'
SOURCE_PATH = os.path.dirname(os.path.abspath(__name__))
TEMPLATE_PATH = os.path.join(SOURCE_PATH, 'build')
STATIC_PATH = os.path.join(SOURCE_PATH, 'build', 'static')

# We'll use a thread pool to handle up to four requests *per instance* at a
# time.
thread_pool = ThreadPoolExecutor(8)


class HomePageHandler(RequestHandler):

    template = os.path.join(TEMPLATE_PATH, 'home.html')

    def get(self):
        number = random.randint(0, 3)
        self.render(self.template, number=number)


class MoodPageHandler(RequestHandler):

    template = os.path.join(TEMPLATE_PATH, 'mood.html')

    def async_get(self, mood_id):
        url = MOOD_ENDPOINT.format(mood_id=mood_id)
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


application = Application([
    url(r'/static/(.*)', tornado.web.StaticFileHandler, {'path': STATIC_PATH}),
    url(r"/?", HomePageHandler, name='home'),
    url(r"/m/(.{10})/?", MoodPageHandler, name='mood'),
], debug=True)

if '__main__' == __name__:
    print('Starting server on {}'.format(PORT))
    application.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
