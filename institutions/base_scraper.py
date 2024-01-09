import logging
from fake_useragent import UserAgent
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class Scraper(ABC):
    @abstractmethod
    def __init__(self, name: str, url: str):
        logging.info(f'Registering scraper {name} with URL: {url}')
        self.url = url
    
    @abstractmethod
    def extract(self) -> float:
        """
        Extract and return a float which specifies the current percentage / APY
        interest rate. Ensure the number is within range of 0.0 - 100.0
        
        Returns:
            float: The interest / APY rate within the range of 0.0 - 100.0
        """
        pass

    def get_name(self):
        """
        Get the name of the scraper.

        :return: The name of the scraper.
        """
        return self.name

    def get_url(self):
        """
        Get the URL of the scraper.

        :return: The URL of the scraper.
        """
        return self.url
