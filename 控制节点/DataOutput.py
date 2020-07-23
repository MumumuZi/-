# coding:utf-8
import pymongo
import time


class DataOutput(object):
    def __init__(self):
        self.client=pymongo.MongoClient('localhost',27017)
        self.mydb=self.client['lagou']
        self.job=self.mydb['test']

    def store_data(self, results):
        if results is None:
            return
        for result in results:
            infos={
                "positionName":result["positionName"],
                "companyShortName":result["companyShortName"],
                "companyFullName":result["companyFullName"],
                "companySize":result["companySize"],
                "industryField":result["industryField"],
                "financeStage":result["financeStage"],
                "skillLables":result["skillLables"],
                "createTime":result["createTime"],
                "city":result["city"],
                "district":result["district"],
                "salary":result["salary"],
                "workYear":result["workYear"],
                "jobNature":result["jobNature"],
                "education":result["education"],
                "positionAdvantage":result["positionAdvantage"]
                            }
            print(infos)
            #插入数据库
            self.job.insert_one(infos)
            time.sleep(0.2)


