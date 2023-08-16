import spf_lib

import time


class SuperpharmPageComponents:
    search_bar = spf_lib.PageElement(id=f"autocomplete-0-input")
    # search_button = spf_lib.PageElement(xpath='//*[@id="wrapper"]/div[1]/div[1]/div[1]/div/div[6]/div[2]/div/div/div[2]/a')
    next_page_button = spf_lib.PageElement(class_name="ais-Pagination-item.ais-Pagination-item--nextPage")
    # pop_up_dismiss = spf_lib.PageElement(id="close-button-1454703513202")
    all_item_list = spf_lib.PageElement(class_name="ais-Hits-item")
    go_to_page = spf_lib.PageElement(class_name="ais-Pagination-link")


class SuperpharmProductComponents:
    price_footer = spf_lib.PageElement(class_name="price-wrapper")
    price_norm = spf_lib.PageElement(class_name="before_special")
    price_lowest = spf_lib.PageElement(class_name= "lowest-big")
    label = spf_lib.PageElement(class_name="amlabel-text")
    
    price = spf_lib.PageElement(class_name="after_special.promotion")
    name = spf_lib.PageElement(class_name="result-title.text-ellipsis")
    description = spf_lib.PageElement(class_name="result-description.text-ellipsis")
    link = spf_lib.PageElement(class_name="result")

    # product_unavailable = spf_lib.PageElement(class_name="product-tile.js-product-tile.product-tile--non-available")




class SuperpharmProduct:
    def __init__(self, product) -> None:
        # availability check
        try:
            product.find_element(SuperpharmProductComponents.product_unavailable.locator, SuperpharmProductComponents.product_unavailable.name)
            self.is_available = False
        except:
            self.is_available = True

        # sale check
        try:
            labels = product.find_elements(SuperpharmProductComponents.label.locator, SuperpharmProductComponents.label.name)
            self.is_on_sale = False
            for label in labels:
                if "PROMOCJA" in label.text:
                    self.is_on_sale = True
            self.price_regular = product.find_element(SuperpharmProductComponents.price_norm.locator, SuperpharmProductComponents.price_norm.name).text
            self.price_lowest = product.find_element(SuperpharmProductComponents.price_lowest.locator, SuperpharmProductComponents.price_lowest.name).text
        except:
            self.is_on_sale = False

        # read key properties of on-sale items
        self.product = product
        self.name = product.find_element(SuperpharmProductComponents.name.locator, SuperpharmProductComponents.name.name).text
        self.description = product.find_element(SuperpharmProductComponents.description.locator, SuperpharmProductComponents.description.name).text
        self.link = product.find_element(SuperpharmProductComponents.link.locator, SuperpharmProductComponents.link.name).get_attribute("href")
        
        # on sale items have prices hidden in different classes - no point bothering with them, we're looking for cheap stuff
        try:
            self.price = product.find_element(SuperpharmProductComponents.price.locator, SuperpharmProductComponents.price.name).text
        except:
            # IDGF
            self.price = "Probably not on sale :("

    def __repr__(self) -> str:
        try:
            # if on sale - print also sale-referring prices
            text = ""
            if self.price > self.price_lowest:
                text += "Is it really on sale...?\n"
            return text + f"{self.price} ({self.price_regular} / {self.price_lowest} ) \n{self.name}, {self.description} \n{self.link}\n"
        except:
            # if not on sale - print only bare minimum
            return f"{self.price} \n{self.name}, {self.description} \n{self.link}\n"
 
    
class SuperpharmWebScraper(spf_lib.WebScraper):
    def __init__(self, URL):
        super().__init__(URL)
        self.search_bar = SuperpharmPageComponents.search_bar
        self.next_page_button = SuperpharmPageComponents.next_page_button
        self.all_item_list = SuperpharmPageComponents.all_item_list
        # self.search_button = SuperpharmPageComponents.search_button
        # self.pop_up_dismiss = SuperpharmPageComponents.pop_up_dismiss

    

    def num_pages(self):
        page = SuperpharmPageComponents.go_to_page
        num_pages = self.driver.find_elements(page.locator, page.name)
        last_page_num = int(num_pages[-1].text)

        return last_page_num


    def scrape(self, item: str, item_type: str):
        self.open_website()

        # print header of matching item list
        print(f"\n\nSUPERPHARM \n{self.driver.title}\n")

        # check for special offer - need to close the pop-up window
        # time.sleep(5)
        # try:
        #     self.click(self.pop_up_dismiss)
        # except:
        #     pass 

        # use search bar to search for phrase defined in "item"
        self.search(item)
        time.sleep(2)

        # search all pages except the last one (usually garbage offers, not available products, etc.)
        for i in range(1, self.num_pages()): 
            # open page and scroll to the bottom of the page to load all items and "Next Page" button
            print(f"Page: {i}")            
            self.scroll(0, end=True)

            # read all item list
            products = self.find_all(self.all_item_list)
            time.sleep(1)
            # iterate over list of products
            for product in products:
                spf = SuperpharmProduct(product)

                if not spf.is_on_sale or not spf.is_available:
                    continue

                # print only items containing "SPF50" phrase
                for type in item_type:
                    if type in spf.name:
                        print(spf)
            
            time.sleep(3)
            # proceed to the next page
            self.hover_and_click(self.next_page_button)