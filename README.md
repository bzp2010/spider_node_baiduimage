# Baidu + Sogou Image Spider
> this project is mainly used to download images from baidu + sogou.

The spider will take your Amazon S3 Information which will be the database for the result image. If you don't have a S3 yet, you can use alternatives like DigitalOcean space which is also a great storage provider.

# How to use the code
Run the code in shell, python3 is recommended, you will need to install the dependencies first.
```
pip install -r requirements.txt
<activate your conda/virtual env environment here>
python3 run.py
```
It will ask you S3 credentials and foldername as well as the keywords you want to scrape. It will then go through sogou, baidu image and take those images into your S3 folder.

# About proxy
> This feature will be supported in the future

# About retry and network connection 
> If a request failed, the code will retry for 3 times.

# Debug mode
> This feature will be supported in the future

# Contribution
> Welcome and appreciate :) 
