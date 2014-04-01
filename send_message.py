import redis
import time
import random

import numpy as np

r = redis.Redis(host='localhost', db=2)

r.publish('test_realtime',[])
time.sleep(0.1)

N = 1000;

f = 100 #Hz

T = np.arange(N)/f

v = 300 #rpm

L = 0.5 #cm

r = 20 #cm

theta0 = random.random()*2*np.pi

Lalpha = L/r

vAlpha = v*2*np.pi/60

theta = (theta0 + vAlpha * T) % (2*np.pi)

gpioPin = theta<Lalpha

mesg = []

for idx,(x,y) in enumerate(zip(xx, yy)):
    mesg.append([x,y])
    if idx % 10 == 0:
        r.publish('test_realtime',mesg)
        time.sleep(0.2)
        mesg = []
r.publish('test_realtime',mesg)
