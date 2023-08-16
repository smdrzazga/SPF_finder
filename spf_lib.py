from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time


class Notifications:
    def options(self):
        chrome_options = Options()
        chrome_options.add_argument('--disable-notifications')
        # chrome_options.add_argument("--ignore-certificate-errors")
        # chrome_options.add_argument("--disable-popup-blocking")
        # chrome_options.add_argument("diable-lazy-loading")
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        return chrome_options
 

class PageElement():
    def __init__(self, xpath="", class_name="", id="", name="", css_selector="") -> None:
        if xpath != "":
            self.locator = "xpath"
            self.name = xpath

        elif class_name != "":
            self.locator = "class name"
            self.name = class_name

        elif id != "":
            self.locator = "id"
            self.name = id

        elif name != "":
            self.locator = "name"
            self.name = name

        elif css_selector != "":
            self.locator = "css selector"
            self.name = css_selector


class WebScraper:
    def __init__(self, URL):
        self.website = URL
        self.driver = webdriver.Chrome(options = Notifications().options())

    legend = """
PRICE \t|  REG \t|  LOW \t|
-------------------------
ITEM \t|  DESCRIPTION \t|  
-------------------------
LINK \t|\n
      """
    

    def open_website(self):
        self.driver.get(self.website)


    def find_single(self, element: PageElement):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((element.locator, element.name)))
        
        return self.driver.find_element(element.locator, element.name)


    def find_all(self, element: PageElement):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((element.locator, element.name)))
        
        return self.driver.find_elements(element.locator, element.name)


    def find_clickable(self, element: PageElement):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((element.locator, element.name)))
      
        return self.driver.find_element(element.locator, element.name)


    def click(self, element: PageElement) -> None:
        # wait for button to be clickable and click
        # button = self.find_clickable(element)

        button = self.find_single(element)

        time.sleep(0.5)
        button.click()


    def search(self, item):
        search_bar = self.find_single(self.search_bar)
        search_bar.clear()
        search_bar.send_keys(item)
        time.sleep(1)
        search_bar.send_keys(Keys.ENTER)


    def scroll(self, amount, end=False):
        html = self.driver.find_element(By.TAG_NAME, 'html')
        if end:
            html.send_keys(Keys.END)
            for i in range(amount):
                html.send_keys(Keys.PAGE_UP)
        
        else:
            for i in range(amount):
                html.send_keys(Keys.PAGE_DOWN)



    def hover_and_click(self, element: PageElement):
        actions = ActionChains(self.driver)

        try:
            button = self.find_single(element)
        except:
            print("no button")

        actions.move_to_element(button)
        actions.click()
        actions.perform()
        time.sleep(2)
    

    def quit(self):
        self.driver.quit()

    


