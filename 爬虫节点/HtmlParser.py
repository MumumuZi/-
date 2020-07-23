# coding:utf-8
import re
import urllib.parse
from bs4 import BeautifulSoup
import json
import math


class HtmlParser(object):

    def get_page(self, html_cont):
        '''
        获取职位列表的页数信息
        :param json:
        :return: 总页数
        '''
        if html_cont is None:
            return
        json_data = json.loads(html_cont)
        total_Count = json_data['content']['positionResult']['totalCount']
        # 拉钩网在搜索城市没有符合条件的职位时会显示全国的职位
        if total_Count > 10000:
            return 0
        # 每页15个职位
        page_num = math.ceil(total_Count / 15)
        # 拉钩网最多展示30页职位信息
        if page_num < 30:
            return page_num
        else:
            return 30

    def get_job(self, html_cont):
        '''
        获取职位相关信息
        :param html_cont: 页面内容
        :return:返回一页的工作信息
        '''
        json_data = json.loads(html_cont)
        results = json_data['content']['positionResult']['result']
        return results
