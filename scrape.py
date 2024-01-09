import logging
import pathlib
import importlib
import datetime
import hashlib
import csv
import os
from institutions.base_scraper import Scraper
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOTAL_HOURS = 24
MAX_MD5_HASH_VALUE = pow(2, 128)

def get_scrapers() -> List[Scraper]:
    scrapers = []
    for file in pathlib.Path('./institutions').glob('*.py'):
        mod = importlib.import_module(f'institutions.{file.stem}')
        for klass in mod.__dict__.values():
            if isinstance(klass, type) and issubclass(klass, Scraper) and klass.__name__ != 'Scraper':
                scrapers.append(klass)
    return scrapers

# Attempts to evenly distribute scrapers across 24 hours
# We can lower the granularity from hours to minutes if too many scrapers are running in a single hour
def is_allowed(scraper: Scraper):
    md5_hash = hashlib.md5(scraper.NAME.encode('utf-8'))
    hashed_integer = int(md5_hash.hexdigest(), 16)
    marker = hashed_integer / MAX_MD5_HASH_VALUE

    now = datetime.datetime.now()
    hour = now.hour # range is from 0 to 23

    logger.info(f'Left Bound {hour / TOTAL_HOURS}, Marker {marker}, Right Bound {(hour + 1) / TOTAL_HOURS})')

    return (hour / TOTAL_HOURS) < marker <= ((hour + 1) / TOTAL_HOURS)

def is_new_file(file_name: str):
    os.path.getsize(file_name) == 0

if __name__ == '__main__':
    rates = []
    for klass in get_scrapers():
        scraper = klass()
        # if not is_allowed(scraper):
        #     logger.info(f'Skipping scraper for {scraper.NAME}')
        #     continue
        # else:
        #     logger.info(f'Running scraper for {scraper.NAME}')

        rate = scraper.extract()
        logger.info(f'Rate: {rate}')
        if rate >= 0:
            rates.append({
                'date': datetime.datetime.now().isoformat(timespec='milliseconds'),
                'rate': rate,
                'name': scraper.NAME,
            })

    os.makedirs('rates', exist_ok=True)

    logger.info(f'Writing rates to {len(rates)} files')

    for rate in rates:
        file_name = f'rates/{rate["name"]}.csv'
        if is_new_file(file_name):
            logger.info(f'New file: {file_name}')
            with open(file=file_name, mode='a+', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['date', 'rate', 'name'])
                if f.tell() == 0:
                    logger.info(f'New file: {file_name}')
                    writer.writeheader()
                    writer.writerow(rate)
        else:
            logger.info(f'Existing file: {file_name}')
            with open(file=file_name, mode='r', newline='') as f:
                reader = csv.DictReader(f, fieldnames=['date', 'rate', 'name'])
                last_line = next(reader) # skip the header
                for line in reader:
                    last_line = line
                # only write a new entry if the rate has changed from the last known value
                if float(last_line['rate']) != rate['rate']:
                    logger.info(f'Updating file: {file_name}')
                    with open(file=file_name, mode='a+', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=['date', 'rate', 'name'])
                        writer.writerow(rate)
