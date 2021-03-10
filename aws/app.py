import crochet
crochet.setup()  # initialize crochet before further imports
import time
import multiprocessing
from flask import Flask, request, jsonify
from flask_caching import Cache
import scrapers.scrap as scraper

# from scrapers.bedbat import BlogSpider
from scrapers.amazon import BlogSpider
from scrapy.crawler import CrawlerProcess

# from klein import route, run
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher


cache = Cache()

app = Flask(__name__)
output_data = []
app.config['CACHE_TYPE'] = 'simple'
cache.init_app(app)

crawl_runner = CrawlerRunner()

def cache_key():
    return request.get_json()["keyword"]


@app.route('/', methods=['GET'])
def helloGET():
    # return str(time.ctime()) + " Your Server CPU: " + str(multiprocessing.cpu_count())
    
    scrape_with_crochet()
    return jsonify(output_data)


@app.route('/search', methods=['GET', 'POST'])
@cache.cached(timeout=86400, key_prefix=cache_key)
def search():
    # data = request.get_json()
    # if "keyword" not in data:
    #     print("ERROR")
    #     return "ERROR no Keyord"
    # keyword = data["keyword"]
    keyword = "bed"
    scrapinglist = scraper.search(keyword)
    return scrapinglist

@crochet.wait_for(timeout=60.0)
def scrape_with_crochet():
    # signal fires when single item is processed
    # and calls _crawler_result to append that item
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    print("hlleoget---+++++----")
    eventual = crawl_runner.crawl(BlogSpider)
    print("hlleoget-------")
    return eventual  # returns a twisted.internet.defer.Deferred

def _crawler_result(item, response, spider):
    """
    We're using dict() to decode the items.
    Ideally this should be done using a proper export pipeline.
    """
    print("7242423")
    output_data.append(dict(item))
 
if __name__ == '__main__':
    app.run(host= '0.0.0.0')