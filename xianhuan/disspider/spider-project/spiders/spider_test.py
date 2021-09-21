# -*- coding: utf-8 -*-
"""
Created on 2021-09-18 20:21:34
---------
@summary:
---------
@author: cxhuan
"""

import feapder
import json
from items.report_item import ReportItem


class SpiderTest(feapder.Spider):
    # 自定义数据库，若项目中有setting.py文件，此自定义可删除
    __custom_setting__ = dict(
        REDISDB_IP_PORTS="localhost:6379", REDISDB_USER_PASS="", REDISDB_DB=0
    )

    def start_requests(self):
        yield feapder.Request("http://reportapi.eastmoney.com/report/list?cb=datatable1351846&industryCode=*&pageSize=50&industry=*&rating=&ratingChange=&beginTime=2021-09-16&endTime=2021-09-17&pageNo=1&fields=&qType=0&orgCode=&code=*&rcode=&p=2&pageNum=2&_=1603724062679")

    def parse(self, request, response):
        html = response.content.decode("utf-8")
        if len(html):
            content = html.replace('datatable1351846(', '')[:-1]
            content_json = json.loads(content)
            print(content_json)

            for obj in content_json['data']:
                result = ReportItem()
                result['orgName'] = obj['orgName'] #机构名称
                result['orgSName'] = obj['orgSName'] #机构简称
                result['publishDate'] = obj['publishDate'] #发布日期
                result['predictNextTwoYearEps'] = obj['predictNextTwoYearEps'] #后年每股盈利
                result['title'] = obj['title'] #报告名称
                result['stockName'] = obj['stockName'] #股票名称
                result['stockCode'] = obj['stockCode'] #股票code
                result['orgCode'] = obj['stockCode'] #机构code
                result['predictNextTwoYearPe'] = obj['predictNextTwoYearPe'] #后年市盈率
                result['predictNextYearEps'] = obj['predictNextYearEps'] # 明年每股盈利
                result['predictNextYearPe'] = obj['predictNextYearPe'] # 明年市盈率
                result['predictThisYearEps'] = obj['predictThisYearEps'] #今年每股盈利
                result['predictThisYearPe'] = obj['predictThisYearPe'] #今年市盈率
                result['indvInduCode'] = obj['indvInduCode'] # 行业代码
                result['indvInduName'] = obj['indvInduName'] # 行业名称
                result['lastEmRatingName'] = obj['lastEmRatingName'] # 上次评级名称
                result['lastEmRatingValue'] = obj['lastEmRatingValue'] # 上次评级代码
                result['emRatingValue'] = obj['emRatingValue'] # 评级代码
                result['emRatingName'] = obj['emRatingName'] # 评级名称
                result['ratingChange'] = obj['ratingChange'] # 评级变动
                result['researcher'] = obj['researcher'] # 研究员
                result['encodeUrl'] = obj['encodeUrl'] # 链接
                result['count'] = int(obj['count']) # 近一月个股研报数
                yield result


    def download_midware(self, request):
        request.headers = {
            "Connection": "keep-alive",
            "Cookie": "qgqp_b_id=0f1ac887e1e3e484715bf0e3f148dbd8; intellpositionL=1182.07px; st_si=32385320684787; st_asi=delete; cowCookie=true; intellpositionT=741px; st_pvi=73966577539485; st_sp=2021-03-22%2009%3A25%3A40; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=4; st_psi=20210914160650551-113300303753-3491653988",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
            "Host": "reportapi.eastmoney.com"
        }
        return request

    def validate(self, request, response):
        if response.status_code != 200:
            raise Exception("response code not 200") # 重试


if __name__ == "__main__":
    SpiderTest(redis_key="spider:report").start()
