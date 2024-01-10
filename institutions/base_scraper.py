import logging
from abc import ABC, abstractmethod
from collections import namedtuple
from typing import List

logger = logging.getLogger(__name__)

ExtractedResult = namedtuple('ExtractedResult', 'rate type')

class Scraper(ABC):
    @abstractmethod
    def __init__(self, name: str, url: str):
        logging.info(f'Registering scraper {name} with URL: {url}')
        self.url = url

    @abstractmethod
    def extract(self) -> List[ExtractedResult]:
        """
        Extract and return a float which specifies the current percentage / APY
        interest rate. Ensure the number is within range of 0.0 - 100.0
        
        Returns:
            float: The interest / APY rate within the range of 0.0 - 100.0
        """
        pass
