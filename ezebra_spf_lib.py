import spf_lib
from selenium.webdriver.common.action_chains import ActionChains

import time

class EzebraPageComponents:
    search_bar = spf_lib.PageElement(id=f"menu_search_text")
    next_page_button = spf_lib.PageElement(class_name="pagination__element.--next.--button.d-md-flex.d-none")
    pop_up_dismiss = spf_lib.PageElement(class_name="secondary.popover-button")
    all_item_list = spf_lib.PageElement(class_name="product.col-6.col-sm-4.pt-3.pb-md-3")
    page_bucket = spf_lib.PageElement(class_name="s_paging__item.pagination.mb-2.mb-sm-3")
    goto_pages = spf_lib.PageElement(class_name='pagination__element.--item')


class EzebraProductComponents:
    price_footer = spf_lib.PageElement(class_name="price-row")
    promotion_label = spf_lib.PageElement(class_name="product__yousavepercent")
    availability_label = spf_lib.PageElement(class_name="product__hover-effect")
    price = spf_lib.PageElement(class_name="price.--max-exists")
    price_norm = spf_lib.PageElement(class_name="price.--max")
    price_lowest = spf_lib.PageElement(class_name="omnibus_price__value")

    name = spf_lib.PageElement(class_name="product__name")

    link = spf_lib.PageElement(class_name="product__name")



class EzebraProduct:
    def __init__(self, product) -> None:
        # availability check
        try:
            self.is_available = True
            label = product.find_element(EzebraProductComponents.availability_label.locator, EzebraProductComponents.availability_label.name)
            if label.text == "Produkt niedostępny":
                self.is_available = False
        except:
            self.is_available = True
            
        # sale check
        try:
            product.find_element(EzebraProductComponents.promotion_label.locator, EzebraProductComponents.promotion_label.name)
            self.is_on_sale = True
        except:
            self.is_on_sale = False

        # get price values
        try:
            self.product = product
            self.price = product.find_element(EzebraProductComponents.price.locator, EzebraProductComponents.price.name).text
            self.price_regular = product.find_element(EzebraProductComponents.price_norm.locator, EzebraProductComponents.price_norm.name).text
            self.price_lowest = product.find_element(EzebraProductComponents.price_lowest.locator, EzebraProductComponents.price_lowest.name).text
        except:
            pass

        # read key properties of on-sale items
        try:
            self.name = product.find_element(EzebraProductComponents.name.locator, EzebraProductComponents.name.name).text
            self.link = product.find_element(EzebraProductComponents.link.locator, EzebraProductComponents.link.name).get_attribute("href")
        except:
            pass


    def __repr__(self) -> str:
        try:
            # if on sale - print also sale-referring prices
            text = ""
            if self.price > self.price_lowest:
                text += "Is it really on sale...?\n"
            return text + f"{self.price} ({self.price_regular} / {self.price_lowest} ) \n{self.name}, \n{self.link}\n"
        except:
            # if not on sale - print only bare minimum
            return f"{self.price} \n{self.name}, \n{self.link}\n"
 
    
class EzebraWebScraper(spf_lib.WebScraper):
    def __init__(self, URL):
        super().__init__(URL)
        self.search_bar = EzebraPageComponents.search_bar
        self.next_page_button = EzebraPageComponents.next_page_button
        self.all_item_list = EzebraPageComponents.all_item_list

    

    def num_pages(self):
        pagination_elements = self.driver.find_elements(EzebraPageComponents.goto_pages.locator, EzebraPageComponents.goto_pages.name)
        last_page_num = pagination_elements[-1].text

        return int(last_page_num)


    def goto_next_page(self):
        page_bucket = self.driver.find_element(EzebraPageComponents.page_bucket.locator, EzebraPageComponents.page_bucket.name)
        buttons = page_bucket.find_elements(EzebraPageComponents.next_page_button.locator, EzebraPageComponents.next_page_button.name)
        next = buttons[-1]
        actions = ActionChains(self.driver)
        actions.move_to_element(next).click().perform()


    def scrape(self, item: str, item_type: str):

        # print header of matching item list
        self.open_website()
        print(f"\n\nEzebra \n{self.driver.title}\n")

        # use search bar to search for phrase defined in "item"
        time.sleep(1)
        self.hover_and_click(self.search_bar)
        time.sleep(1)
        self.search(item)
 
        self.scroll(2, end=True)
        time.sleep(2)
        self.click(EzebraPageComponents.pop_up_dismiss)

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
                spf = EzebraProduct(product)

                if not spf.is_on_sale or not spf.is_available:
                    continue

                # print only items containing "SPF50" phrase
                for type in item_type:
                    if type in spf.name:
                        print(spf)
            
            time.sleep(3)
            # proceed to the next page
            # self.goto_next_page()    
            self.hover_and_click(self.next_page_button)
