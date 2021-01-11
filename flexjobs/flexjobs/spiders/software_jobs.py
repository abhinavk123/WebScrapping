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
        date_posted = response.xpath("//table[@class='table table-striped table-sm mb-3']/tr/td/text()")[0].get().strip()
        remote_work = response.xpath("//table[@class='table table-striped table-sm mb-3']/tr/td/text()")[1].get().strip()
        location = response.xpath("//table[@class='table table-striped table-sm mb-3']/tr/td/text()")[2].get().strip()
        Job_Type = response.xpath("//table[@class='table table-striped table-sm mb-3']/tr/td/text()")[3].get().strip()
        Job_Schedule = response.xpath("//table[@class='table table-striped table-sm mb-3']/tr/td/text()")[4].get().strip()
        Career_Level = response.xpath("//table[@class='table table-striped table-sm mb-3']/tr/td/text()")[5].get().strip()
        Travel_req = response.xpath("//table[@class='table table-striped table-sm mb-3']/tr/td/text()")[6].get().strip()
        S_and_ben = response.xpath("//table[@class='table table-striped table-sm mb-3']/tr/td/text()")[7].get().strip()
        Other_Ben = response.xpath("//table[@class='table table-striped table-sm mb-3']/tr/td/text()")[8].get().strip()
        Cat = response.xpath("//table[@class='table table-striped table-sm mb-3']/tr/td/text()")[9].get().strip()

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
            'Salary & Benefits' : S_and_ben,
            'Other Benefits' : Other_Ben,
            'Categories' : Cat,
            'User-Agent' : response.request.headers['User-Agent'].decode('utf-8')

        }