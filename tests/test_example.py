import re
from playwright.sync_api import Page, expect


def test_has_title(page: Page):
    page.goto("https://books.toscrape.com/index.html")
    expect(page).to_have_title(re.compile("Books to Scrape"))