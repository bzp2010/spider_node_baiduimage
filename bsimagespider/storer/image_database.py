from __future__ import absolute_import, division, print_function, \
    with_statement
from peewee import *
from bsimagespider.storer.data_model import DataModel
from bsimagespider.parser.baidu_response_parser import BaiduResponseParser
from bsimagespider.uploader.S3Uploader import S3Uploader
import logging


class ImageDatabase:
    def __init__(self, region_name, endpoint_url, aws_access_key_id, aws_secret_access_key, bucket_name, folder_name):
        self.s3_uploader = S3Uploader(region_name, endpoint_url, aws_access_key_id, aws_secret_access_key, bucket_name, folder_name)

        self.init_database()

    @staticmethod
    def init_database():
        db = SqliteDatabase(":memory:")
        db.connect()
        try:
            db.drop_tables([DataModel])
        except:
            pass
        db.create_tables([DataModel], safe=True)
        db.close()

    def cache_json_response_to_memory(self, json_obj):
        if json_obj == []:
            logging.info("This is an invalid json obj. ")
            return

        images = BaiduResponseParser.get_image_objects_list(json_obj=json_obj)
        if images == []:
            logging.info("There is no image inside the json response")
            return

        for image in images:
            item = DataModel()
            item.image_name = BaiduResponseParser.get_image_name(image) + "." + BaiduResponseParser.get_image_extension(image)
            item.image_url = BaiduResponseParser.get_image_url(image)
            try:
                item.save()
            except Exception as e:
                logging.error(e)
            del item

