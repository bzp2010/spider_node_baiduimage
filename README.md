# 百度图片爬虫&amp;下载器

### 关于这个项目
###### it's a junk-like project!

### 文件说明
#### 1.baiduImgList.js 按关键词获取图片详情页面url
#### 2.baiduImgDetail.js 按图片详情页面地址获取图片url

### 使用说明
#### 1.执行 node baiduImgList.js -k [关键词] -t [抓取总页数]
##### &ensp;&ensp;**其中每页20张图片，执行结束会在运行目录产生一个result_xxx.txt**
#### 2.执行 node baiduImgDetail.js -l [第一步产生的result_xxx.txt的路径]
##### &ensp;&ensp;**执行结束会在运行目录产生一个result0_xxx.txt**

### 注意
#### 这个项目还没有完成!
##### **其中图片url获取暂未完全适配，会发生crash!**
