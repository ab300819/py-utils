import os, re, time
import urllib.error as error

from pyquery import PyQuery as pq
from urllib import request


# 普通验证码
# /captcha.gif?r=1482662794237&amp;type=login

# 文字点击验证码
# /captcha.gif?r=1482662996504&amp;type=login&amp;lang=cn

# 验证码name
# captcha

class ZhiHu:
    def get_page(self, url):
        pass
