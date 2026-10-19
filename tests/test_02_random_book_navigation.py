
import random
import re

import allure
import pytest
from playwright.sync_api import expect

import config

RANDOM_BOOK_INDEXES = random.sample(range(config.BOOKS_PER_PAGE), config.RANDOM_BOOK_COUNT)


@allure.feature("Book Navigation")
@pytest.mark.regression
class TestRandomBookNavigation:

    #Checks each random book opens its own details page

    @pytest.mark.parametrize(
        "book_index",
        RANDOM_BOOK_INDEXES,
        ids=[f"book_position_{i + 1}" for i in RANDOM_BOOK_INDEXES],
    )
    def test_random_book_opens_correct_details(self, home_page, book_details_page, book_index):
        page = home_page.page

        with allure.step("Capture the book title"):
            expected_title = home_page.get_book_title(book_index)
            allure.dynamic.title(f"Book opens correct details: {expected_title}")

        with allure.step("Click the book"):
            home_page.open_book(book_index)

        with allure.step("Verify details page loaded"):
            expect(page).to_have_url(re.compile(config.BOOK_DETAILS_URL_PATTERN))

        with allure.step("Verify H1 matches the selected book title"):
            expect(book_details_page.title).to_have_text(expected_title)

        with allure.step("Verify book information is visible"):
            expect(book_details_page.product_main).to_be_visible()
            expect(book_details_page.product_info_table).to_be_visible()

        with allure.step("Navigate back to homepage"):
            book_details_page.go_back()
            expect(page).to_have_url(config.BOOKS_HOME_URL)