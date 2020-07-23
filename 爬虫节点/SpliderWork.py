# coding:utf-8
from multiprocessing.managers import BaseManager
from HtmlDownloader import HtmlDownloader
from HtmlParser import HtmlParser


class SpiderWork(object):
    def __init__(self):
        # 初始化分布式进程中的工作节点的连接工作
        # 第一步：使用BaseManageer获取Queue的方法名称
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')
        # 第二步：连接到服务器
        server_addr = '127.0.0.1'
        print(('Connect to server %s...' % server_addr))
        # 端口和验证口令注意和服务进程设置的完全一致：
        self.m = BaseManager(address=(server_addr, 8002), authkey='lagou'.encode('utf-8'))
        # 从网络连接
        self.m.connect()
        # 第三步：获取Queue的对象
        self.task = self.m.get_task_queue()
        self.result = self.m.get_result_queue()
        # 初始化网页下载器和解析器
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        print('init finish')

    def crawl(self):
        while True:
            try:
                if not self.task.empty():
                    url = self.task.get()
                    if url == 'end':
                        print('控制节点通知爬虫节点停止工作...')
                        # 接着通知其他节点停止工作
                        self.result.put('end')
                        return
                    #print('成功获取到第%d个任务'%(316-self.task.qsize()))
                    print('该爬虫节点正在解析：%s' % url)
                    # 先下载第一页来获取总页
                    html = self.downloader.download_job(url, 1)
                    tal_page = self.parser.get_page(html)
                    print("共%d页职位信息" %tal_page)
                    for page in range(1, tal_page + 1):
                        print("正在爬取第%d页" % page + "共%d页" % tal_page)
                        html = self.downloader.download_job(url, page)
                        data = self.parser.get_job(html)
                        self.result.put(data)

            except EOFError as e:
                print("连接工作节点失败")
                return
            except Exception as e:
                print(e)
                print('crawl fail')


if __name__ == "__main__":
    spider = SpiderWork()
    spider.crawl()
