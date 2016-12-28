import urllib.error as error
from urllib import request

header = {'desktop': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/55.0.2883.87 Safari/537.36',
          'ipad': 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) '
                  'AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 '
                  'Mobile/13B143 Safari/601.1',
          'edge': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'}

user_agent = {'User-agent': header['edge']}

url = 'https://www.zhihu.com/#signin'

try:
    response = request.Request(url, headers=user_agent)
    content = request.urlopen(response, timeout=5)
    html = content.read().decode('utf-8', 'ignore')
except error.HTTPError:
    print(error.HTTPError.code)

print(html)
