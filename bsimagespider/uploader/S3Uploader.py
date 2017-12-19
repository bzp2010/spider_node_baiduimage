import boto3, logging, time


class S3Uploader:
    def __init__(self, region_name, endpoint_url, aws_access_key_id, aws_secret_access_key, bucket_name, directory):
        self.region_name = region_name
        self.endpoint_url = endpoint_url
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.bucket_name = bucket_name
        self.directory = directory
        self.client = self.init_client()

    def init_client(self):
        retry = 0
        client = self.connect_to_S3()
        while client == 1:
            client = self.connect_to_S3()
            retry += 1
            time.sleep(1)
            if retry >= 5:
                raise ConnectionError("Can't connect to S3, please check your internet. ")
        return client

    # @returns: boto3 Session.client if succeed, 1 for ConnectionError
    def connect_to_S3(self):
        try:
            session = boto3.session.Session()
            client = session.client('s3',
                                    region_name=self.region_name,
                                    endpoint_url=self.endpoint_url,
                                    aws_access_key_id=self.aws_access_key_id,
                                    aws_secret_access_key=self.aws_secret_access_key)
            return client
        except Exception as e:
            logging.info(e)
            return 1

    # @returns: 0 if uploaded, 1 for ConnectionError
    def upload_file_to_s3(self, file_name):
        try:
            self.client.upload_file(file_name, self.bucket_name, self.directory + file_name)
            return 0
        except Exception as e:
            logging.info(e)
            return 1
    # ------ stt interface ------

    def upload_image_to_s3(self, image_url, image_name):


    # ------ end interface ------