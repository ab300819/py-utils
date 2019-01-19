import html
import http.cookiejar
import json
import time

import requests
from pyquery import PyQuery as pq

from spider import ui

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

'''
普通验证码
/captcha.gif?r=1482662794237&type=login

文字点击验证码
/captcha.gif?r=1482662996504&type=login&lang=cn

验证码name = 'captcha'

手机登陆
http://www.zhihu.com/login/phone_num

邮箱登陆
https://www.zhihu.com/login/email

用户文章列表获取url,返回json数据
https://www.zhihu.com/api/v4/members/sgai/articles?include=data[*].comment_count,collapsed_counts,reviewing_comments_count,can_comment,comment_permission,content,voteup_count,created,updated,upvoted_followees,voting;data[*].author.badge[?(type=best_answerer)].topics&offset=0&limit=10&sort_by=created

文章json数据获取
https://zhuanlan.zhihu.com/api/posts/
'''


class GrabZhiHu:
    def __init__(self):
        self.main_url = 'https://www.zhihu.com'
        self.login_url = 'https://www.zhihu.com/login/email'
        self.article_main_url = 'https://zhuanlan.zhihu.com/api/posts/'
        self.user_main_url = 'https://www.zhihu.com/people/'
        self.user_agent = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        self.cookie_file = '../resources/zhihu_cookie'
        self.session = requests.Session()
        self.session.cookies = http.cookiejar.LWPCookieJar(filename=self.cookie_file)
        self.__check_login()

    def __check_login(self):
        try:
            # 加载Cookies文件
            self.session.cookies.load(ignore_discard=True)
            print("使用cookie登陆!")

        except:
            print("未找到或cookie已过期!")
            self.__login()

    def __login(self):

        # 获取_xsrf
        result = self.session.get(self.main_url, headers=self.user_agent)
        html = pq(result.content)
        xsrf = pq(html("input[name='_xsrf']")[0])
        _xsrf = xsrf.attr.value

        # 获取验证码图片
        gif_url = "http://www.zhihu.com/captcha.gif?r=" + str(int(time.time() * 1000)) + "&type=login"
        gif_image = self.session.get(gif_url, headers=self.user_agent)

        # 保存图片
        with open('../resources/zhihu_code.gif', 'wb') as f:
            f.write(gif_image.content)

        # 获取登陆信息
        login_info = ui.get_login_info('../resources/zhihu_code.gif')
        login_data = {
            "captcha": login_info['code'],
            "password": login_info['password'],
            "_xsrf": _xsrf,
            "email": login_info['username']
        }

        # 登录
        response = self.session.post(self.login_url, data=login_data, headers=self.user_agent)
        print(response.content.decode('unicode-escape'))

        # 保存cookie
        self.session.cookies.save()

    def test(self, url):
        if url:
            result = self.session.get(url, headers=self.user_agent, allow_redirects=False)
        else:
            result = self.session.get(self.main_url, headers=self.user_agent, allow_redirects=False)
        print(html.unescape(result.content.decode("utf-8")))

    # 抓取用户发表文章
    def analyze_article_url(self, user_posts):
        user_posts_url = self.user_main_url + user_posts
        user_posts_html = self.session \
            .get(user_posts_url, headers=self.user_agent, allow_redirects=False) \
            .content \
            .decode('utf-8')
        user_posts_page = pq(user_posts_html)
        user_posts_data = user_posts_page('#data').attr['data-state']
        user_posts_json_data = json.loads(user_posts_data)

        print(user_posts_json_data)

    # 获取文章json数据
    def get_article_json(self, article_id):
        article = {}
        article_author = {}
        article_content = {}

        article_url = self.article_main_url + str(article_id)
        article_html = self.session \
            .get(article_url, headers=self.user_agent, allow_redirects=False) \
            .content \
            .decode('utf-8')
        article_json_data = json.loads(article_html)

        article_author_data = article_json_data['author']
        article_author['id'] = article_author_data['slug']
        article_author['name'] = article_author_data['name']
        article['author'] = article_author

        article_content['id'] = article_json_data['slug']
        article_content['title'] = article_json_data['title']
        article_content['time'] = article_json_data['publishedTime']
        article_content['content'] = article_json_data['content']
        article['content'] = article_content
        article['like'] = article_json_data['likesCount']

        column = article_json_data['column']
        article['column'] = column['slug']
        print(article)
        return article

    # 保存内容
    def save_content(self, article_info):
        pass

    # 传入收藏夹主页，分析每个问题及其答案
    def analyse_collection_url(self):
        pass

    # 传入单个问题url，抓取收藏夹问题和答案
    def get_collection_question_answer(self):
        pass

    # 抓取目标问题及答案
    def get_question_answer(self):
        pass


class WriteToDataBase:
    def __init__(self):
        pass


if __name__ == '__main__':
    # test = GrabZhiHu()
    # url = 25181905
    # test.get_article_json(url)
    # user_url = 'sgai/pins/posts'
    # test.analyze_article_url(user_url)
    user_article_list = 'https://www.zhihu.com/api/v4/members/sgai/articles?' \
                        'include=data[*].comment_count,content,voteup_count,created,updated,voting;' \
                        'data[*].author.badge[?(type=best_answerer)].topics&offset=0&limit=10&sort_by=created'
    print(user_article_list)
