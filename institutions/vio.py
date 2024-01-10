import requests
from fake_useragent import UserAgent
from institutions.base_scraper import Scraper, ExtractedResult
from bs4 import BeautifulSoup

class VioBankScraper(Scraper):

    NAME = 'vio'
    URL = 'https://www.viobank.com/cornerstone-money-market-savings'

    def __init__(self):
        super().__init__(VioBankScraper.NAME, VioBankScraper.URL)

    def extract(self) -> ExtractedResult:
        ua = UserAgent()
        html_content = requests.get(self.url,headers={'User-Agent': ua.random}).text
        soup = BeautifulSoup(html_content, 'html.parser')
        rates = soup.find_all("span", class_="featured-product--rate")
        return [] # broken for now
