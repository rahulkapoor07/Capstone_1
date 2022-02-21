import os
import redis

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis = redis.from_url(redis_url)

redistogo_url = os.getenv('REDISTOGO_URL', None)
if redistogo_url == None:
  redis_url = '127.0.0.1:6379'
else:
  redis_url = redistogo_url
  redis_url = redis_url.split('redis://redistogo:')[1]
  redis_url = redis_url.split('/')[0]
  REDIS_PWD, REDIS_HOST = redis_url.split('@', 1)
  redis_url = "%s?password=%s" % (REDIS_HOST, REDIS_PWD)
session_opts = { 'session.type': 'redis', 'session.url': redis_url, 'session.data_dir': './cache/', 'session.key': 'appname', 'session.auto': True, }
