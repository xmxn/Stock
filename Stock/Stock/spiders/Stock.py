import scrapy
import re

class StocksSpider(Scrapy.Spider):
	name = "Stock"
	start_urls = ['http://quote.eastmoney.com/stocklist.html']#百度股票链接
    
    #对页面中所有A标签的链接进行提取
    def parse(self, response):
    for href in response.css('a::attr(href)').extract():
        try:
            stock  = re.findall(r"[s][hz]\d{6}", href)[0] #通过正则表达式库获取股票代码
            url = 'https://gupiao.baidu.com/stock/' + stock +'.html' #百度股票对应的链接信息
            #将新的链接请求提交，类似一个循环
            yield scrapy.Request(url, callback=self.parse_stock) #pass_stock提取股票信息的代码
        except:
            continue
    
    def parse_stock(sef, response):
        infoDict = {}
        #提取其中的信息 by CSS Selector
        stockInfo = response.css('.stock-bets')
        name = stockInfo.css('bets-name').extract()[0]
        #选取dt标签
        keyList = stockInfo.css('dt').extract()
        #选取dd标签
        valueList = stockInfo.css('dd').extract()
        #将选取好的dt信息保存在字典中，以防免提交给Pipeline处理
        for i in range(len(keyList)):
            key = re.findall(r'>.*</dt>', keyList[i][0][1:-5]
            try:
                val = re.findall(r'\d+\.?.*</dd>', valueList[i][0][0,-5]
            except:
                val = '--'
            infoDict[key] = val
            
        #将股票信息进行更新
        infoDict.update(
                {'股票名称':refindall('\s.*\(', name)[0].split()[0] + \ re.findall('\>.*\<', name)[0][1:-i]})
        #将后续信息给到ItemPipeLine
        yield infoDict