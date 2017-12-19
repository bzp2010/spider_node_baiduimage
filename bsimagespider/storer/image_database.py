from __future__ import absolute_import, division, print_function, \
    with_statement
from peewee import *
from bsimagespider.storer.data_model import DataModel
from bsimagespider.parser.baidu_response_parser import BaiduResponseParser
from bsimagespider.uploader.S3Uploader import S3Uploader
import logging
from multiprocessing.dummy import Pool as ThreadPool



class ImageDatabase:
    def __init__(self, region_name, endpoint_url, aws_access_key_id, aws_secret_access_key, bucket_name, directory, uploading_threads=100):
        try:
            s3_uploader = S3Uploader(region_name, endpoint_url, aws_access_key_id, aws_secret_access_key, bucket_name, directory)
            del s3_uploader
            self.region_name = region_name
            self.endpoint_url = endpoint_url
            self.aws_access_key_id = aws_access_key_id
            self.aws_secret_access_key = aws_secret_access_key
            self.bucket_name = bucket_name
            self.directory = directory
        except Exception as e:
            logging.error(e)
            raise AttributeError("This is an invalid S3 credential. ")
        if type(uploading_threads) is not int:
            raise AttributeError("Uploading threads must be a string type. ")
        if uploading_threads > 1000:
            raise AttributeError("Thread can not be greater than 1000. ")
        self.uploading_threads = uploading_threads
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

    def json_response_to_memory(self, json_obj):
        if json_obj == []:
            logging.info("This is an invalid json obj. ")
            return

        images = BaiduResponseParser.get_image_objects_list(json_obj=json_obj)
        if images == []:
            logging.info("There is no image inside the json response")
            return

        for image in images:
            image_name = BaiduResponseParser.get_image_name(image)
            image_extension = BaiduResponseParser.get_image_extension(image)
            image_url = BaiduResponseParser.get_image_url(image)
            if image_name is None or image_extension is None or image_url is None:
                logging.info("This is not a valid image. ")
                return
            file_name = image_name + "." + image_extension
            image_url = image_url
            item = DataModel()
            item.image_name = file_name
            item.image_url = image_url
            try:
                item.save()
            except Exception as e:
                logging.error(e)
            del item

    def upload_images_to_s3(self):
        images = DataModel.select()

        images_chunks = [images[x:x + 1000] for x in range(0, len(images), 1000)]
        try:
            for chunk in images_chunks:
                pool = ThreadPool(int(self.uploading_threads))
                pool.map(self.async_data_to_s3, chunk)
                pool.close()
                pool.join()
        except RuntimeError as e:
            logging.error(e)
            logging.error("I can't start that many threads, calm down okay? :< ")

    def async_data_to_s3(self, image):
        s3_uploader = S3Uploader(self.region_name, self.endpoint_url, self.aws_access_key_id, self.aws_secret_access_key,
                                 self.bucket_name, self.directory)
        try:
            s3_uploader.upload_image_to_s3(image.image_name, image.image_url)
        except ConnectionError as e:
            logging.info("1 Image upload failed :< ")