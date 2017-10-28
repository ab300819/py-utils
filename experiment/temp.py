import json
import spider.ui as ui
import html

with open('d:\\test.html', 'r',encoding='utf-8') as f:
    content = f.read()

result = html.unescape(content)
with open('d:\\result.html', 'w',encoding='utf-8') as f:
    f.write(result)
