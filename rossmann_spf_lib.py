import spf_lib
from selenium.webdriver.common.action_chains import ActionChains

import time


class RossmannPageComponents:
    search_bar = spf_lib.PageElement(class_name=f"modal-search__input.form-control")
    search_button = spf_lib.PageElement(class_name=f"show-search__btn.btn")
    next_page_button = spf_lib.PageElement(class_name="btn ")
    pop_up_dismiss = spf_lib.PageElement(id="onetrust-close-btn-container")
    all_item_list = spf_lib.PageElement(class_name="product-list__col--thirds.col-8.mb-6.item")
    go_to_page = spf_lib.PageElement(class_name="pages__last")
    page_bucket = spf_lib.PageElement(class_name="pages.align-items-center.center ")


class RossmannProductComponents:
    price_footer = spf_lib.PageElement(class_name="tile-product__price.position-relative")
    promotion_footer = spf_lib.PageElement(class_name="pt-2.tile-product__lowest-price")
    price = spf_lib.PageElement(class_name="tile-product__promo-price")
    price_norm = spf_lib.PageElement(class_name="tile-product__old-price")
    price_lowest = spf_lib.PageElement(class_name= "text-nowrap")
    
    name = spf_lib.PageElement(class_name="tile-product__name")
    link = spf_lib.PageElement(class_name="tile-product__name")



class RossmannProduct:
    def __init__(self, product) -> None:
        # availability check
        self.is_available = True

        # sale check
        try:
            promotion_footer = product.find_element(RossmannProductComponents.promotion_footer.locator, RossmannProductComponents.promotion_footer.name)
            self.price_lowest = promotion_footer.find_element(RossmannProductComponents.price_lowest.locator, RossmannProductComponents.price_lowest.name).text
            self.price_regular = product.find_element(RossmannProductComponents.price_norm.locator, RossmannProductComponents.price_norm.name).text
            self.is_on_sale = True
        except:
            self.is_on_sale = False

        # read key properties of on-sale items
        try:
            self.product = product
            self.name = product.find_element(RossmannProductComponents.name.locator, RossmannProductComponents.name.name).text
            self.link = product.find_element(RossmannProductComponents.link.locator, RossmannProductComponents.link.name).get_attribute("href")
        except:
            pass

        # on sale items have prices hidden in different classes - no point bothering with them, we're looking for cheap stuff
        try:
            self.price = product.find_element(RossmannProductComponents.price.locator, RossmannProductComponents.price.name).text
        except:
            # IDGF
            self.price = "Probably not on sale :("

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
 
    
class RossmannWebScraper(spf_lib.WebScraper):
    def __init__(self, URL):
        super().__init__(URL)
        self.search_bar = RossmannPageComponents.search_bar
        self.next_page_button = RossmannPageComponents.next_page_button
        self.all_item_list = RossmannPageComponents.all_item_list

    

    def num_pages(self):
        page = RossmannPageComponents.go_to_page
        num_pages = self.driver.find_elements(page.locator, page.name)
        last_page_num = int(num_pages[-1].text)

        return last_page_num


    def goto_next_page(self):
        page_bucket = self.driver.find_element(RossmannPageComponents.page_bucket.locator, RossmannPageComponents.page_bucket.name)
        buttons = page_bucket.find_elements(RossmannPageComponents.next_page_button.locator, RossmannPageComponents.next_page_button.name)
        next = buttons[-1]
        actions = ActionChains(self.driver)
        actions.move_to_element(next).click().perform()


    def scrape(self, item: str, item_type: str):
        self.open_website()

        # print header of matching item list
        print(f"\n\nROSSMANN \n{self.driver.title}\n")

        # use search bar to search for phrase defined in "item"
        self.find_single(RossmannPageComponents.search_button).click()
        time.sleep(0.5)
        self.search(item)
        time.sleep(3)
        self.click(RossmannPageComponents.pop_up_dismiss)
        self.scroll(0, end=True)

        # search all pages except the last one (usually garbage offers, not available products, etc.)
        for i in range(1, self.num_pages()): 
            # read all item list
            print(f"Page: {i}")
            products = self.find_all(self.all_item_list)

            # iterate over list of products
            for product in products:
                spf = RossmannProduct(product)
                if not spf.is_on_sale or not spf.is_available:
                    continue

                # print only items containing "SPF50" phrase
                for type in item_type:
                    if type in spf.name:
                        print(spf)
            
            time.sleep(3)
            # proceed to the next page
            self.goto_next_page()
            time.sleep(1)

            # open page and scroll to the bottom of the page to load all items and "Next Page" button
            self.scroll(1, end=True)
            
