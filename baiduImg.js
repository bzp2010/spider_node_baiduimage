var program = require('commander');
var webdriver = require('selenium-webdriver'),
    By = webdriver.By,
    until = webdriver.until;
var fs = require("fs");

program
    .version('1.0.0')
    .option('-k, --keyword [keyword]', '抓取关键词', 'test')
    .option('-t, --time [time]', '抓取张数', 10)
    .option('-b, --browser [browser]', '浏览器核心', 'chrome')
    .parse(process.argv);

var keyword = program.keyword;
var maxId = program.time;
var browser = program.browser;
var currentId = 0;
var imgUrlList = [];


var driver = new webdriver.Builder()
    .forBrowser(browser)
    .build();

driver.get("http://image.baidu.com/search/detail?word="+keyword+"&tn=baiduimagedetail").then(doGet);

function doResultOutput(data) {
    fs.writeFile('./result_'+Date.now()+'.txt', JSON.stringify(data),{flag:'w',encoding:'utf-8',mode:'0666'},function(err){
        if(err){
            console.log("结果文件写入失败")
        }else{
            console.log("结果写入文件成功");
        }
    });
    driver.quit();
}

function doGet() {
    if (currentId > maxId){
        doResultOutput(imgUrlList);
        return;
    }

    driver.wait(until.elementLocated(By.css('#srcPic > img')), 3000);

    driver.findElement(By.css('#srcPic > img')).then(function (element){
        driver.sleep(500);
        element.getAttribute('src').then(function(url){

            console.log("current: "+currentId+" url: "+url);

            imgUrlList.push(url);
            currentId++;
            //切换下一张图片
            driver.findElement(By.className("img-next")).then(function (element) {
                element.click();
                doGet();
            }).catch(function (error) {
                console.log(error);
            })

        }).catch(function (error) {
            console.log(error);
        });
    }).catch(function (error) {
        console.log(error);
    });


}
