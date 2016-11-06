#! -*-encoding:utf-8-*-
import logging as log
import re
import urllib.error as HttpError
from html.parser import HTMLParser
from urllib import request, parse

from pyquery import PyQuery as pq

if __name__ == '__main__':
    main_url = 'http://103av.com'
