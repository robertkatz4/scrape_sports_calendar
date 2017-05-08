import scrapy
import datetime as dt
from scrapy.crawler import CrawlerProcess

class ScheduleSpider(scrapy.Spider):
    name = "premier_league"
    start_urls = [
        'https://www.theguardian.com/football/premierleague/fixtures',
    ]

    def parse(self, response):
        for match in response.css('#article > div > div > div.content__main-column > div.football-matches__container > div > div > div > table tr'):
            home = str(match.css('td.football-match__teams.table-column--main > a > div.football-match__team.football-match__team--home.football-team > div.football-team__name.team-name > span::text').extract())
            away = str(match.css('td.football-match__teams.table-column--main > a > div.football-match__team.football-match__team--away.football-team > div.football-team__name.team-name > span::text').extract())
            heading = away + " @ " + home
            time_diff = int(5)
            timedate = str(match.css('td.football-match__status.football-match__status--f.table-column--sub > time').xpath('@datetime').extract())
            if timedate == '[]':
                timedate = '...2017-08-01T15:00:00+0100'
            time_adj = str(int(float(timedate[14:16].strip())) - time_diff) + timedate[16:19]
            month_int = int(float(timedate[8:10].strip()))
            day_int = int(float(timedate[11:13].strip()))
            dt_var = dt.date(2017,month_int,day_int)
            dt_var = dt_var.strftime('%m/%d/%Y')
            watch_fc  = ["[u'Chelsea']","[u'Spurs']","[u'Liverpool']","[u'Man City']","[u'Arsenal']","[u'Man Utd']"]
            if home in watch_fc and away in watch_fc:
                yield {
                    'subject': heading,
                    'dt_var': dt_var,
                    'time': time_adj,
                    'home': home,
                    'away': away,
                }

if __name__ == "__main__":
        process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(ScheduleSpider)
    process.start()
