# coding:utf-8
from multiprocessing.managers import BaseManager
from multiprocessing import Process, Queue
from UrlManager import UrlManager
from DataOutput import DataOutput
import time


class NodeManager(object):

    def start_Manager(self, url_q, result_q):
        '''
        创建一个分布式管理器
        :param url_q: url队列
        :param result_q: 结果队列
        :return:
        '''
        # 把创建的两个队列注册在网络上，利用register方法，callable参数关联了Queue对象，将Queue对象在网络上暴露
        BaseManager.register('get_task_queue', callable=get_task)
        BaseManager.register('get_result_queue', callable=get_result)
        # 绑定端口8001，设置验证口令‘baike’，相当于对象的初始化
        manager = BaseManager(address=('127.0.0.1', 8002), authkey='lagou'.encode('utf-8'))
        # 返回manager对象
        return manager

    def url_manager_proc(self, url_q):
        '''
        url管理进程将url_q中的待爬取城市传递给爬虫节点
        :param url_q:管理进程通将url传递给爬虫节点的通道
        :return:
        '''
        url_manager = UrlManager()
        while True:
            while (url_manager.has_new_url()):
                # 从URL管理器获取新的url
                new_url = url_manager.get_new_url()
                # 将新的URL发给工作节点
                url_q.put(new_url)
            # 通知爬虫节点停止工作
            url_q.put('end')
            # 关闭管理节点，同时存储set状态
            url_manager.save_progress('new_city.txt', url_manager.new_urls)
            url_manager.save_progress('old_city.txt', url_manager.old_urls)
            return

    def result_solve_proc(self, result_q, store_q):
        '''
        将获取到的职位信息添加到store_q队列交给数据存储进程。
        :param result_q:
        :param store_q:
        :return:
        '''
        while True:
            try:
                if not result_q.empty():
                    content = result_q.get(True)
                    if content == 'end':
                        # 结果分析进程接受通知然后结束
                        print('结果分析进程接受通知然后结束！')
                        store_q.put('end')
                        return
                    store_q.put(content)  # 解析出来的数据是字典类型
                else:
                    time.sleep(0.1)  # 延时休息
            except BaseException as e:
                time.sleep(0.1)  # 延时休息

    def store_proc(self, store_q):
        '''
        数据存储进程从store_q中读取数据并调用数据存储器进行存储
        :param store_q:
        :return:
        '''
        output = DataOutput()
        while True:
            if not store_q.empty():
                data = store_q.get()
                if data == 'end':
                    print('存储进程接受通知然后结束！')
                    return
                output.store_data(data)
            else:
                time.sleep(0.2)
        pass


if __name__ == '__main__':
    # 初始化4个队列
    url_q = Queue()
    result_q = Queue()
    store_q = Queue()


    def get_task():
        return url_q


    def get_result():
        return result_q


    # 创建分布式管理器
    node = NodeManager()
    manager = node.start_Manager(url_q, result_q)
    # 创建URL管理进程、数据提取进程和数据存储进程
    url_manager_proc = Process(target=node.url_manager_proc,
                               args=(url_q,))
    result_solve_proc = Process(target=node.result_solve_proc, args=(result_q, store_q,))
    store_proc = Process(target=node.store_proc, args=(store_q,))
    # 启动3个进程和分布式管理器
    url_manager_proc.start()
    result_solve_proc.start()
    store_proc.start()
    manager.get_server().serve_forever()
