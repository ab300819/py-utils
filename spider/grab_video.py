import requests as rqs
from pyquery import PyQuery as pq

'''
                   _ooOoo_
                  o8888888o
                  88" . "88
                  (| -_- |)
                  O\  =  /O
               ____/`---'\____
             .'  \\|     |//  `.
            /  \\|||  :  |||//  \
           /  _||||| -:- |||||_  \
           |   | \\\  -  /// |   |
           | \_|  ''\---/''  |_/ |
           \  .-\__  `-`  ___/-. /
         ___`. .'  /--.--\  `. .'___
      ."" '<  `.___\_<|>_/___.'  >' "".
     | | :  `- \`.;`\ _ /`;.`/ -`  : | |
     \  \ `-.   \_ __\ /__ _/   .-` /  /
======`-.____`-.___\_____/___.-`____.-'======
                   `=---='
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
             佛祖保佑     永无BUG
'''

url = 'http://www.888tv.co/video/890/%E7%A5%9E%E7%94%B0%E3%82%8B%E3%81%AA-%E3%81%8B%E3%82%93%E3%81%A0%E3%82%8B%E3%81%AA-%E7%B6%9A%E3%80%85%E7%94%9F%E4%B8%AD-%E5%85%83%E3%83%A9%E3%82%A6%E3%83%B3%E3%83%89%E3%82%AC%E3%83%BC%E3%83%AB%E3%82%92%E3%82%A4%E3%82%AB%E3%81%9B%E3%81%BE%E3%81%8F%E3%82%8B-%E7%A5%9E%E7%94%B0%E3%82%8B%E3%81%AA-1691'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
header = {'user-agent': user_agent}

html_source = rqs.get(url, headers=header)
print(html_source.text)

html = pq(html_source.text)
print(html)

video_source = html('source')
