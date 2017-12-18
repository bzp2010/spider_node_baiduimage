var program = require('commander');
var webdriver = require('selenium-webdriver'),
    By = webdriver.By,
    until = webdriver.until;
var fs = require("fs");

program
    .version('1.0.0')
    .option('-l, --list [list]', '详情页地址集文件地址', 'test')
    .parse(process.argv);

var listPath = program.list;

var urlList = JSON.parse(fs.readFileSync(listPath));

var currentImgId = 0;
var imgUrlList = [];

var driver = new webdriver.Builder()
    .forBrowser('chrome')
    .build();

doGet(urlList, currentImgId);

function doResultOutput(data) {
    fs.writeFile('./result0_'+Date.now()+'.txt', JSON.stringify(data),{flag:'w',encoding:'utf-8',mode:'0666'},function(err){
        if(err){
            console.log("结果文件写入失败")
        }else{
            console.log("结果写入文件成功");
        }
    })
}

function doGet(urlList, currentId) {
    if (currentId > urlList.length - 1){
        doResultOutput(imgUrlList);
        return;
    }

    console.log('current: '+ (currentId + 1) + ' all: '+urlList.length);
    driver.get(urlList[currentId]).then(function (res){

        driver.findElement(By.xpath('//*[@id="srcPic"]/img')).then(function (res){
            res.getAttribute('src').then(function(url){
                imgUrlList.push(url);
                currentImgId++;
                doGet(urlList, currentImgId);
            }).catch(function (error) {
                console.log(error);
            });
        }).catch(function (error) {
            console.log(error);
        })
    }).catch(function (error) {
        console.log(error);
    })
}
