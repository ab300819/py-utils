import requests as rq
import json


def init_token():
    data = {}
    token_address = 'http://211.103.143.72:81/BaikuUserCenterV2/auth?service=authorize&params={' \
                    '"account":"15810870355|e16557a20eae4093874c3faff893a62e",' \
                    '"password":"e10adc3949ba59abbe56e057f20f883e","imei":"mobileNumber"} '

    token_request = rq.post(token_address).json()
    token_content = token_request['user']

    data["token"] = token_content['accessToken']
    data["nube"] = token_content['nubeNumber']

    return data


def init_data_pool():
    with open('RESTful_test_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data


def init_method_pool():
    with open('RESTful_test_method.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data


def auto_test(test_url, method_pool, data_pool, method=None):

    test_data = {}

    if method:
        data_list = method_pool[method]
        for item in data_list:
            test_data[item] = data_pool[item]
        test_address = test_url + method
        method_test(test_address, test_data)
    else:
        for key, value in method_pool:
            for item in value:
                test_data[item] = data_pool[item]
            test_address = test_url + key
            method_test(test_address, test_data)


def method_test(test_address, data):
    test_request = rq.post(test_address, data=json.dumps(data)).json()
    if test_request == '':
        print('返回值为空！')
        return
    if test_request['code'] == 0:
        print(test_address + ' is OK!')
    else:
        print(test_address + 'is Failed , code=' + test_request['code'] + ' , msg=' + test_request['msg'])


if __name__ == '__main__':
    test_url_head = 'http://localhost/mds'
    account_token = init_token()

    test_data = init_data_pool()
    test_method = init_method_pool()

    test_data_pool = {**account_token, **test_data}

    auto_test(method='/union/exist', method_pool=test_method, data_pool=test_data_pool, test_url=test_url_head)
