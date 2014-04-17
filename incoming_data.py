import redis
import pickle
from datetime import datetime

now = datetime.today()

r = redis.Redis(host='localhost', db=0)

ps = r.pubsub()
ps.subscribe('rowing')

for message in ps.listen():
    print (message['data'])
