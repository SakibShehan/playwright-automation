#share fixture and hooks
import allure
import pytest


import config
from pages.book_details_page import BookDetailsPage
from pages.home_page import HomePage


@pytest.fixture
def home_page(page) -> HomePage:
    return HomePage(page).load()

@pytest.fixture
def book_details_page(page) -> BookDetailsPage:
    return BookDetailsPage(page)

@pytest.fixture(scope="module")
def scanned_pages(browser) -> list[dict]:
    
    #goes to 5 pages and keeps every image's details
    context = browser.new_context()
    home_page = HomePage(context.new_page()).load()
    results = []
    for page_number in range(1, config.MAX_PAGINATION_PAGES + 1):
        results.append(home_page.scan_images())
        if page_number == config.MAX_PAGINATION_PAGES or not home_page.has_next_page():
            break
        home_page.go_to_next_page(page_number + 1)
    context.close()
    return results

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    #attach  screenshot to the Allure report when a test fail
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            allure.attach(
                page.screenshot(full_page=True),
                name="failure-screenshot",
                attachment_type=allure.attachment_type.PNG,
            )