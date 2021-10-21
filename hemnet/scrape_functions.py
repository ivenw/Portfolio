from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import sys
import pickle

def pull_page(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = Chrome(ChromeDriverManager().install(), options=chrome_options)

    driver.get(url)
    soup = bs(driver.page_source)

    driver.close()
    return soup


def hemnet_pull_all(url):
    # first get how many pages there are
    soup = pull_page(url)
    key = "div.pagination__item"
    pages_num = int(soup.select(key)[-2].text)
    soup_list = [soup]

    for page in range(2, pages_num+1):
        soup = pull_page(f"{url}&page={page}")
        soup_list.append(soup)

    return soup_list


def flatten(t):
    return [item for sublist in t for item in sublist]


def container_list_gen(container_key, soup_list):
    container_list = [soup.select(container_key) for soup in soup_list]
    container_list = flatten(container_list)
    container_list = [i for i in container_list if i != "\n"]

    return container_list


def container_scrape(container_list, column_keys):
    pd_dct = {i: [] for i in column_keys}

    for container in container_list:
        for cat, key in column_keys.items():
            try:
                pd_dct[cat].append(container.select(key)[0].text)
            except:
                pd_dct[cat].append(np.nan)

    return pd.DataFrame(pd_dct)


def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


def load_object(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)