import redis
import time

r = redis.Redis(host='localhost', db=2)

for i in range(100):
    r.publish('test_realtime',dict(msg01='%d' % i, msg02='%d' % (i*2)))
    time.sleep(0.1)


