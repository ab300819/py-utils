import requests
import html as ht
import re
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

{
    "module": "",
    "version": "",
    "name": "",
    "url": ""

}

html_url = 'http://www.lfd.uci.edu/~gohlke/pythonlibs/'
head = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
}

html_response = requests.get(html_url, headers=head)
html_page = pq(html_response.content)
target_list = html_page('.pylibs li')

module_name = []
package_name = []
package_url = []

for value in target_list:
    li = pq(value)
    if not li('a'):
        continue
    if li('a').attr('id'):
        module_name.append(ht.unescape(li('a').attr('id')))
    if li('a').attr('onclick'):
        package_name.append(ht.unescape(li('a').text()))
        package_url.append(ht.unescape(li('a').attr('onclick')))

print(module_name)
# print(package_name)
print(package_url)

for value in package_name:
    if not ('cp35' in value and 'amd64' in value):
        package_name.remove(value)
print(package_name)

# with open('../resources/list.txt', 'a', encoding='utf-8') as f:
#     f.write(ht.unescape(temp.html()) + '\n')
