import spf_lib
from selenium.webdriver.common.action_chains import ActionChains

import time

class DouglasPageComponents:
    search_bar = spf_lib.PageElement(id=f"typeAhead-input")
    next_page_button = spf_lib.PageElement(class_name="link.link--text.pagination__arrow.active")
    pop_up_dismiss = spf_lib.PageElement(class_name="uc-banner-title__decline-all-link")
    all_item_list = spf_lib.PageElement(class_name="product-grid-column.col-sm-6.col-md-4.col-lg-3")
    page_bucket = spf_lib.PageElement(class_name="pagination")
    goto_pages = spf_lib.PageElement(class_name="pagination-title.pagination-title--with-dropdown")


class DouglasProductComponents:
    price_footer = spf_lib.PageElement(class_name="price-row")
    promotion_label = spf_lib.PageElement(class_name="product-price__lowest.product-price__lowest.product-price__lowest--black")
    price = spf_lib.PageElement(class_name="product-price__price")
    price_norm = spf_lib.PageElement(class_name="product-price__price")
    price_lowest = spf_lib.PageElement(class_name="product-price__price")

    brand = spf_lib.PageElement(class_name="text.top-brand")
    category = spf_lib.PageElement(class_name="text.category")
    name = spf_lib.PageElement(class_name="text.name")

    link = spf_lib.PageElement(class_name="link.link--no-decoration.product-tile__main-link")



class DouglasProduct:
    def __init__(self, product) -> None:
        # availability check
        self.is_available = True

        # sale check
        try:
            product.find_element(DouglasProductComponents.promotion_label.locator, DouglasProductComponents.promotion_label.name)
            self.is_on_sale = True
        except:
            self.is_on_sale = False

        # get price values
        self.product = product
        prices = product.find_elements(DouglasProductComponents.price_norm.locator, DouglasProductComponents.price_norm.name)
        if len(prices) == 3:
            self.price_regular = prices[0].text
            self.price = prices[1].text
            self.price_lowest = prices[2].text
        else:
            self.is_on_sale = False

        # read key properties of on-sale items
        try:
            self.brand = product.find_element(DouglasProductComponents.brand.locator, DouglasProductComponents.brand.name).text
            self.category = product.find_element(DouglasProductComponents.category.locator, DouglasProductComponents.category.name).text
            self.name = product.find_element(DouglasProductComponents.name.locator, DouglasProductComponents.name.name).text
            self.link = product.find_element(DouglasProductComponents.link.locator, DouglasProductComponents.link.name).get_attribute("href")
        except:
            pass


    def __repr__(self) -> str:
        try:
            # if on sale - print also sale-referring prices
            text = ""
            if self.price > self.price_lowest:
                text += "Is it really on sale...?\n"
            return text + f"{self.price} ({self.price_regular} / {self.price_lowest} ) \n{self.brand}, {self.category} \n{self.name}, \n{self.link}\n"
        except:
            # if not on sale - print only bare minimum
            return f"{self.price} \n{self.name}, \n{self.link}\n"
 
    
class DouglasWebScraper(spf_lib.WebScraper):
    def __init__(self, URL):
        super().__init__(URL)
        self.search_bar = DouglasPageComponents.search_bar
        self.next_page_button = DouglasPageComponents.next_page_button
        self.all_item_list = DouglasPageComponents.all_item_list

    

    def num_pages(self):
        num_pages = self.driver.find_element(DouglasPageComponents.goto_pages.locator, DouglasPageComponents.goto_pages.name).text
        last_page_num = num_pages.split()[-1]

        return int(last_page_num)


    def goto_next_page(self):
        page_bucket = self.driver.find_element(DouglasPageComponents.page_bucket.locator, DouglasPageComponents.page_bucket.name)
        buttons = page_bucket.find_elements(DouglasPageComponents.next_page_button.locator, DouglasPageComponents.next_page_button.name)
        next = buttons[-1]
        actions = ActionChains(self.driver)
        actions.move_to_element(next).click().perform()


    def scrape(self, item: str, item_type: str):

        # print header of matching item list
        self.open_website()
        print(f"\n\nDOUGLAS \n{self.driver.title}\n")

        # use search bar to search for phrase defined in "item"
        time.sleep(3)
        self.click(DouglasPageComponents.pop_up_dismiss)
        time.sleep(1)
        self.hover_and_click(self.search_bar)
        time.sleep(1)
        self.search(item)
        time.sleep(2) 


        # search all pages except the last one (usually garbage offers, not available products, etc.)
        for i in range(1, self.num_pages()): 
            # open page and scroll to the bottom of the page to load all items and "Next Page" button
            print(f"Page: {i}")            
            self.scroll(2, end=True)
            
            # read all item list
            time.sleep(0.5)
            products = self.find_all(self.all_item_list)

            # iterate over list of products
            for product in products:
                spf = DouglasProduct(product)

                if not spf.is_on_sale or not spf.is_available:
                    continue

                # print only items containing "SPF50" phrase
                for type in item_type:
                    if type in spf.name:
                        print(spf)
            
            time.sleep(3)
            # proceed to the next page
            self.goto_next_page()    
