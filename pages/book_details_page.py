from playwright.sync_api import Locator

from pages.base_page import BasePage


class BookDetailsPage(BasePage):

    TITLE = "div.product_main h1"
    PRODUCT_MAIN = "div.product_main"
    PRODUCT_INFO_TABLE = "table.table-striped"

    @property
    def title(self) -> Locator:
        return self.page.locator(self.TITLE)

    @property
    def product_main(self) -> Locator:
        #title, price, stock and rating
        return self.page.locator(self.PRODUCT_MAIN)

    @property
    def product_info_table(self) -> Locator:
        return self.page.locator(self.PRODUCT_INFO_TABLE)

    def go_back(self) -> None:
        self.page.go_back()