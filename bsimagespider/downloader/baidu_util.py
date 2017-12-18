from __future__ import absolute_import, division, print_function, \
    with_statement
import requests
import json
import logging
import unittest
import w3lib.url
from w3lib.url import url_query_parameter

# ------ stt interface ------
def get_total_image_of_baidu_engine(request, keyword=1):
    BaiduUtil.request_total_images_of_baidu_engine(request, keyword)

# ------ end interface ------


# ------ start private ------
class BaiduUtil:

    # private method for request_total_image_of_baidu_engine
    @staticmethod
    def parse_total_images_of_baidu_engine(response_dict):
        if "displayNum" in response_dict:
            return response_dict['displayNum']
        else:
            return None

    # @returns[int]: (total images) in baidu image engine.
    # @if the request get error, return None
    @staticmethod
    def request_total_images_of_baidu_engine(request, keyword=1):
        if keyword == 1:
            raise ValueError("Hey, tell me what is your keyword, how can I search with out a keyword? :< ")
        raw_url = """https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%BB%91%E7%A8%BD&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E6%BB%91%E7%A8%BD&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn=90&rn=30&gsm=5a&1513615762697="""
        new_url_with_keyword = w3lib.url.add_or_replace_parameter(raw_url, "queryWord", str(keyword))
        new_url_with_keyword = w3lib.url.add_or_replace_parameter(new_url_with_keyword, "word", str(keyword))
        s = request
        response_dict = None
        try:
            response = s.get(new_url_with_keyword)
            response_dict = json.loads(response)
        except Exception as e:
            logging.info(e)
            logging.info("Total image of baidu request failed. ")
            return None
        total = None
        try:
            total = BaiduUtil.parse_total_images_of_baidu_engine(response_dict)
        except ValueError as e:
            logging.info(e)
            logging.info("Total image of baidu response can't be parsed ! :< ")
            return None
        if total is None:
            return None
        else:
            return int(total)



# ------ end private ------

# ------ unit test ------

# depends on util, run util test before this test
def test_request_total_image_of_baidu():
    from bsimagespider.downloader import util
    request =

# ------ unit test ------