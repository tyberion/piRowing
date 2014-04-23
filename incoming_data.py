import redis
import pickle
import numpy as np
from datetime import datetime, timedelta

w = [[], # resistance 1
     [], # resistance 2
     [], # resistance 3
     [], # resistance 4
     [], # resistance 5
     [], # resistance 6
     [], # resistance 7
     [], # resistance 8
     [], # resistance 9
     []] # resistance 10

now = datetime.today()
nowString = '%04d%02d%02dT%02d%02d' % (now.year, now.month, now.day, now.hour, now.minute)

print(nowString)

rr = redis.Redis(host='localhost', db=0)
rw = redis.Redis(host='localhost', db=1)

ps = rr.pubsub()
ps.subscribe('rowing')

N = 5
minSz = 3
d = 5
sigma = 2

filt = np.exp(-(np.linspace(-d,d,N+1)/sigma)**2)
filt = filt/filt.sum()
dfilt = -1 * np.diff(filt)
filt = np.exp(-(np.linspace(-d,d,N)/sigma)**2)
filt = filt/filt.sum()

omega_raw = np.zeros(N)

data = np.zeros((0,3))
data_current = np.zeros((1,3))
data_stroke = np.zeros((0,3))

T = 0
I = 0

alpha0 = np.zeros(minSz)
nPulls = 0

for message in ps.listen():
    dt = float(message['data'])
    if dt < 5:
        T += dt
        omega_raw = np.append(omega_raw[1:],np.pi/dt)

        if I > N:
            omega = (omega_raw * filt).sum()
            alpha = (omega_raw * dfilt).sum()/np.pi*omega
            
            data_current[0,0] = T
            data_current[0,1] = omega
            data_current[0,2] = alpha

            data = np.append(data,data_current,axis=0)
            data_stroke = np.append(data_stroke,data_current,axis=0)

            if (alpha0 < 0).sum() == minSz and alpha > 0:
                nPulls += 1 
                data_stroke = np.zeros((0,3))
                # add removal of the resistance acceleration and calculate energy and work per stroke
                rw.publish('rowing_data',{'nPulls':nPulls,'time':str(timedelta(seconds=round(T)))})
                np.save('data/%s' % nowString, data)

            alpha0 = np.append(alpha0[1:], alpha)

        I+=1

