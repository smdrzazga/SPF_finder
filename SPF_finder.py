import time

import spf_lib as sz
import hebe_spf_lib as hebe
import superpharm_spf_lib as sup
import pigment_spf_lib as pig
import rossmann_spf_lib as ross
import cocolita_spf_lib as coco
import douglas_spf_lib as dgl
import ezebra_spf_lib as ez

# define item to look for and website:
item = "spf"
model = ["SPF50", "SPF 50"]

# use chrome driver, assume chromedriver added to environmental variable PATH
dictionary = {
    hebe.HebeWebScraper: "https://www.hebe.pl",
    sup.SuperpharmWebScraper: "https://www.superpharm.pl/",
    pig.PigmentWebScraper: "https://drogeriapigment.pl/",
    ross.RossmannWebScraper: "https://www.rossmann.pl/",
    coco.CocolitaWebScraper: "https://www.cocolita.pl/",
    dgl.DouglasWebScraper: "https://www.douglas.pl/pl",
    ez.EzebraWebScraper: "https://www.ezebra.pl/"
}

# print header of matching item list
print(sz.WebScraper.legend)

for webscraper, webpage in zip(dictionary, dictionary.values()):
    scraper = webscraper(webpage)
    scraper.scrape(item, model)
    scraper.quit()


# TODO
# more websites:
    # superpharm (+)
    # pigment (+)
    # rossman (+)
    # cocolita (+)
    # Douglas (+)
    # ezebra (+)




# Dependencies:
# selenium
# chromedriver added to PATH environmental variables
