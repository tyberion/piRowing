import tornado.ioloop
import tornado.web

import redis
import pickle

r = redis.StrictRedis(host='localhost', port=6378, db=0)

data = dict(text='Hello, world!',r=r)

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, data):
        self.data = data
    def get(self):
        r = self.data['r']
        text = r.get('text')
        if not text == None:
            self.write(text)
        else:
            self.write(self.data['text'])

application = tornado.web.Application([
    (r"/", MainHandler, dict(data=data)),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
