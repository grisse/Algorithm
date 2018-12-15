import requests
import re
import time
import json
from requests.exceptions import RequestException
from multiprocessing import Pool

def get_page(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    response = requests.get(url,headers = headers)
    try:
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print("request error")
        return None
def parse_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star">(.*?)</p>'
    + '.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S) #re.S使.能匹配任意字符
    items = pattern.findall(str(html))
    for item in items:
        yield {
            'top':item[0],
            'image_src':item[1],
            'name':item[2],
            'actor':item[3].strip()[3:] if len(item[3]) > 3 else '',
            'releasetime':item[4].strip()[5:],
            'score':item[5] + item[6]
        }
def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii = False) + '\n')
        f.close()

def main(offset):
    url = "http://maoyan.com/board/4?offset=" + str(offset)
    html = get_page(url)
    for item in parse_page(html):
        print(item)
        write_to_file(item)

# 如需保证电影顺序，则放弃使用多线程
# if __name__ == '__main__':
#     for i in range(10):
#         main(offset=i * 10)
#         time.sleep(1)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[i*10 for i in range(10)])