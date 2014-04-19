import threading

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import tornado.template

import socket

import redis

import os.path

def getNetworkIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('192.168.178.1', 0))
    return s.getsockname()[0]

SERVER = getNetworkIp()
PORT = 8888

LISTENERS = []

def redis_listener():
    r = redis.Redis(host='localhost', db=1)
    ps = r.pubsub()
    ps.subscribe('rowing_data')
    print(ps)
    for message in ps.listen():
        for element in LISTENERS:
            print(element)
            element.write_message(message['data'])


class NewMsgHandler(tornado.web.RequestHandler):
    def get(self):
	print('starting NewMsgHandler')
        self.render('data.html', server=SERVER, port='%d' % PORT)
        
    def post(self):
        pass

class RealtimeHandler(tornado.websocket.WebSocketHandler):
    def open(self):
	print('starting RealtimeHandler')
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
    #(r'/data/(data\.json)', tornado.web.StaticFileHandler, {'path': '.'}),
], **settings)

if __name__ == "__main__":
    T = threading.Thread(target=redis_listener)
    T.start()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(PORT)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("stopping program")
        #TODO: disable thread 
        tornado.ioloop.IOLoop.instance().stop()
