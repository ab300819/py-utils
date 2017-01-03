#!/usr/bin/env python3

import urllib.error as error
from urllib import request

'''
                   _ooOoo_
                  o8888888o
                  88" . "88
                  (| -_- |)
                  O\  =  /O
               ____/`---'\____
             .'  \\|     |//  `.
            /  \\|||  :  |||//  \
           /  _||||| -:- |||||-  \
           |   | \\\  -  /// |   |
           | \_|  ''\---/''  |   |
           \  .-\__  `-`  ___/-. /
         ___`. .'  /--.--\  `. . __
      ."" '<  `.___\_<|>_/___.'  >'"".
     | | :  `- \`.;`\ _ /`;.`/ - ` : | |
     \  \ `-.   \_ __\ /__ _/   .-` /  /
======`-.____`-.___\_____/___.-`____.-'======
                   `=---='
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            佛祖保佑       永无BUG
'''

class Tool:
    def __init__(self):
        self.agent = {'pc_chrome': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                                   'Chrome/55.0.2883.87 Safari/537.36',
                      'iPad': 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) '
                              'AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 '
                              'Mobile/13B143 Safari/601.1',
                      'edge': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'}

    def get_html(self, url):
        user_agent = {'User-agent': self.agent['edge']}
        try:
            response = request.Request(url, headers=user_agent)
            content = request.urlopen(response, timeout=10)
            html = content.read().decode('utf-8', 'ignore')
        except error.URLError as e:
            if hasattr(e, 'reason'):
                print('Failed to reach the server.\nThe reason:%s' % e.reason)
            if hasattr(e, 'code'):
                print("The server couldn't fulfill the request")
                print('Error code:%d' % e.code)
                print('Return content:%s' % e.read())
            return None
        return html

    def write_file(self, path, file_name, url):
        pass


if __name__ == '__main__':
    pass
