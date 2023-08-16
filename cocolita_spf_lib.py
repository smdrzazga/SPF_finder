import spf_lib

import time

class CocolitaPageComponents:
    search_bar = spf_lib.PageElement(name=f"q")
    next_page_button = spf_lib.PageElement(class_name="next")
    # pop_up_dismiss = spf_lib.PageElement(id="onetrust-close-btn-container")
    all_item_list = spf_lib.PageElement(class_name="product-box.gallery.clearfix")
    page_bucket = spf_lib.PageElement(class_name="pagination ")


class CocolitaProductComponents:
    price_footer = spf_lib.PageElement(class_name="product-price-container")
    promotion_label = spf_lib.PageElement(class_name="product-label.promotion")
    price = spf_lib.PageElement(class_name="discount-price")
    price_norm = spf_lib.PageElement(class_name="base-price")

    name = spf_lib.PageElement(class_name="product-name")
    link = spf_lib.PageElement(class_name="product-hover-opacity")



class CocolitaProduct:
    def __init__(self, product) -> None:
        # availability check
        self.is_available = True

        # sale check
        try:
            self.is_on_sale = False
            discount = product.find_element(CocolitaProductComponents.promotion_label.locator, CocolitaProductComponents.promotion_label.name).text
            if discount != "":
                self.is_on_sale = True
        except:
            self.is_on_sale = False

        # read key properties of on-sale items
        try:
            self.product = product
            self.price_regular = product.find_element(CocolitaProductComponents.price_norm.locator, CocolitaProductComponents.price_norm.name).text
            self.name = product.find_element(CocolitaProductComponents.name.locator, CocolitaProductComponents.name.name).text
            self.link = product.find_element(CocolitaProductComponents.link.locator, CocolitaProductComponents.link.name).get_attribute("href")
        except:
            pass

        # on sale items have prices hidden in different classes - no point bothering with them, we're looking for cheap stuff
        try:
            self.price = product.find_element(CocolitaProductComponents.price.locator, CocolitaProductComponents.price.name).text
        except:
            # IDGF
            self.price = "Probably not on sale :("

    def __repr__(self) -> str:
        try:
            # if on sale - print also sale-referring prices
            return f"{self.price} ({self.price_regular} / Unknown ) \n{self.name}, \n{self.link}\n"
        except:
            # if not on sale - print only bare minimum
            return f"{self.price} \n{self.name}, \n{self.link}\n"
 
    
class CocolitaWebScraper(spf_lib.WebScraper):
    def __init__(self, URL):
        super().__init__(URL)
        self.search_bar = CocolitaPageComponents.search_bar
        self.next_page_button = CocolitaPageComponents.next_page_button
        self.all_item_list = CocolitaPageComponents.all_item_list

    

    def num_pages(self):
        num_pages = self.driver.find_element(CocolitaPageComponents.page_bucket.locator, CocolitaPageComponents.page_bucket.name).text
        last_page_num = ''.join(num_pages).split()[-1]

        return int(last_page_num)


    def scrape(self, item: str, item_type: str):

        # print header of matching item list
        self.open_website()
        print(f"\n\nCOCOLITA \n{self.driver.title}\n")

        # use search bar to search for phrase defined in "item"
        self.search(item)
        time.sleep(0.5) 


        # search all pages except the last one (usually garbage offers, not available products, etc.)
        for i in range(1, self.num_pages()): 
            # open page and scroll to the bottom of the page to load all items and "Next Page" button
            print(f"Page: {i}")            
            self.scroll(0, end=True)
            
            # read all item list
            products = self.find_all(self.all_item_list)

            # iterate over list of products
            for product in products:
                spf = CocolitaProduct(product)
                if not spf.is_on_sale or not spf.is_available:
                    continue

                # print only items containing "SPF50" phrase
                for type in item_type:
                    if type in spf.name:
                        print(spf)
            
            time.sleep(2)
            # proceed to the next page
            self.hover_and_click(self.next_page_button)
            
