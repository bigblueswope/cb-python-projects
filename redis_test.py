#!/bin/env python
# bigblueswope+github+public@gmail.com

import redis

r = redis.Redis(
    host='192.168.230.202',
    port=6379 )

r.set('foo', 'bar')
value = r.get('foo')
print(value)
