import scrapy


class DelhijobsSpider(scrapy.Spider):
    name = 'delhijobs'
    allowed_domains = ['www.naukri.com/']
    start_urls = ['https://www.naukri.com/jobs-in-delhi/']

    def parse(self, response):
        pass
