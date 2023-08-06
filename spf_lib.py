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
        chrome_options.add_argument("--headless")
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

    
    def __repr__(self) -> str:
        return """
PRICE \t|  REG \t|  LOW \t|
-------------------------
ITEM \t|  DESCRIPTION \t|  
-------------------------
LINK \t|\n
      """

    def open_website(self):
        self.driver.get(self.website)


    def find(self, element: PageElement):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((element.locator, element.name)))
        
        return self.driver.find_element(element.locator, element.name)


    def find_clickable(self, element: PageElement):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((element.locator, element.name)))
      
        return self.driver.find_element(element.locator, element.name)


    def click(self, element: PageElement) -> None:
        # wait for button to be clickable and click
        # button = self.find_clickable(element)

        button = self.find(element)

        time.sleep(0.5)
        button.click()


    def search(self, item):
        search_bar = self.find(self.search_bar)
        search_bar.clear()
        search_bar.send_keys(item)


    def scroll(self, amount, end=False):
        html = self.driver.find_element(By.TAG_NAME, 'html')
        if end:
            html.send_keys(Keys.END)
            for i in range(amount):
                html.send_keys(Keys.PAGE_UP)
        
        else:
            for i in range(amount):
                html.send_keys(Keys.PAGE_UP)



    def hover_and_click(self, element: PageElement):
        actions = ActionChains(self.driver)

        try:
            button = self.find(element)
            # button = self.driver.find_element(By.CLASS_NAME, element.name)
        except:
            print("no button")
        actions.move_to_element(button)
        actions.click()
        actions.perform()
        time.sleep(4)
    

    def quit(self):
        self.driver.quit()



class HebeWebScraper(WebScraper):
    def __init__(self, URL):
        super().__init__(URL)
        self.search_bar = PageElement(name=f"q")
        self.search_button = PageElement(xpath='//*[@id="wrapper"]/div[1]/div[1]/div[1]/div/div[6]/div[2]/div/div/div[2]/a')
        self.next_page_button = PageElement(class_name="bucket-pagination__icon.bucket-pagination__icon--next")
        self.pop_up_dismiss = PageElement(id="close-button-1454703513202")
    