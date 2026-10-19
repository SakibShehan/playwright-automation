import logging
import random

from playwright.sync_api import Locator

import config
from pages.base_page import BasePage

logger = logging.getLogger(__name__)

#actions for home page testing 
class HomePage(BasePage):


    HEADINGS = "h1, h2, h3, h4, h5, h6"
    BOOKS_SECTION = "ol.row"
    BOOK_ITEMS = "ol.row article.product_pod"
    BOOK_TITLE_LINK = "h3 a"

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

    
    def get_book_count(self) -> int:
        return self.book_items.count()

    def get_random_book_indexes(self, count: int) -> list[int]:
    #Return  unique random positions of books on the page
        indexes = random.sample(range(self.get_book_count()), count)
        logger.info("Randomly selected book positions: %s", indexes)
        return indexes

    def get_book_title(self, index: int) -> str:
        
        #Return the full title of the book at index
        link = self.book_items.nth(index).locator(self.BOOK_TITLE_LINK)
        return link.get_attribute("title")

    def open_book(self, index: int) -> None:
        #click the book to open its details page
        logger.info("Opening book at position %s", index)
        self.book_items.nth(index).locator(self.BOOK_TITLE_LINK).click()