#share fixture and hooks
import allure
import pytest

from pages.book_details_page import BookDetailsPage
from pages.home_page import HomePage


@pytest.fixture
def home_page(page) -> HomePage:
    return HomePage(page).load()

@pytest.fixture
def book_details_page(page) -> BookDetailsPage:
    return BookDetailsPage(page)

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