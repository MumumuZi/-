# coding:utf-8
import requests
from bs4 import BeautifulSoup
import pickle

class GetCity(object):
    def download(self, url):
        if url is None:
            print("url为空")
            return None
        # 通过头部构造伪装成浏览器的正常访问
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
        headers = {'User-Agent': user_agent}
        r = requests.post(url, headers=headers)
        if r.status_code == 200:
            # 请求页面状态码为200表示请求成功
            r.encoding = 'utf-8'
            return r.text
        return None

    def parser_city(self, html_cont):
        '''
        用于解析html网页中的城市列表
        :param html_cont: 下载页面的内容
        :return:城市列集合
        '''
        if html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser')
        city_list = set()
        citys = soup.find('table', class_='word_list').find_all('a')
        for city in citys:
            city_list.add(city.get_text())
        return city_list

    def save_progress(self, path, data):
        '''
        保存进度
        :param path:文件路径
        :param data:数据
        :return:
        '''
        with open(path, 'wb') as f:
            pickle.dump(data, f)

    def load_progress(self, path):
        '''
        从本地文件加载进度
        :param path:文件路径
        :return:返回set集合
        '''
        print('[+] 从文件加载进度: %s' % path)
        try:
            with open(path, 'rb') as f:
                tmp = pickle.load(f)
                return tmp
        except:
            print('[!] 无进度文件, 创建: %s' % path)
        return set()

if __name__ =='__main__':
    getcity=GetCity()
    city_url="https://www.lagou.com/jobs/allCity.html?px=new&city=%E5%8C%97%E4%BA%AC&positionNum=500+&companyNum=0&isCompanySelected=false&labelWords="
    html=getcity.download(city_url)
    city_list=getcity.parser_city(html)
    getcity.save_progress("new_city.txt",city_list)
    city=getcity.load_progress("new_city.txt")
    print("共获取到%d个城市"%len(city))
    print(city)