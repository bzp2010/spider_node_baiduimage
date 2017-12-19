from __future__ import absolute_import, division, print_function, \
    with_statement
import re

# ------ stt interface ------

class BaiduResponseParser:
    @staticmethod
    def get_image_objects_list(json_obj):
        if 'data' in json_obj:
            return json_obj['data']
        else:
            return []

    @staticmethod
    def get_image_url(image_object):
        if 'middleURL' in image_object:
            try:
                re.match(r"""^(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})$""", image_object['middleURL']).group(0)
            except AttributeError as e:
                return None
            return image_object['middleURL']
        else:
            return None

    @staticmethod
    def get_image_name(image_object):
        if 'fromPageTitleEnc' in image_object:
            return image_object['fromPageTitleEnc']
        else:
            return None

    @staticmethod
    def get_image_extension(image_object):
        image_url = BaiduResponseParser.get_image_url(image_object)
        if image_url is not None:
            return image_url.split(".")[-1]
        else:
            return None

# ------ end interface ------

# ------ stt unittest ------


def test_good_get_image_object_list():
    import requests, json
    s = requests.Session()
    s.get("https://image.baidu.com")
    response = s.get("https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%BB%91%E7%A8%BD&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E6%BB%91%E7%A8%BD&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn=90&rn=30&gsm=5a&1513663408629=")
    assert response.text is not None
    json_obj = json.loads(response.text)
    object_list = BaiduResponseParser.get_image_objects_list(json_obj)
    assert len(object_list) > 20

def test_good_get_image_url():
    import requests, json
    s = requests.Session()
    s.get("https://image.baidu.com")
    response = s.get(
        "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%BB%91%E7%A8%BD&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E6%BB%91%E7%A8%BD&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn=90&rn=30&gsm=5a&1513663408629=")
    assert response.text is not None
    json_obj = json.loads(response.text)
    object_list = BaiduResponseParser.get_image_objects_list(json_obj)
    assert len(object_list) > 20
    valid_total = 0
    for object in object_list:
        image_url = BaiduResponseParser.get_image_url(object)
        if image_url is not None:
            assert re.match(r"""^(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})$""", image_url).group(0) is not None
            valid_total += 1
        else:
            pass
    assert valid_total >= 25

def test_good_get_image_name():
    import requests, json
    s = requests.Session()
    s.get("https://image.baidu.com")
    response = s.get(
        "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%BB%91%E7%A8%BD&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E6%BB%91%E7%A8%BD&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn=90&rn=30&gsm=5a&1513663408629=")
    assert response.text is not None
    json_obj = json.loads(response.text)
    object_list = BaiduResponseParser.get_image_objects_list(json_obj)
    assert len(object_list) > 20
    valid_total = 0
    for object in object_list:
        image_name = BaiduResponseParser.get_image_name(object)
        if image_name is not None and len(image_name) > 4:
            valid_total += 1
        else:
            pass
    assert valid_total >= 25

def test_good_get_image_extension():
    import requests, json
    s = requests.Session()
    s.get("https://image.baidu.com")
    response = s.get(
        "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%BB%91%E7%A8%BD&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E6%BB%91%E7%A8%BD&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn=90&rn=30&gsm=5a&1513663408629=")
    assert response.text is not None
    json_obj = json.loads(response.text)
    object_list = BaiduResponseParser.get_image_objects_list(json_obj)
    assert len(object_list) > 20
    valid_total = 0
    for object in object_list:
        extension = BaiduResponseParser.get_image_extension(object)
        if extension is not None:
            valid_total += 1
        else:
            pass
    assert valid_total >= 25


# ------ end unittest ------
