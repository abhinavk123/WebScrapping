import scrapy


class PopulationSpider(scrapy.Spider):
    name = 'population'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        #title = response.xpath("//h1/text()").get()
        countries = response.xpath("//td/a")
        
        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()
        
            #absolute_url = response.urljoin(link)
            #yield scrapy.Request(absolute_url)

            yield response.follow(link,self.parse_country,meta = {'country_name' : name})

            '''yield {
                #'title' : title,
                'country_name' : name,
                'country_url'   : title
            }'''
    
    def parse_country(self,response):
        country = response.request.meta['country_name']
        rows = response.xpath('//table[@class="table table-striped table-bordered table-hover table-condensed table-list"]/tbody/tr')
        for row in rows:
            year = row.xpath('.//td/text()').get()
            population = row.xpath('.//td[2]/strong/text()').get()
            yearly_per_change = row.xpath('.//td[3]/text()').get()
            yearly_change = row.xpath('.//td[4]/text()').get()
            migrants_net = row.xpath('.//td[5]/text()').get()
            median_age = row.xpath('.//td[6]/text()').get()
            fertility_rate = row.xpath('.//td[7]/text()').get()
            density = row.xpath('.//td[8]/text()').get()
            urban_pop = row.xpath('.//td[9]/text()').get()
            urban_population = row.xpath('.//td[10]/text()').get()
            ctry_shr_of_wld_pop = row.xpath('.//td[11]/text()').get()
            world_pop = row.xpath('.//td[12]/text()').get()
            yield {
                'Country' : country,
                'Year' : year,
                'Population' : population,
                'Yearly % Change' : yearly_per_change,
                'Yearly Change' : yearly_change,
                'Migrants (net)' : migrants_net,
                'Median Age' : median_age,
                'Fertility Rate' : fertility_rate,
                'Density (P/Km²)' : density,
                'Urban Pop %' : urban_pop,
                'Urban Population' : urban_population,
                "Country's Share of World Pop" : ctry_shr_of_wld_pop,
                'World Population' : world_pop
            }

