import os
import gzip
import chardet

gz_file='C:\\Users\\mengshen\\Desktop\\vm-usa-micen-vo-18101-netmask-vo_web_action_2020.0410.002901.gz'

with open(gz_file,'rb') as f:
    data = f.read()
    content=gzip.decompress(data)
    ch= chardet.detect(content)
    print(ch['encoding'])
    print(len(content.encode('gbk')))
    # dicts=chardet.detect(data)
    # print(dicts["encoding"])
