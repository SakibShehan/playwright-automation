import allure
import pytest
from playwright.sync_api import expect

import config


@allure.feature("Homepage")
@pytest.mark.smoke
class TestHomepage:

    @allure.title("Homepage URL is correct")
    def test_url_is_correct(self, home_page):
        expect(home_page.page).to_have_url(config.BOOKS_HOME_URL)

    @allure.title("Homepage title is correct")
    def test_title_is_correct(self, home_page):
        expect(home_page.page).to_have_title(config.BOOKS_HOME_TITLE)

    @allure.title("All visible headings are displayed")
    def test_headings_are_visible(self, home_page):
        headings = home_page.visible_headings
        assert headings.count() > 0, "No visible headings found"
        for index in range(headings.count()):
            expect(headings.nth(index)).to_be_visible()

    @allure.title("Every visible heading has text")
    def test_headings_have_text(self, home_page):
        texts = home_page.visible_headings.all_inner_texts()
        assert texts, "No visible headings found"
        for index, text in enumerate(texts):
            assert text.strip(), f"Heading #{index} is empty"

    @allure.title("Books section is visible")
    def test_books_section_is_visible(self, home_page):
        expect(home_page.books_section).to_be_visible()

    @allure.title("Books section contains at least one book")
    def test_books_list_is_not_empty(self, home_page):
        expect(home_page.book_items).not_to_have_count(0)