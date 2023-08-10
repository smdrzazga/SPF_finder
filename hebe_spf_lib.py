import spf_lib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

class HebeProduct:
    price_footer = spf_lib.PageElement(class_name="price-omnibus-text.price-omnibus-text--tile")
    price_norm = spf_lib.PageElement(class_name="price-omnibus-text__value.price-omnibus-text__value--regular")
    price_lowest = spf_lib.PageElement(class_name= "price-omnibus-text__value")
    
    price1 = spf_lib.PageElement(class_name="price-tile__amount")
    price2 = spf_lib.PageElement(class_name="price-tile__currency")
    name = spf_lib.PageElement(class_name="product-tile__name")
    description = spf_lib.PageElement(class_name= "product-tile__description ")
    link = spf_lib.PageElement(class_name="product-tile__clickable.js-product-link")

    product_unavailable = spf_lib.PageElement(class_name="product-tile.js-product-tile.product-tile--non-available")


    def __init__(self, product) -> None:
        # read key properties of on-sale items
        self.product = product
        self.price1 = product.find_element(self.price1.locator, self.price1.name).text
        self.price2 = product.find_element(self.price2.locator, self.price2.name).text.split("\n")
        self.name = product.find_element(self.name.locator, self.name.name).text
        self.description = product.find_element(self.description.locator, self.description.name).text
        self.link = product.find_element(self.link.locator, self.link.name).get_attribute("href")

        # availability check
        try:
            product.find_element(self.product_unavailable.locator, self.product_unavailable.name)
            self.is_available = False
        except:
            self.is_available = True


        # sale check
        try:
            self.price_regular = product.find_element(self.price_norm.locator, self.price_norm.name).text
            self.price_lowest = product.find_element(self.price_lowest.locator, self.price_lowest.name).text
            self.is_on_sale = True
        except:
            self.is_on_sale = False


    def __repr__(self) -> str:
        try:
            # if on sale - print also sale-referring prices
            return f"{self.price1}.{self.price2[0]}{self.price2[1]} ({self.price_regular} / {self.price_lowest} ) \n{self.name}, {self.description} \n{self.link}\n"
        except:
            # if not on sale - print only bare minimum
            return f"{self.price1}.{self.price2[0]}{self.price2[1]} \n{self.name}, {self.description} \n{self.link}\n"
 
    


class HebeWebScraper(spf_lib.WebScraper):
    def __init__(self, URL):
        super().__init__(URL)
        self.search_bar = spf_lib.PageElement(name=f"q")
        self.search_button = spf_lib.PageElement(xpath='//*[@id="wrapper"]/div[1]/div[1]/div[1]/div/div[6]/div[2]/div/div/div[2]/a')
        self.next_page_button = spf_lib.PageElement(class_name="bucket-pagination__icon.bucket-pagination__icon--next")
        self.pop_up_dismiss = spf_lib.PageElement(id="close-button-1454703513202")
        
        self.all_item_list = spf_lib.PageElement(class_name="product-grid__item ")
        
        # self.price_footer = 
    

    def num_pages(self):
        page = spf_lib.PageElement(class_name="bucket-pagination__link ")
        num_pages = self.driver.find_elements(page.locator, page.name)

        return int(num_pages[-1].text)

    def scrape(self, item: str, item_type: str):
        self.open_website()

        # print header of matching item list
        print(f"\n\n{self.driver.title}\n")

        # check for special offer - need to close the pop-up window
        # time.sleep(5)
        # try:
        #     self.click(self.pop_up_dismiss)
        # except:
        #     pass 

        # use search bar to search for phrase defined in "item"
        self.search(item)
        time.sleep(2)

        # search all pages
        for i in range(self.num_pages()): 
            # open page and scroll to the bottom of the page to load all items and "Next Page" button
            self.open_website()
            self.scroll(1, end=True)

            # read all item list
            products = self.find_all(self.all_item_list)
            time.sleep(1)

            # iterate over list of products
            for product in products:
                spf = HebeProduct(product)

                if not spf.is_on_sale or not spf.is_available:
                    continue

                # print only items containing "SPF50" phrase
                if item_type in spf.description:
                    print(spf)
            
            time.sleep(3)
            # proceed to the next page
            self.hover_and_click(self.next_page_button)