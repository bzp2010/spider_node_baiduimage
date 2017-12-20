import boto3, logging, time
from bsimagespider.downloader import stream_file_downloader
import re


class S3Uploader:
    # ------ stt interface ------

    # @returns: Exception for Error uploading
    def upload_image_to_s3(self, image_name, image_url):
        image_stream = stream_file_downloader.download_image_from_url(image_url)
        retry = 0
        result = self.upload_file_to_s3(image_name, image_stream)
        while result == 1:
            result = self.upload_file_to_s3(image_name, image_stream)
            retry += 1
            if retry >= 3:
                raise ConnectionError("Can't upload file to S3 bucket")

    # ------ end interface ------


    # ------ stt private ------
    def __init__(self, region_name, endpoint_url, aws_access_key_id, aws_secret_access_key, bucket_name, directory):
        if type(region_name) is not str:
            raise AttributeError("Region name is not valid. ")
        self.region_name = region_name

        try:
            re.match(r'(\b(https?|ftp|file)://)?[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]', endpoint_url).group(0)
        except AttributeError as e:
            raise AttributeError("Endpoint url is not valid. ")
        self.endpoint_url = endpoint_url

        if type(aws_access_key_id) is not str:
            raise AttributeError("Access key id is not valid. ")
        self.aws_access_key_id = aws_access_key_id

        if type(aws_secret_access_key) is not str:
            raise AttributeError("Secret access key is not valid. ")
        self.aws_secret_access_key = aws_secret_access_key

        if type(bucket_name) is not str:
            raise AttributeError("Bucket name is not valid. ")
        self.bucket_name = bucket_name

        if type(directory) is not str:
            raise AttributeError("Directory is not valid. ")
        if str(directory).endswith("/") is not True:
            raise AttributeError("Directory is not ending with '/' . ")
        self.directory = directory

        self.client = self.connect_to_S3()

    # @returns: boto3 Session.client if succeed, 1 for ConnectionError
    def connect_to_S3(self):
        session = boto3.session.Session()
        client = session.client('s3',
                                region_name=self.region_name,
                                endpoint_url=self.endpoint_url,
                                aws_access_key_id=self.aws_access_key_id,
                                aws_secret_access_key=self.aws_secret_access_key)
        return client

    # @returns: 0 if uploaded, 1 for ConnectionError
    def upload_file_to_s3(self, file_name, file_stream):
        try:
            self.client.upload_fileobj(file_stream, self.bucket_name, self.directory + file_name)
            return 0
        except Exception as e:
            logging.info(e)
            return 1

    # ------ end private ------


