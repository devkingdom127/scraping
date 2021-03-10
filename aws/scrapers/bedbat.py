import os
import sys
import time
import scrapy
from scrapy.crawler import CrawlerProcess
from threading import Thread
from sys import platform
import config
import helpers

BASE_URL = "https://www.bedbathandbeyond.com/store/product/"
AFFILIATE_KEY = "bedbat"

class Bedbatcom( Thread):
    def __init__(self, searchkey):
        self.timeout = 30
        # self.first_driver = first_driver
        self.searchkey = searchkey
        print("searchkey---->", searchkey)
        self.goodlist = []

        self.start_url = 'https://www.bedbathandbeyond.com/store/s/'
        
        if platform == "linux" or platform == "linux2":
                self.input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver")
        elif platform == "win32":
                self.input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver.exe")
        super(Bedbatcom, self).__init__()
    def scroller(self, timeout):
        last_height = self.first_driver.execute_script("return document.body.scrollHeight")
        new_height = 0
        print("new height--->", new_height)
        while True:
            self.first_driver.execute_script(f"window.scrollTo(0,  {new_height+100});")
            new_height +=100
            if new_height >= last_height*10:
                break
        time.sleep(1)

    def run(self):
        try : 
            # self.first_driver = self.open_chrome()
            # self.first_driver.delete_all_cookies()
            # chrome = self.first_driver.get(self.start_url + self.searchkey)
            print("chrome=====>")
            process = CrawlerProcess({
                'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
            })

            process.crawl(BlogSpider)
            process.start()
        except:
            pass

        # process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})

        # process.crawl(BlogSpider)
        # process.start()

class BlogSpider(scrapy.Spider):

    name = 'blogspider'
    start_url = 'https://www.bedbathandbeyond.com/store/s/'
    searchkey = 'bed'
    goodlist = []
    def start_requests(self):
        print("start")
        yield scrapy.Request(url='https://www.bedbathandbeyond.com/store/s/bed', callback=self.parse, headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"})
   
    def parse(self, response):

        obj = response.css("article.tealium-product-card")
        print("======obj=======", len(obj))
        if ( len(obj) == 0):
            print("Bedbathandbeyond.com : Please Enter Correct Key.")
            return
        
        total = 0
        for li in obj:
            dic ={}           

            image = li.css("div.Thumbnail_4q2qnF img::attr(src)").extract()

            if ( image is not None):
                dic['image1'] = image
                print("image1===>", dic['image1'])
                image2 = li.css("div.ProductTile-inline_6bSQ4q a::attr(href)").extract()
                print("image2----->", image2)
                #dic['detail'] = helpers.format_impact_affiliate_link("https://www.bedbathandbeyond.com" + image2, BASE_URL, AFFILIATE_KEY)
                
            price = li.css("span.Price_3HnIBb")
            if ( price is not None ):
                pass
                dic['price'] = helpers.strip_text_from_price(price.css("span::text").get())
            else: 
                dic['price']=""

            print("price===>", dic['price'])

            title = li.css("div.tealium-product-title")            
            if (title is not None):
                dic['title'] = title.css("a::text").get()
            
            rate = li.css("span.Rating_3RTQ2U")
            if (rate is not None):
                dic['rate'] = rate.css("span::text").get()            

            shipmsg = li.css("p.ProductTile-inline_36NSEc")   
            if ( shipmsg is not None):
                dic['shipmsg'] = shipmsg.css("p::text").get()

            dic["source"] = config.sources["bedbathandbeyond"]
            print("source=====>", dic['source'])
            total += 1

            self.goodlist.append(dic)
            if ( total >= config.max_items):
                print("barnesandnoble.com:  " , total)
                return self.goodlist
 # the script will block here until the crawling is finished