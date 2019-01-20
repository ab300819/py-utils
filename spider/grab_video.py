import mysql.connector as database
import requests as rqs
from pyquery import PyQuery as pq
import time

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

MAIN_URL = 'http://www.888tv.co/videos?page='
TOTAL_PAGE = 45
START_PAGE = 1
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
HEADER = {'user-agent': USER_AGENT}

# SQL
INSERT_VIDEO_LIST = "INSERT INTO video_list(title,url,rate,download_status) values (%s,%s,%s,%s)"
UPDATE_VIDEO_LIST = ''
DELETE_VIDEO_LIST = ''
SELECT_VIDEO_LIST = ''


def get_html_response(url):
    html_source = rqs.get(MAIN_URL, headers=HEADER)
    return html_source.text


def get_video_list(html):
    video_list_result = []
    html_parse = pq(html)
    video_list = html_parse('.col-sm-6.col-md-4.col-lg-4')

    for i in video_list:
        single_video = []
        video = pq(i)
        single_video.append(video('span').text())
        single_video.append(video('a').attr('href'))
        single_video.append(remove_str(video('b').text(), '%'))
        single_video.append(0)
        print(single_video)
        video_list_result.append(single_video)
    return video_list_result


def get_video_file(html):
    html_parse = pq(html)


def remove_str(source, target):
    return source.rstrip(target)


if __name__ == '__main__':

    all_video = []

    for i in range(START_PAGE, TOTAL_PAGE+1):
        html_res = get_html_response(MAIN_URL + str(i))
        video_result = get_video_list(html_res)
        all_video.extend(video_result)
        print(i)
        time.sleep(9)

    connect = database.connect(host='192.168.9.109', user='root', password='110119', database='test')
    cursor = connect.cursor()
    for value in all_video:
        cursor.execute(INSERT_VIDEO_LIST, value)
    print(cursor.rowcount)
    connect.commit()
    connect.close()
