import scrapy
from scrapy_playwright.page import PageMethod
from urllib.parse import urlencode

API_KEY = 'Your_API_KEY'

def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

class WalmartDummySpiderSpider(scrapy.Spider):
    name = "walmart_Dummy_Spider"
    
    def start_requests(self):
        url = "https://www.walmart.com/browse/clothing/womens-boots/5438_1045804_1045806_3142010_1228542?povid=FashionTopNav_Women_Shoes_Boots"
        yield scrapy.Request(url=get_proxy_url(url), meta=dict(
                playwright = True,
                playwright_include_page = True, 
                playwright_page_methods =[PageMethod
                ('wait_for_selector', 'div.flex-wrap')]), callback=self.parse)

    async def parse(self, response):
        product_container = response.css('div.mb0')
        product = product_container.css('div[data-testid="list-view"]')
        product_name_div = product.css('div[data-automation-id="product-price"]') 
        yield {
            "price" : product_name_div.css('span.w_iUH7::text').get()

        }
