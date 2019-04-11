"""
__title__ = ''
__author__ = 'Thompson'
__mtime__ = '2018/8/22'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
import requests
from lxml import etree
from queue import Queue
import threading
import json


class thread_crawl(threading.Thread):
    '''
    抓取线程类
    '''
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
            'Accept-Language': 'zh-CN,zh;q=0.8'}

    def run(self):
        print("Starting " + self.threadID)
        self.qiushi_spider()
        print("Exiting ", self.threadID)

    def qiushi_spider(self):
        while not page_queue.empty():
            page = page_queue.get()
            url = 'http://www.qiushibaike.com/8hr/page/' + str(page) + '/'
            print('spider:', self.threadID, ',page:', str(page))
            # 多次尝试失败结束、防止死循环
            timeout = 4
            while timeout > 0:
                timeout -= 1
                try:
                    content = requests.get(url, headers=self.headers,timeout=0.5)
                    data_queue.put(content.text)
                    #print(content.text)
                    break
                except Exception as e:
                    print('qiushi_spider', e)


class Thread_Parser(threading.Thread):
    '''
    页面解析类；
    '''
    def __init__(self, threadID, file):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.file = file

    def run(self):
        print('starting ', self.threadID)
        while not exitFlag_Parser:
            try:
                '''
                调用队列对象的get()方法从队头删除并返回一个项目。可选参数为block，默认为True。
                如果队列为空且block为True，get()就使调用线程暂停，直至有项目可用。
                如果队列为空且block为False，队列将引发Empty异常。
                '''
                item = data_queue.get(False)
                if not item:
                    pass
                self.parse_data(item)
                data_queue.task_done() #提示线程join()是否停止阻塞
            except:
                pass
        print('Exiting ', self.threadID)

    def parse_data(self, item):
        '''
        解析网页函数
        :param item: 网页内容
        :return:
        '''
        try:
            #print(item)
            html = etree.HTML(item)
            result = html.xpath('//li[contains(@id,"qiushi_tag")]')
            print('result len:',len(result))
            for site in result:
                try:
                    imgUrl = site.xpath('.//img/@src')[0]
                    print('imgUrl:',imgUrl)
                    title = site.xpath('.//a[@class="recmd-content"]')[0]
                    detailUrl = title.xpath('@href')[0]
                    print('detail url:', detailUrl)
                    title = title.text
                    print('title:', title)
                    author = site.xpath('.//span[@class="recmd-name"]/text()')[0]
                    print('author:', author)
                    portrait = site.xpath('.//a[@class="recmd-user"]/img/@src')[0]
                    print('portrait:', portrait)
                    tmp = site.xpath('.//div[@class="recmd-num"]/span')
                    votenum = tmp[0].text
                    print("votenum:", votenum)
                    comments = 0
                    if len(tmp) >= 5:
                        comments = tmp[3].text
                    print('comments:', comments)
                    print('='*60)
                    data = {
                        'imgUrl': imgUrl,
                        'title': title,
                        'detailUrl':detailUrl,
                        'author': author,
                        'portrait':portrait,
                        'votenum': votenum,
                        'comments': comments,
                    }

                    if mutex.acquire():
                        data = json.dumps(data, ensure_ascii=False)
                        print('save....',data)
                        self.file.write(data + "\n")
                        mutex.release()
                except Exception as e:
                    print('site in result', e)
        except Exception as e:
            print('parse_data', e)

def main():
    output = open('./data/qiushibaike.json', 'a',encoding='utf-8')
    #初始化网页页码page从1-10个页面
    for page in range(1, 11):
        page_queue.put(page)
    #初始化采集线程
    crawlthreads = []
    crawlList = ["crawl-1", "crawl-2", "crawl-3"]
    for threadID in crawlList:
        thread = thread_crawl(threadID)
        thread.start()
        crawlthreads.append(thread)
    #初始化解析线程parserList
    parserthreads = []
    parserList = ["parser-1", "parser-2", "parser-3"]
    #分别启动parserList
    for threadID in parserList:
        thread = Thread_Parser(threadID, output)
        thread.start()
        parserthreads.append(thread)

    # 等待队列清空
    while not page_queue.empty():
        pass


    # 等待所有线程完成
    for t in crawlthreads:
        t.join()

    while not data_queue.empty():
        pass
    # 通知线程是时候退出
    global exitFlag_Parser
    exitFlag_Parser = True

    for t in parserthreads:
        t.join()
    print("Exiting Main Thread")
    if mutex.acquire():
        output.close()


if __name__ == '__main__':

    data_queue = Queue()
    page_queue = Queue(50)
    exitFlag_Parser = False
    mutex = threading.Lock()

    main()




