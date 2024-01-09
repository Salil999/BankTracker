import requests
from fake_useragent import UserAgent
from institutions.base_scraper import Scraper
from bs4 import BeautifulSoup

class PenFedScraper(Scraper):

    NAME = 'penfed'
    URL = 'https://www.penfed.org/content/penfed/public/services/getallrates.json'

    def __init__(self):
        super().__init__(PenFedScraper.NAME, PenFedScraper.URL)

    def extract(self) -> float:
        ua = UserAgent()
        try:
            rates = requests.get(self.url, headers = {'User-Agent': ua.random}, timeout=5).json()
        except requests.exceptions.Timeout:
            return -1
        savings_rate_key = 'Premium Online Savings APY'
        for d in rates:
            key = d['name']
            if key == savings_rate_key:
                return float(d['rate'])
        return -1
