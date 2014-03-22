import threading

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import tornado.template

import socket

import redis

import os.path

SERVER = socket.gethostname()
PORT = 8888

LISTENERS = []

def redis_listener():
    r = redis.Redis(host='localhost', db=2)
    ps = r.pubsub()
    ps.subscribe('test_realtime')
    for message in ps.listen():
        for element in LISTENERS:
            element.write_message(message['data'])


class NewMsgHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('graph.html', server=SERVER, port='%d' % PORT)
        
    def post(self):
        pass

class RealtimeHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        LISTENERS.append(self)

    def on_message(self, message):
        pass

    def on_close(self):
        LISTENERS.remove(self)

settings = dict(
    auto_reload = True,
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
)

application = tornado.web.Application([
    (r'/', NewMsgHandler),
    (r'/realtime/', RealtimeHandler),
    (r'/data/(data\.json)', tornado.web.StaticFileHandler, {'path': '.'}),
], **settings)

if __name__ == "__main__":
    threading.Thread(target=redis_listener).start()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
