import redis
import pickle
import numpy as np
from datetime import datetime

now = datetime.today()
nowString = '%04d%02d%02dT%02d%02d' % (now.year, now.month, now.day, now.hour, now.minute)

print(nowString)

r = redis.Redis(host='localhost', db=0)

ps = r.pubsub()
ps.subscribe('rowing')

N = 5
d = 5
sigma = 2
filt = np.exp(-(np.linspace(-d,d,N+1)/sigma)**2)
filt = filt/filt.sum()
dfilt = -1 * np.diff(filt)
filt = np.exp(-(np.linspace(-d,d,N)/sigma)**2)
filt = filt/filt.sum()

omega_raw = np.zeros(N)

data = np.zeros((1,3))
data_current = np.zeros((1,3))

T = 0
I = 0

for message in ps.listen():
    dt = float(message['data'])
    T += dt
    omega_raw = np.append(omega_raw[1:],np.pi/dt)

    if I > N:
	omega = (omega_raw * filt).sum()
	alpha = (omega_raw * dfilt).sum()/np.pi*omega

	data_current[0,0] = T
	data_current[0,1] = omega
	data_current[0,2] = alpha
	
	data = np.append(data,data_current,axis=0)

	if I%100 == 0:
	    np.save('data/%s' % nowString, data)
            #pickle.dump(data, open('data/%s.pcl' % nowString, 'wb'))

    I+=1

