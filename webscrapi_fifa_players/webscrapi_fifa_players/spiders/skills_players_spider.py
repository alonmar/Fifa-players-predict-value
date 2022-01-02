import scrapy

# https://www.fifaindex.com/players/
# Info player: response.xpath('//td[@data-title="Name"]/a/@href').getall()
# Next Page: response.xpath('//*[contains(text(),"Next Page")]/@href').get()

#################################################

# nombre response.xpath('//h5[@class="card-header"]/text()').get()
# nation: response.xpath('//a[@class="link-nation"]/@title').get() 
# overallrating, potencial: response.xpath('//h5[@class="card-header"]//span[@class="float-right"]/span/text()').getall()

# ['Height ', 'Weight ', response.xpath('//*[contains(text(),"Height ")]//span[@class="data-units data-units-metric"]/text()').get()
# 'Preferred Foot ', 'Birth Date ', 'Age ', response.xpath('//*[contains(text(),"Preferred Foot ")]/span[@class="float-right"]/text()').get()
# 'Player Work Rate ', response.xpath('//*[contains(text(),"Preferred Foot ")]/span[@class="float-right"]/text()').get()
# 'Preferred Positions ', response.xpath('//*[contains(text(),"Preferred Positions ")]/span[@class="float-right"]/a/span/text()').getall()
# 'Weak Foot ', 'Skill Moves ', # nop
# 'Value ', 'Value ', 'Value ', 'Wage ', 'Wage ', 'Wage ', response.xpath('//*[contains(text(),"Wage ")]/span[@class="float-right"]/text()').get()  
# 'Position ', 'Kit Number ', 'Joined Club ', #nop
# 'Contract Length ', response.xpath('//*[contains(text(),"Contract Length ")]/span[@class="float-right"]/text()').get() 
# 'Position ', 'Kit Number ', #Nop
# 'Ball Control ', 'Dribbling ', 'Marking ', 'Slide Tackle ', 'Stand Tackle ', 
# 'Aggression ', 'Reactions ', 'Att. Position ', 'Interceptions ', 'Vision ', 'Composure ', 
# 'Crossing ', 'Short Pass ', 'Long Pass ', 'Acceleration ', 'Stamina ', 'Strength ', 'Balance ', 
# 'Sprint Speed ', 'Agility ', 'Jumping ', 'Heading ', 'Shot Power ', 'Finishing ', 'Long Shots ', 
# 'Curve ', 'FK Acc. ', 'Penalties ', 'Volleys ', 'GK Positioning ', 'GK Diving ', 'GK Handling ', 
# 'GK Kicking ', 'GK Reflexes '] response.xpath('//*[contains(text(),"skill ")]/span[@class="float-right"]/span/text()').get()  




class SkillsSpider(scrapy.Spider):
    name = 'skills'
    start_urls = [
        'https://www.fifaindex.com/players/'
    ]

    custom_settings = {
        'FEED_URI': 'data_fifa_players.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'ROBOTSTXT':True,
    }

    def parse_data_player(self, response, **kwargs):
        """Get data in url by player"""
        link = kwargs['url']
        name = response.xpath('//h5[@class="card-header"]/text()').get()
        nation = response.xpath('//a[@class="link-nation"]/@title').get() 
        overallrating, potencial = response.xpath('//h5[@class="card-header"]//span[@class="float-right"]/span/text()').getall()
        height = response.xpath('//*[contains(text(),"Height ")]//span[@class="data-units data-units-metric"]/text()').get()
        weight = response.xpath('//*[contains(text(),"Weight ")]//span[@class="data-units data-units-metric"]/text()').get()
        preferred_positions = response.xpath('//*[contains(text(),"Preferred Positions ")]/span[@class="float-right"]/a/span/text()').getall()

        # This data player have sabe xpath structure
        list1 = [
            'Preferred Foot ', 'Birth Date ', 'Age ', 'Player Work Rate ', 'Value ','Wage ', 'Contract Length '
            ]

        x = {}
        for i in list1:
            # removed last white space
            x[i.rstrip()] = response.xpath(f'//*[contains(text(),"{i}")]/span[@class="float-right"]/text()').get()

        # This data player have sabe xpath structure
        list2 = [
            'Ball Control ', 'Dribbling ', 'Marking ', 'Slide Tackle ', 'Stand Tackle ',
            'Aggression ', 'Reactions ', 'Att. Position ', 'Interceptions ', 'Vision ', 'Composure ', 
            'Crossing ', 'Short Pass ', 'Long Pass ', 'Acceleration ', 'Stamina ', 'Strength ', 'Balance ', 
            'Sprint Speed ', 'Agility ', 'Jumping ', 'Heading ', 'Shot Power ', 'Finishing ', 'Long Shots ', 
            'Curve ', 'FK Acc. ', 'Penalties ', 'Volleys ', 'GK Positioning ', 'GK Diving ', 'GK Handling ',
            'GK Kicking ', 'GK Reflexes '
        ]

        y = {}
        for i in list2:
            # removed last white space
            y[i.rstrip()] = response.xpath(f'//*[contains(text(),"{i}")]/span[@class="float-right"]/span/text()').get() 

        # join dicts 
        x.update(y)

        skills_data_players = {
            'url': link,
            'name': name,
            'nation': nation,
            'overallrating': overallrating,
            'potencial': potencial,
            'height': height,
            'weight': weight,
            'preferred_positions': preferred_positions,
        }
        skills_data_players.update(x)

        yield skills_data_players



    def parse(self, response):
        # visit every url for player
        info_players_links = response.xpath('//td[@data-title="Name"]/a/@href').getall()

        for link in info_players_links:
            yield response.follow(link, callback=self.parse_data_player, cb_kwargs={'url': response.urljoin(link)})

        # If next button exits go
        next_page_button_link = response.xpath('//*[contains(text(),"Next Page")]/@href').get()

        if next_page_button_link:#!= '/players/3/':
            yield response.follow(next_page_button_link, callback=self.parse)





