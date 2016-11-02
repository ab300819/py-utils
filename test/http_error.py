from urllib import request as rq
import urllib.error as error

request = rq.Request('http://blog.csdn.net/toddhan/article/details/7942952')
try:
    content = rq.urlopen(request)
except error:
    print(error)
