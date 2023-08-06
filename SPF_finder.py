from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

import spf_lib as sz

# define item to look for and website:
item = "spf"
website = "https://www.hebe.pl"
# website = "https://www.hebe.pl/search?lang=pl_PL&q=spf"

# use chrome driver, assume chromedriver added to environmental variable PATH
scraper = sz.HebeWebScraper(website)
scraper.open_website()

# print header of matching item list
print(f"\n\n{scraper.driver.title}\n")
print(scraper)

# now they have special offer so need to close the pop-up window
time.sleep(5)
scraper.click(scraper.pop_up_dismiss)

# use search bar to search for phrase defined in "item"
scraper.search(item)
time.sleep(2)
scraper.click(scraper.search_button)

# scraper.driver.get_screenshot_as_file("screenshot.png")


# search first 10 pages
for i in range(10): 
    # scroll to the bottom of the page to load all items and "Next Page" button
    scraper.scroll(1, end=True)

    # read all item list
    product_class = "product-grid__item "
    products = scraper.driver.find_elements(By.CLASS_NAME, product_class)
    time.sleep(1)

    # iterate over list of products
    for product in products:
        # check whether it is on sale
        try:
            price_footer = product.find_element(By.CLASS_NAME, "price-omnibus-text.price-omnibus-text--tile")
            price_regular = product.find_element(By.CLASS_NAME, "price-omnibus-text__value.price-omnibus-text__value--regular").text
            price_lowest = product.find_element(By.CLASS_NAME, "price-omnibus-text__value").text
        except:
            continue

        # read key properties of on-sale items
        price1 = product.find_element(By.CLASS_NAME, "price-tile__amount").text
        price2 = product.find_element(By.CLASS_NAME, "price-tile__currency").text.split("\n")
        name = product.find_element(By.CLASS_NAME, "product-tile__name").text
        description = product.find_element(By.CLASS_NAME, "product-tile__description ").text
        link = product.find_element(By.CLASS_NAME, "product-tile__clickable.js-product-link").get_attribute("href")

        # print only items containing "SPF50" phrase
        if "SPF50" in description:
            print(f"{price1}.{price2[0]}{price2[1]} ({price_regular} / {price_lowest} ) ")
            print(f"{name}, {description}")
            print(f"{link}\n")
    
    time.sleep(3)
    # proceed to the next page
    scraper.hover_and_click(scraper.next_page_button)


time.sleep(30)
scraper.quit()


# TODO
# more websites
# use classes


# Dependencies:
# selenium
# chromedriver added to PATH environmental variables
