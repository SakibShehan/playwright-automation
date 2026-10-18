# it is a base class , share common properties among pages
import logging

from playwright.sync_api import Page

logger = logging.getLogger(__name__)


class BasePage:

    def __init__(self, page: Page):
        self.page = page

    def open(self, url: str) -> None:
       #navigating to url
        logger.info("Opening %s", url)
        self.page.goto(url)

    def get_title(self) -> str:
        return self.page.title()

    def get_current_url(self) -> str:
        return self.page.url