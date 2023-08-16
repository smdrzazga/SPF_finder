import spf_lib

import time


class PigmentPageComponents:
    search_bar = spf_lib.PageElement(name=f"search_word")
    # next_page_button = spf_lib.PageElement(class_name="ais-Pagination-item.ais-Pagination-item--nextPage")
    pop_up_dismiss_rodo = spf_lib.PageElement(class_name="js-rodo-close")
    pop_up_dismiss_promotion = spf_lib.PageElement(class_name="bhr-ap__c__close.ap-close-event.bhr-ap__c__close--3")
    all_item_list = spf_lib.PageElement(css_selector='#product_list li[itemprop=itemListElement]')
    # go_to_page = spf_lib.PageElement(class_name="ais-Pagination-link")


class PigmentProductComponents:
    price_footer = spf_lib.PageElement(class_name="content_price")
    price_norm = spf_lib.PageElement(class_name="old-price.product-price")
    label = spf_lib.PageElement(class_name="sale-label-custom2")
    
    price = spf_lib.PageElement(class_name="price.product-price")
    name = spf_lib.PageElement(class_name="manufacturer-info-block")
    description = spf_lib.PageElement(class_name="product-name")
    link = spf_lib.PageElement(class_name="product-name")

    product_unavailable = spf_lib.PageElement(class_name="button.high.mailalert_link2")




class PigmentProduct:
    def __init__(self, product) -> None:
        # availability check
        try:
            product.find_element(PigmentProductComponents.product_unavailable.locator, PigmentProductComponents.product_unavailable.name)
            self.is_available = False
        except:
            self.is_available = True

        # sale check
        try:
            labels = product.find_elements(PigmentProductComponents.label.locator, PigmentProductComponents.label.name)
            self.is_on_sale = False
            for label in labels:
                if "PROMOCJA" in label.text:
                    self.is_on_sale = True
            self.price_regular = product.find_element(PigmentProductComponents.price_norm.locator, PigmentProductComponents.price_norm.name).text
        except:
            self.is_on_sale = False

        # read key properties of on-sale items
        self.product = product
        self.name = product.find_element(PigmentProductComponents.name.locator, PigmentProductComponents.name.name).text
        self.description = product.find_element(PigmentProductComponents.description.locator, PigmentProductComponents.description.name).text
        self.link = product.find_element(PigmentProductComponents.link.locator, PigmentProductComponents.link.name).get_attribute("href")
        self.price = product.find_element(PigmentProductComponents.price.locator, PigmentProductComponents.price.name).text


    def __repr__(self) -> str:
        try:
            # if on sale - print also sale-referring prices
            return f"{self.price} ({self.price_regular} / 'No data' ) \n{self.name}, {self.description} \n{self.link}\n"
        except:
            # if not on sale - print only bare minimum
            return f"{self.price} \n{self.name}, {self.description} \n{self.link}\n"
 
    
class PigmentWebScraper(spf_lib.WebScraper):
    def __init__(self, URL):
        super().__init__(URL)
        self.search_bar = PigmentPageComponents.search_bar
        # self.next_page_button = PigmentPageComponents.next_page_button
        self.all_item_list = PigmentPageComponents.all_item_list


    def scrape(self, item: str, item_type: str):
        self.open_website()

        # print header of matching item list
        print(f"\n\nPIGMENT \n{self.driver.title}\n")

        # use search bar to search for phrase defined in "item"
        self.search(item)
        time.sleep(2)

        # search all pages except the last one (usually garbage offers, not available products, etc.)
        for i in range(20):
            # open page and scroll to the bottom of the page to load all items and "Next Page" button
            try:
                cross = self.driver.find_element(PigmentPageComponents.pop_up_dismiss_promotion.locator, PigmentPageComponents.pop_up_dismiss_promotion.name)
                self.hover_and_click(PigmentPageComponents.pop_up_dismiss_promotion)
            except:
                pass

            try:
                cross = self.driver.find_element(PigmentPageComponents.pop_up_dismiss_rodo.locator, PigmentPageComponents.pop_up_dismiss_rodo.name)
                self.hover_and_click(PigmentPageComponents.pop_up_dismiss_rodo)
            except:
                pass
            finally:
                self.scroll(0, end=True)
            time.sleep(0.5)

        time.sleep(1)
        
        # read all item list
        products = self.find_all(self.all_item_list)
        print(len(products))
        time.sleep(4)

        # iterate over list of products
        for product in products:
            spf = PigmentProduct(product)

            if not spf.is_on_sale or not spf.is_available:
                continue

            # print only items containing "SPF50" phrase
            for type in item_type:
                if type in spf.description:
                    print(spf)
        time.sleep(5)