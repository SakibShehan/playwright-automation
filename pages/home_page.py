from playwright.sync_api import Locator

import config
from pages.base_page import BasePage



#actions for home page testing 
class HomePage(BasePage):


    HEADINGS = "h1, h2, h3, h4, h5, h6"
    BOOKS_SECTION = "ol.row"
    BOOK_ITEMS = "ol.row article.product_pod"

    def load(self) -> "HomePage":
     #Open the homepage and return self for chaining
        self.open(config.BOOKS_HOME_URL)
        return self

    @property
    def visible_headings(self) -> Locator:
        #check visible headings
        return self.page.locator(self.HEADINGS).filter(visible=True)

    @property
    def books_section(self) -> Locator:
        #this container holds  book grid
        return self.page.locator(self.BOOKS_SECTION)

    @property
    def book_items(self) -> Locator:
        #showing book card
        return self.page.locator(self.BOOK_ITEMS)