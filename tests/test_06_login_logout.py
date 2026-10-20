
import re
import allure
import pytest
from playwright.sync_api import expect

import config


@allure.feature("Login and Logout")
@pytest.mark.smoke
class TestLoginLogout:

    #Tests run in order and share one browser session

    @allure.title("The Quotes to Scrape homepage loads successfully")
    def test_homepage_loads(self, quotes_page):
        with allure.step("Navigate to Quotes to Scrape"):
            quotes_page.load()

        with allure.step("Verify the homepage loaded"):
            expect(quotes_page.page).to_have_url(config.QUOTES_BASE_URL)
            expect(quotes_page.page).to_have_title("Quotes to Scrape")

    @allure.title("The Login link is visible and clickable")
    def test_login_link_visible_and_clickable(self, quotes_page):
        with allure.step("Verify the Login link is visible"):
            expect(quotes_page.login_link).to_be_visible()

        with allure.step("Verify the Login link is enabled"):
            expect(quotes_page.login_link).to_be_enabled()

        with allure.step("Click the Login link"):
            quotes_page.click_login_link()

    @allure.title("The login page loads successfully")
    def test_login_page_loads(self, quotes_page):
        with allure.step("Verify the login page URL"):
            expect(quotes_page.page).to_have_url(re.compile(r".*/login"))

        with allure.step("Verify the login form is visible"):
            expect(quotes_page.username_field).to_be_visible()
            expect(quotes_page.password_field).to_be_visible()
            expect(quotes_page.submit_button).to_be_visible()

    @allure.title("The username and password fields accept the provided credentials")
    def test_fields_accept_credentials(self, quotes_page):
        with allure.step("Enter username and password"):
            quotes_page.enter_credentials(config.QUOTES_USERNAME, config.QUOTES_PASSWORD)

        with allure.step("Verify the fields hold the entered values"):
            expect(quotes_page.username_field).to_have_value(config.QUOTES_USERNAME)
            expect(quotes_page.password_field).to_have_value(config.QUOTES_PASSWORD)

    @allure.title("The login form submits successfully")
    def test_login_form_submits(self, quotes_page):
        with allure.step("Click the Login button and wait for the response"):
            response = quotes_page.submit_login()
            allure.attach(f"{response.status}  {response.url}", name="login response", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Verify the login request completed successfully"):
            assert response.status == config.LOGIN_SUCCESS_STATUS, f"Login request returned {response.status}, expected {config.LOGIN_SUCCESS_STATUS}"

    @allure.title("The application displays the authenticated page state")
    def test_authenticated_page_state(self, quotes_page):
        with allure.step("Verify the user is back on the quotes page"):
            expect(quotes_page.page).to_have_url(config.QUOTES_BASE_URL)

        with allure.step("Verify the Login link is gone"):
            expect(quotes_page.login_link).to_have_count(0)

    @allure.title("The Logout link becomes visible and is enabled after successful login")
    def test_logout_link_visible_and_enabled(self, quotes_page):
        with allure.step("Verify the Logout link is visible"):
            expect(quotes_page.logout_link).to_be_visible()

        with allure.step("Verify the Logout link is enabled"):
            expect(quotes_page.logout_link).to_be_enabled()