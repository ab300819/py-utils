import urllib.error as Error
from urllib import request
import time

if __name__ == '__main__':
    main = '320123'
    year = range(1985, 1994)
    month = range(1, 12)
    day = range(1, 31)
    middle = []
    for y in year:
        for m in month:
            for d in day:
                for v in range(0, 1000):
                    middle.append(main + str(y) + '0' + str(m) + str(d) + str(v))

    print(middle)

    for id in middle:
        try:
            url = 'http://gs.njfu.edu.cn/photo/' + id + '.jpg'
            print(url)
            image = request.urlopen(url, timeout=2)
            data = image.read()
            f = open('D:\\Temp\\student\\' + id + '.jpg', 'wb')
            f.write(data)
            f.close()
            time.sleep(3)
        except Error.HTTPError:
            continue
