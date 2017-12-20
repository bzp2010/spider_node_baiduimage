from __future__ import absolute_import, division, print_function, \
    with_statement
from bsimagespider.downloader import baidu_downloader
from bsimagespider.storer.image_database import ImageDatabase


class BSImageSpider:
    def __init__(self, region_name, endpoint_url, aws_access_key_id, aws_secret_access_key, bucket_name, directory,
                 keyword_to_search, threads=100):
        self.region_name           = region_name
        self.endpoint_url          = endpoint_url
        self.aws_access_key_id     = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.bucket_name           = bucket_name
        self.directory             = directory
        self.keyword_to_search     = keyword_to_search
        self.threads               = threads

    def check_and_display_configurations(self):
        print("self.region_name           is: %s "%(self.region_name          ))
        print("self.endpoint_url          is: %s "%(self.endpoint_url         ))
        print("self.aws_access_key_id     is: %s "%(self.aws_access_key_id    ))
        print("self.aws_secret_access_key is: %s "%(self.aws_secret_access_key))
        print("self.bucket_name           is: %s "%(self.bucket_name          ))
        print("self.directory             is: %s "%(self.directory            ))
        print("self.keyword_to_search     is: %s "%(self.keyword_to_search    ))
        print("self.threads               is: %s "%(self.threads              ))

    def init_database(self):
        return ImageDatabase(region_name=self.region_name,
                                 endpoint_url=self.endpoint_url,
                                 aws_access_key_id=self.aws_access_key_id,
                                 aws_secret_access_key=self.aws_secret_access_key,
                                 bucket_name=self.bucket_name,
                                 directory=self.directory,
                                 uploading_threads=self.threads)

    def scrape_baidu_image_and_save_to_memory_database(self, database):
        baidu_downloader.start_download_from_baidu(self.keyword_to_search, database, self.threads)


def main():
    # S3 Credentials
    print("Please give me your S3 Credentials. ")
    region_name = input("Region name: ")
    endpoint_url = input("End point url: ")
    aws_access_key_id = input("aws access key id: ")
    aws_secret_access_key = input("aws secret access key: ")
    bucket_name = input("bucket name or space name: ")
    directory = input("directory name: ")
    # Image keyword to search
    keyword_to_search = input("Keyword to search: ")
    # Threads to use
    threads = int(input("How many threads you want to use? "))

    spider = BSImageSpider(region_name, endpoint_url, aws_access_key_id, aws_secret_access_key, bucket_name, directory, keyword_to_search, threads)
    database = spider.init_database()
    print("Start Download images from baidu search engine, please wait... ")
    spider.scrape_baidu_image_and_save_to_memory_database(database)
    print("Start Uploading images to S3, please wait... ")
    database.upload_images_to_s3()


if __name__ == '__main__':
    main()
