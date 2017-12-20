from bsimagespider.downloader import baidu_util, util
from multiprocessing.dummy import Pool as ThreadPool
import logging
import json
import w3lib.url
from w3lib.url import url_query_parameter


# ------ stt interface ------
# @return: download all image_name with image_url into memory database
# @ConnectionError: failed to download from baidu.
def start_download_from_baidu(keyword, image_database, threads=100):
    if type(threads) is not int:
        raise ValueError("Please give me a valid thread number. :< ")
    if threads >= 1000:
        raise ValueError("Threads cannot be greater than 1000. :< ")
    if type(keyword) is not str:
        raise ValueError("Keyword is not a string. :< ")
    if len(keyword) < 1:
        raise ValueError("Keyword too short. :< ")
    if len(keyword) >= 100:
        raise ValueError("Keyword too long. :< ")

    downloader = BaiduDownloader(keyword, image_database, threads)
    downloader.run()
    logging.info("Baidu Downloader had finish downloading. ")

# ------ end interface ------

# ------ unit test ------
def test_downloader_get_url_from_baidu():
    from bsimagespider.storer.image_database import ImageDatabase
    threads = 100
    downloader = BaiduDownloader("滑稽", ImageDatabase(region_name="nyc3",
                             endpoint_url='https://nyc3.digitaloceanspaces.com',
                             aws_access_key_id='A6LS4MC6FKL4G536NPBU',
                             aws_secret_access_key='2v8y2hx8X71GHgcuWz1nVMRHtAX47ZlBKGQPpWRosmg',
                             bucket_name="xetra-database",
                             directory="test2/", uploading_threads=threads), threads)
    urls = downloader.get_urls_from_baidu()
    assert len(urls) >= 25
    assert type(urls) is list

def test_save_image_from_url():
    from bsimagespider.storer.image_database import ImageDatabase
    from bsimagespider.storer.image_database import DataModel
    threads = 100
    downloader = BaiduDownloader("滑稽", ImageDatabase(region_name="nyc3",
                                                     endpoint_url='https://nyc3.digitaloceanspaces.com',
                                                     aws_access_key_id='A6LS4MC6FKL4G536NPBU',
                                                     aws_secret_access_key='2v8y2hx8X71GHgcuWz1nVMRHtAX47ZlBKGQPpWRosmg',
                                                     bucket_name="xetra-database",
                                                     directory="test2/", uploading_threads=threads), threads)
    urls = downloader.get_urls_from_baidu()
    assert len(urls) >= 25
    assert type(urls) is list
    downloader.save_images_from_url(urls[0])
    images = DataModel.select()
    assert type(images[0].image_url) is str
    assert type(images[0].image_name) is str
    assert len(images[0].image_url) > 10
    assert len(images[0].image_name) > 10

# ------ unit test ------

# ------ stt class ------

class BaiduDownloader:
    def __init__(self, keyword, image_database, threads=100):
        self.keyword = keyword
        self.threads = threads
        self.image_database = image_database

    # get all urls that need to be scrapped
    def get_urls_from_baidu(self):
        target_urls = []
        step = 30
        total_images = baidu_util.get_total_image_of_baidu_engine(BaiduDownloader.prepare_a_request(), self.keyword)
        total_steps = int(total_images/step)+1
        keyword = self.keyword
        raw_url = """https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%BB%91%E7%A8%BD&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E6%BB%91%E7%A8%BD&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn=90&rn=30&gsm=5a&1513615762697="""
        new_url_with_keyword = w3lib.url.add_or_replace_parameter(raw_url, "queryWord", str(keyword))
        new_url_with_keyword = w3lib.url.add_or_replace_parameter(new_url_with_keyword, "word", str(keyword))
        for p in range(total_steps):
            pn = p*step
            target_urls.append(w3lib.url.add_or_replace_parameter(new_url_with_keyword, "pn", str(pn)))
        return target_urls

    def run(self):
        target_urls = self.get_urls_from_baidu()

        threads = self.threads
        target_chunks = [target_urls[x:x + 1000] for x in range(0, len(target_urls), 1000)]
        for chunk in target_chunks:
            pool = ThreadPool(int(threads))
            pool.map(self.save_images_from_url, chunk)
            pool.close()
            pool.join()

    def save_images_from_url(self, target):
        s = None
        try:
            s = self.prepare_a_request()
        except ConnectionError as e:
            logging.error(e)
            raise ConnectionError("Please check your internet connection. ")

        json_obj = None
        try:
            json_obj = self.json_obj_from_url(s, target)
        except ConnectionError as e:
            logging.error(e)
            raise ConnectionError("Please check your internet connection. ")

        self.save_result_to_memory(self.image_database, json_obj)

    # prepare a request with good session
    @staticmethod
    def prepare_a_request():
        s = util.request_cookie(util.init_request(proxydict=None))
        if s is not None:
            return s
        else:
            raise ConnectionError

    # @returns: json dict or Exception for ConnectionError
    def json_obj_from_url(self, request, url):
        retry = 0
        response = self.download_url_response(request, url)
        while response == 1:
            response = self.download_url_response(request, url)
            retry += 1
            if retry >= 3:
                raise ConnectionError
        try:
            json_obj = self.parse_response_to_obj(response)
        except Exception as e:
            logging.info(e)
            return []
        return json_obj

    # response or 1 for ConnectionError
    @staticmethod
    def download_url_response(request, url):
        s = int()
        try:
            s = request.get(url)
        except Exception as e:
            logging.info(e)
            s = 1
        return s

    # parse response to json dict
    @staticmethod
    def parse_response_to_obj(response):
        return json.loads(response.content.decode())

    # save json obj to database
    @staticmethod
    def save_result_to_memory(image_database, json_dict):
        image_database.json_response_to_memory(json_dict)

# ------ end class ------
