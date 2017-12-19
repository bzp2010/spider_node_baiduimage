import requests, logging

# ------ stt interface ------

# @returns: byte-like object or ConnectionError
def download_image_from_url(url):
    retry = 0
    obj = StreamFileDownloader.download_from_url(url)
    if obj == 1:
        obj = StreamFileDownloader.download_from_url(url)
        retry += 1
        if retry >= 3:
            raise ConnectionError
    return obj

# ------ end interface ------

# ------ private class ------

class StreamFileDownloader:

    # @returns: byte-like object or 1 for ConnectionError
    @staticmethod
    def download_from_url(image_url):
        try:
            req_for_image = requests.get(image_url, stream=True)
        except Exception as e:
            logging.info(e)
            return 1
        file_object_from_req = req_for_image.raw
        req_data = file_object_from_req.read()
        return req_data


# ------ private class ------

# ------ unit test ------

def test_good_download_image_from_url():
    url = """https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=335828447,2404240927&fm=27&gp=0.jpg"""
    obj = download_image_from_url(url)
    assert obj is not None

def test_bad_download_image_from_url():
    import pytest
    url = """https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=335828447,2404240927&fm=27&gp=0.jpg"""
    with pytest.raises(Exception):
        obj = download_image_from_url(url)

# ------ unit test ------