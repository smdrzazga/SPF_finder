from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

import spf_lib as sz
import hebe_spf_lib as hebe

# define item to look for and website:
item = "spf"
model = "SPF50"
hebe_website = "https://www.hebe.pl"

# use chrome driver, assume chromedriver added to environmental variable PATH
scraper = hebe.HebeWebScraper(hebe_website)

# print header of matching item list
print(scraper)
scraper.scrape(item, model)


time.sleep(30)
scraper.quit()


# TODO
# more websites:
    # superpharm
    # pigment
    # rossman
    # cocolita
    # Douglas
    # ezebra (?)




# Dependencies:
# selenium
# chromedriver added to PATH environmental variables
