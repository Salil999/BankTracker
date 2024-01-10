import requests
from fake_useragent import UserAgent
from institutions.base_scraper import Scraper, ExtractedResult

class PenFedScraper(Scraper):

    NAME = 'penfed'
    URL = 'https://www.penfed.org/content/penfed/public/services/getallrates.json'

    def __init__(self):
        super().__init__(PenFedScraper.NAME, PenFedScraper.URL)

    def extract(self) -> float:
        ua = UserAgent()
        try:
            rates = requests.get(self.url, headers = {'User-Agent': ua.random}, timeout = 10).json()
        except requests.exceptions.Timeout:
            return []
        # getting these keys based off of https://www.penfed.org/savings
        keys = set([
            'Premium Online Savings APY', # savings
            'MM Cert Mo15 APY', # money market
        ])
        rates = []
        for d in rates:
            key = d['name']
            rate = float(d['rate'])
            if key in keys:
                rates.append(ExtractedResult(rate = rate, type = key))
        return rates
