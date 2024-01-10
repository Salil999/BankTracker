import requests
from fake_useragent import UserAgent
from institutions.base_scraper import Scraper, ExtractedResult

class ChaseScraper(Scraper):

    NAME = 'chase'
    URL = 'https://www.chase.com/bin/services/savingsRate'

    def __init__(self):
        super().__init__(ChaseScraper.NAME, ChaseScraper.URL)

    def extract(self) -> ExtractedResult:
        ua = UserAgent()
        try:
            rates = requests.post(
                self.url,
                headers = {'User-Agent': ua.random},
                data = {
                    'zipcode' : 10017,
                    'chartType' : 111
                },
                timeout=30).json()
        except requests.exceptions.Timeout:
            return []

        raw_rate = rates['ratesData'][0]['relationRate']
        raw_rate = raw_rate.strip('%')
        percentage = float(raw_rate)

        return [ExtractedResult(rate = percentage, type = 'savings')]
