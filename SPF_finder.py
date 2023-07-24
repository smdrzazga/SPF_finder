from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

# desired item to look for:
item = "spf"

# disable pop-ups
option = Options()
option.add_argument('--disable-notifications')

# use chrome driver
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(options= option)

# load website
url = "https://www.hebe.pl"
driver.get(url)

# define action chain to click "Next Page" button
actions = ActionChains(driver)

# key element labels to find on each page
search_bar_xpath = f'//*[@id="q"]'
search_button_xpath = '//*[@id="wrapper"]/div[1]/div[1]/div[1]/div/div[6]/div[2]/div/div/div[2]/a'
next_page_button_class = "a.button.button--outline.button--icon "

# use search bar to search for phrase defined in "item"
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, search_bar_xpath)))
search_bar = driver.find_element(By.XPATH, search_bar_xpath)
search_bar.clear()
search_bar.send_keys(item)

# manually wait a long time until button would be clickable (WebDriverWait does not work)
# WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, search_button_xpath)))
time.sleep(1)
button = driver.find_element(By.XPATH, search_button_xpath)
time.sleep(2)
button.click()
time.sleep(0.5)

# print header of matching item list
print(driver.title)
print("PRICE\tREG\tLOW\tITEM\t\tDESCRIPTION\t\tLINK")

# search first 10 pages
for i in range(10): 
    # scroll to the bottom of the page to load all items and "Next Page" button
    html = driver.find_element(By.TAG_NAME, 'html')
    html.send_keys(Keys.END)
    html.send_keys(Keys.PAGE_UP)

    # read all item list
    product_class = "product-grid__item "
    products = driver.find_elements(By.CLASS_NAME, product_class)
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
    
    # proceed to the next page
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, next_page_button_xpath)))
    next_page = driver.find_element(By.XPATH, '//a[contains(., "Następna strona")]')
    time.sleep(0.5)
    actions.move_to_element(next_page)
    time.sleep(4)
    actions.click()
    actions.perform()
    time.sleep(5)


time.sleep(30)
driver.quit()


# TODO
# more websites
# use classes


# Dependencies:
# selenium
# chromedriver added to PATH environmental variables
