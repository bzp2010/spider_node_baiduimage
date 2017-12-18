var program = require('commander');
var webdriver = require('selenium-webdriver'),
    By = webdriver.By,
    until = webdriver.until;
var fs = require("fs");

program
    .version('1.0.0')
    .option('-k, --keyword [keyword]', '抓取关键词', 'test')
    .option('-t, --time [time]', '抓取页数', 10)
    .parse(process.argv);

var keyword = program.keyword;
var maxPage = program.time;

var urlList = [];

var driver = new webdriver.Builder()
    .forBrowser('chrome')
    .build();

doGet(0, maxPage);

function doResultOutput(data) {
    fs.writeFile('./result_'+Date.now()+'.txt', JSON.stringify(data),{flag:'w',encoding:'utf-8',mode:'0666'},function(err){
        if(err){
            console.log("结果文件写入失败")
        }else{
            console.log("结果写入文件成功");

        }
    })
}

function doGet(page, time) {
    if (page > time) {
        doResultOutput(urlList);
        return;
    }

    console.log("page: " +page+ " max: "+ time);
    driver.get('https://image.baidu.com/search/flip?tn=baiduimage&word='+keyword+'&pn='+page * 20).then(function (res){
        driver.findElements(By.className('imglink')).then(function (res){
            for(var i = 0; i < res.length; i++){
                res[i].getAttribute('href').then(function(url){
                    urlList.push(url);
                });

            }
            page++;
            doGet(page, time);
        });
    });
}
