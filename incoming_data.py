import redis
import pickle
import numpy as np
from datetime import datetime, timedelta

def find_oa_relation(data):
    """
    find the relation between alpha and omega
    """
    omega = data[:,1]
    alpha = data[:,2]
    omega = omega[alpha<0]
    alpha = alpha[alpha<0]
    alpha = alpha[(25<omega) * (omega<45)]
    omega = omega[(25<omega) * (omega<45)]
    omega = omega[:,np.newaxis]
    alpha = alpha[:,np.newaxis]
    A = np.append(omega,np.ones_like(omega),axis=1)
    w = np.linalg.lstsq(A,alpha)[0]

    return w

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
                rw.publish('rowing_data',{'nPulls':nPulls,'time':str(timedelta(seconds=round(T)))})
                np.save('data/%s' % nowString, data)
                #pickle.dump(data, open('data/%s.pcl' % nowString, 'wb'))

            alpha0 = np.append(alpha0[1:], alpha)

        I+=1

