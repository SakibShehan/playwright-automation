from playwright.sync_api import Locator

import config
from pages.base_page import BasePage


class QuotesPage(BasePage):

    LOGIN_LINK = "a[href='/login']"
    LOGOUT_LINK = "a[href='/logout']"
    USERNAME_FIELD = "#username"
    PASSWORD_FIELD = "#password"
    SUBMIT_BUTTON = "input[type='submit']"
    LOGIN_FORM = "form"

    def load(self) -> "QuotesPage":
        self.open(config.QUOTES_BASE_URL)
        return self

    @property
    def login_link(self) -> Locator:
        return self.page.locator(self.LOGIN_LINK)

    @property
    def logout_link(self) -> Locator:
        return self.page.locator(self.LOGOUT_LINK)

    @property
    def username_field(self) -> Locator:
        return self.page.locator(self.USERNAME_FIELD)

    @property
    def password_field(self) -> Locator:
        return self.page.locator(self.PASSWORD_FIELD)

    @property
    def submit_button(self) -> Locator:
        return self.page.locator(self.SUBMIT_BUTTON)

    def click_login_link(self) -> None:
        self.login_link.click()

    def enter_credentials(self, username: str, password: str) -> None:
        self.username_field.fill(username)
        self.password_field.fill(password)

    def submit_login(self):
        with self.page.expect_response("**/login") as response_info:
            self.submit_button.click()
        return response_info.value