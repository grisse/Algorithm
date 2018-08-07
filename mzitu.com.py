from multiprocessing import Pool
import re
import requests
from lxml import etree

class Mzt():

    def __init__(self):
        self.url = 'http://www.mzitu.com/'

    def request_page(self):
        response = requests.get(self.url)
        response.encoding = response.apparent_encoding
        page = etree.HTML(response.text).xpath('//a[@class="page-numbers"]/text()')[-1]
        return page

    def request_img(self):
        for page in self.request_page():
            response = requests.get(self.url + "page/{}/".format(page))
            response.encoding = response.apparent_encoding
            miss_url = []
            for i in etree.HTML(response.text).xpath('.//ul[@id="pins"]/li'):
                miss_url.append(i.xpath('a/@href')[0])
            return miss_url

    def request_next_page(self, url):
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        page = etree.HTML(response.text).xpath('.//div[@class="pagenavi"]/a/@href')[-2]
        for i in range(1, int(page[-2:])+1):
            req_img = requests.get(page[:-2] + str(i))
            req_img.encoding = req_img.apparent_encoding
            miss = etree.HTML(req_img.text).xpath('.//div[@class="main-image"]/p/a/img/@src')[0]
            num = etree.HTML(req_img.text).xpath('.//div[@class="main-image"]/p/a/img/@src')[0][-9:]
            # 反爬虫
            header = {'Referer': miss,'User-Agent': ''}
            r = requests.get(miss, headers=header)
            with open('/home/grisse/image' + str(num), 'wb') as f:
                f.write(r.content)

    def main(self):
        pool = Pool(10)
        pool.map(self.request_next_page, self.request_img())
        pool.close()
        pool.join()

if __name__ == '__main__':
    Mzt().main()
