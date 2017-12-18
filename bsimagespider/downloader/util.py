from __future__ import absolute_import, division, print_function, \
    with_statement
import requests
import json
import logging
import unittest


# ------ stt interface ------

def request_cookie(request):
    retry = 0
    s = DownloaderUtil.request_cookie(request)
    while s == 1:
        logging.info("Error -request-cookie-, retrying. ")
        s = DownloaderUtil.request_cookie(request)
        retry += 1
        if retry >= 3:
            break
    return s


def init_request(proxydict=None):
    retry = 0
    s = DownloaderUtil.init_request(proxydict)
    while s == 1:
        logging.info("Error -init-request-, retrying. ")
        s = DownloaderUtil.init_request(proxydict)
        retry += 1
        if retry >= 3:
            break
    return s

# ------ end interface ------


class DownloaderUtil:

    # @returns: Session object if successful, 1 for Exception
    @staticmethod
    def request_cookie(request):
        s = int(1)
        try:
            request.get("https://image.baidu.com/")
            s = request
        except Exception as e:
            logging.info(e)
            logging.info("Please fix your network connection status immediately")
            logging.info("the script will wait for you about 10 seconds :< ")
            s = 1
        return s

    # @returns: Session object if successful, 1 for Exception.
    @staticmethod
    def init_request(proxydict=None):
        s = int()
        try:
            s = requests.Session()
            if proxydict is None:
                pass
            else:
                # proxies = dict(http='socks5://127.0.0.1:1080',
                #                https='socks5://127.0.0.1:1080')
                # s.proxies.update(proxies)
                raise NotImplementedError("Currently proxydict is not supported. ")
        except Exception as e:
            logging.info(e)
            logging.info("network may exploding, cannot initiate a request now. ")
            s = 1
        return s


# ------ unit test ------


# ------ unit test ------