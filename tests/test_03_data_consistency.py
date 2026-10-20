
import random
import re

import allure
import pytest
from playwright.sync_api import expect

import config

CONSISTENCY_BOOK_INDEXES = random.sample(range(config.BOOKS_PER_PAGE), config.RANDOM_BOOK_COUNT)


@allure.feature("Data Consistency")
@pytest.mark.regression
class TestBookDataConsistency:

    #Checks homepage title and price match the details page

    @pytest.mark.parametrize(
        "book_index",
        CONSISTENCY_BOOK_INDEXES,
        ids=[f"book_position_{i + 1}" for i in CONSISTENCY_BOOK_INDEXES],
    )
    def test_homepage_data_matches_details_page(self, home_page, book_details_page, book_index):
        page = home_page.page

        with allure.step("Capture homepage title"):
            home_title = home_page.get_book_title(book_index)
            allure.dynamic.title(f"Data matches: {home_title}")
            allure.attach(home_title, name="homepage title", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Capture homepage price"):
            home_price = home_page.get_book_price(book_index)
            allure.attach(home_price, name="homepage price", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Open the book details page"):
            home_page.open_book(book_index)
            expect(page).to_have_url(re.compile(config.BOOK_DETAILS_URL_PATTERN))

        with allure.step("Capture details page title"):
            details_title = book_details_page.get_book_title()
            allure.attach(details_title, name="details title", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Capture details page price"):
            details_price = book_details_page.get_price()
            allure.attach(details_price, name="details price", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Compare homepage title with details page title"):
            assert home_title == details_title, f"Title mismatch: home='{home_title}' details='{details_title}'"

        with allure.step("Compare homepage price with details page price"):
            assert home_price == details_price, f"Price mismatch: home='{home_price}' details='{details_price}'"

        with allure.step("Navigate back to homepage"):
            book_details_page.go_back()
            expect(page).to_have_url(config.BOOKS_HOME_URL)