import scrapy
import datetime


class JdDaLondonSpider(scrapy.Spider):
    name = 'jd_da_london'
    allowed_domains = ['www.indeed.co.uk']
    start_urls = ['http://www.indeed.co.uk/jobs?q=data+analyst/']

    def parse(self, response):
        jobs = response.xpath("//div[contains(@class,'jobsearch-SerpJobCard ')]")
        for job in jobs:
            
            title = job.xpath(".//h2/a/@title").get()
            rating = job.xpath("normalize-space(.//span[@class='ratingsContent']/text())").get()
            posted = job.xpath(".//span[contains(@class,'date')]/text()").get()
            url = job.xpath(".//h2/a/@href").get()

            data_1 = {
                'Title' : title,
                'Rating' : rating,
                'Posted' : posted,
                'Scrapped_On' : datetime.datetime.now().strftime("%Y-%m-%d"),
                'URL' : response.urljoin(url)
            }

            yield response.follow(url,self.parse_JD,meta=data_1)

    def parse_JD(self,response):
        data_1 = response.request.meta

        company = response.xpath("//div[contains(@class,'jobsearch-InlineCompanyRating')]/div[1]/a/text()").get()
        add = response.xpath(".//div[contains(@class,'jobsearch-InlineCompanyRating')]/div[4]/text()").get()
        pay = response.xpath(".//div[contains(@class,'jobsearch-JobMetadataHeader-item ')]/span/text()").get()

        yield {
            'Title' : data_1['Title'],
            'Rating' :  data_1['Rating'],
            'Posted' :  data_1['Posted'],
            'Scrapped_On' :  data_1['Scrapped_On'],
            'URL' : data_1['URL'],
            'Company' : company,
            'Address' : add,
            'Pay' : pay
        }
