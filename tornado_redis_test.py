import tornado.ioloop
import tornado.web

import redis
import pickle

r = redis.StrictRedis(host='localhost', port=6378, db=0)

data = {'text','Hello, world!'}

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, data)
	self.data = data;
    def get(self):
        self.write(self.data['text'])

application = tornado.web.Application([
    (r"/", MainHandler, data),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
