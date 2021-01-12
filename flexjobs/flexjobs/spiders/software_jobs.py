import scrapy


class SoftwareJobsSpider(scrapy.Spider):
    name = 'software_jobs'
    allowed_domains = ['www.flexjobs.com']
    start_urls = ['https://www.flexjobs.com/jobs/web-software-development-programming/']
        

    def parse(self, response):
        jobs = response.xpath("//h5[@class='font-weight-bold']/a/@href")
        for job in jobs:
            yield response.follow(response.urljoin(job.get()),callback = self.parse_jd)
    
        next_page = response.xpath("(//a[@rel='next']/@href)[2]").get()

        if next_page:
            yield response.follow(response.urljoin(next_page),callback=self.parse)

    def parse_jd(self,response):

        title = response.xpath("//h1/text()").get()
        jd = response.xpath("//div[@class='well well-sm']/p/text()").get()
        table = response.xpath("//table[@class='table table-striped table-sm mb-3']/tr")
        date_posted = table.xpath(".//th[text()='Date Posted:']/../td/text()").get().strip()
        remote_work = table.xpath(".//th[text()='Remote Work Level:']/../td/text()").get().strip()
        location = table.xpath(".//th[text()='Location:']/../td/text()").get().strip()
        Job_Type = table.xpath(".//th[text()='Job Type:']/../td/text()").get().strip()
        Job_Schedule = table.xpath(".//th[text()='Date Posted:']/../td/text()").get().strip()
        Career_Level = table.xpath(".//th[text()='Career Level:']/../td/text()").get().strip()
        Travel_req = table.xpath(".//th[text()='Travel Required:']/../td/text()").get().strip()
        Cat = table.xpath(".//th[text()='Categories:']/../td/a/text()").getall()

        yield{
            'Title' : title,
            'Job_Desc' : jd,
            'Date_Posted' : date_posted,
            'Remote Work Level' : remote_work,
            'Location' : location,
            'Job Type' : Job_Type,
            'Job Schedule' : Job_Schedule,
            'Career Level' : Career_Level,
            'Travel Required' : Travel_req,
            # 'Salary & Benefits' : S_and_ben,
            # 'Other Benefits' : Other_Ben,
            'Categories' : Cat,
            'User-Agent' : response.request.headers['User-Agent'].decode('utf-8')

        }