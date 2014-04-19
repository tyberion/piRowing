import redis
import time
import random

import numpy as np

r = redis.Redis(host='localhost', db=1)

r.publish('rowing_data',[])
time.sleep(0.1)

N = 1000;

xx = np.linspace(0,10,N)
yy = np.sin(xx)

mesg = []

for idx,(x,y) in enumerate(zip(xx, yy)):
    mesg.append([x,y])
    if idx % 10 == 0:
        r.publish('rowing_data',mesg)
        time.sleep(0.2)
        mesg = []
r.publish('rowing_data',mesg)
