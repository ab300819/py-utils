import os, re, time, json
import http.cookiejar
import requests

from pyquery import PyQuery as pq
from urllib import request, parse, error
from spider import ui

# 普通验证码
# /captcha.gif?r=1482662794237&amp;type=login

# 文字点击验证码
# /captcha.gif?r=1482662996504&amp;type=login&amp;lang=cn

# 验证码name
# captcha

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

main_url = 'https://www.zhihu.com'
login_url = 'https://www.zhihu.com/login/email'
user_agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
cookie_file = '../resources/rezhihu_cookie'

session = requests.Session()
session.cookies = http.cookiejar.LWPCookieJar(filename=cookie_file)

try:
    # 加载Cookies文件
    session.cookies.load(ignore_discard=True)
except:
    print("cookie未保存或cookie已过期")

# 获取_xsrf
html = session.get(main_url, headers=user_agent)
page = pq(html.content)
xsrf = pq(page("input[name='_xsrf']")[0])
_xsrf = xsrf.attr.value

# 获取验证码图片
gif_url = "http://www.zhihu.com/captcha.gif?r=" + str(int(time.time() * 1000)) + "&type=login"
gif_image = session.get(gif_url, headers=user_agent)

# 保存图片
with open('../resources/code.gif', 'wb') as f:
    f.write(gif_image.content)

# 获取登陆信息
login_info = ui.get_login_info('../resources/code.gif')

login_data = {
    "captcha": login_info['code'],
    "password": login_info['password'],
    "_xsrf": _xsrf,
    "email": login_info['username']
}
print(login_data)

# 登录
response = session.post(login_url, data=login_data, headers=user_agent)
print(response.content.decode("utf-8"))

# 保存cookie
session.cookies.save()

# 获取首页信息
resp = session.get(main_url, headers=user_agent, allow_redirects=False)
print(resp.content.decode("utf-8"))
