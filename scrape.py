from splinter import Browser, Config

my_config = Config(headless = False)

with Browser('chrome', config = my_config) as browser:
    browser.visit('https://www.google.com/')
    print(browser.title)