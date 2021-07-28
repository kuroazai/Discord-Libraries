# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 18:05:50 2021

@author: KuroAzai
"""

from bs4 import BeautifulSoup
import urllib3
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# settings dw about this
urllib3.disable_warnings()
http = urllib3.PoolManager()


def parser(term):
    # rng from 1 - 20
    url = 'https://www.urbandictionary.com/define.php?term=' + term
    print(url)
    # options g
    options = Options()
    # Run Driver in headerless mode
    options.headless = True
    # Set the driver with its options
    browser = webdriver.Firefox(options=options)
    # Get the results from our headless browser for our objects page
    browser.get(url)
    driver = browser
    soup = BeautifulSoup(driver.page_source, "html.parser")

    pages = soup.find_all("div", class_="meaning")
    '''
    for x in pages:
        print(x.text)
    '''
    driver.quit()
    return pages[0].text
