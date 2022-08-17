#!/usr/bin/env python3
import time
import requests
import hashlib
import random
import json

url_head = "http://www.cmos025.cn/zyzx/saveVoteInfo.do?player_id="
url_middle = "&voter_id="

query_url = "http://www.cmos025.cn/zyzx/queryVoteInfo.do?voter_id=dsfkdsjoidsj000fdfkmkkdkod0JJJJkkMk_p"

head = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
}


def create_md5():
    m = hashlib.md5()
    m.update(bytes(str(time.time()), encoding='utf-8'))
    return m.hexdigest()


def compare(url_a, url_b):
    pass


def vote(url, number):
    for i in range(0, number + 1 + random.randint(1, 10)):
        result = requests.post(url + url_middle + create_md5(), headers=head)
        print(url + ":" + result.text)


def get_vote():
    data_list = {}

    data = requests.post(query_url, headers=head).text
    json_data = json.loads(data)

    for node in json_data["votedList"]:
        for key, value in node.items():
            if key == "player_id" and value in [str(i) for i in range(1, 17)]:
                data_list[value] = node["vote_cnt"]
                continue
    return data_list


while True:
    vote_list = get_vote()
    for key in vote_list:
        if vote_list['8'] > vote_list['9']:
            vote(url_head + '9', vote_list['8'] - vote_list['9'])
        if vote_list['7'] > vote_list['8']:
            vote(url_head + '8', vote_list['7'] - vote_list['8'])
        if vote_list[key] < vote_list['9']:
            vote(url_head + key, vote_list['9'] - vote_list[key])
        if vote_list[key] > vote_list['6']:
            vote(url_head + '6', vote_list[key] - vote_list['6'])
    print("休息一下~")
    time.sleep(5)
