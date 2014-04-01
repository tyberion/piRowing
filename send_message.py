import redis
import time

import numpy as np

r = redis.Redis(host='localhost', db=2)

r.publish('test_realtime',[])
time.sleep(0.1)

N = 1000;

xx = np.linspace(0,2*np.pi,N)
yy = np.sin(xx)
yy += (np.random.rand(N)-0.5)/2

mesg = []

for idx,(x,y) in enumerate(zip(xx, yy)):
    mesg.append([x,y])
    if idx % 10 == 0:
        r.publish('test_realtime',mesg)
        time.sleep(0.2)
        mesg = []
r.publish('test_realtime',mesg)
