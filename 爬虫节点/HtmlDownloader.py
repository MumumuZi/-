# coding:utf-8
import requests
import time


class HtmlDownloader(object):
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}

    def get_cookie(self):
        url = "https://www.lagou.com/jobs/list_python?city=?&cl=false&fromSearch=true&labelWords=&suginput="
        s = requests.session()
        s.get(url, headers=self.headers, timeout=3)
        cookie = s.cookies
        return cookie

    def download_job(self, city, page):
        '''
        下载工作列表的json文件
        :param url: 要下载的url
        :param page: 页码
        :return:返回json文件
        '''
        url="https://www.lagou.com/jobs/positionAjax.json?px=default&city=%s&needAddtionalResult=false" % city
        referer="https://www.lagou.com/jobs/list_python?&px=default&city=%s"% city
        self.headers['Referer']=referer.encode()
        params = {
            "pn": str(page),
            "kd": "python"
        }
        try:
            r = requests.post(url, data=params, headers=self.headers, cookies=self.get_cookie(), timeout=5)
            while "频繁" in r.text:
                print("访问频繁，等待中")
                time.sleep(3)
                r = requests.post(url, data=params, headers=self.headers, cookies=self.get_cookie(), timeout=5)
            r.encoding = "utf-8"
            return r.text
        except Exception as e:
            print(e)
