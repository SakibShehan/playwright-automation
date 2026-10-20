import allure
import pytest

import config


def expected_page_url(page_number):
    if page_number == 1:
        return config.BOOKS_HOME_URL
    return f"{config.BOOKS_BASE_URL}catalogue/page-{page_number}.html"


def has_required_attributes(image):
    return (
        bool(image["src"] and image["src"].strip())
        and bool(image["alt"] and image["alt"].strip())
        and "thumbnail" in (image["class"] or "")
    )


def find_problems(scanned_pages, is_valid, reason):
    problems = []
    for page_number, scanned in enumerate(scanned_pages, start=1):
        for position, image in enumerate(scanned["images"], start=1):
            if not is_valid(image):
                problems.append(f"page {page_number}, image {position}: {reason} -> {image}")
    return problems


@allure.feature("Product Images")
@pytest.mark.regression
class TestProductImages:

    #Each test checks one expected result using the pages scanned once

    @allure.title("Images are displayed correctly")
    def test_images_are_displayed(self, scanned_pages):
        with allure.step("Verify every page has product images"):
            for page_number, scanned in enumerate(scanned_pages, start=1):
                assert scanned["images"], f"No images found on page {page_number}"

        with allure.step("Verify every image is visible"):
            problems = find_problems(scanned_pages, lambda image: image["visible"], "image not visible")
            assert not problems, "\n".join(problems)

    @allure.title("All required attributes exist")
    def test_required_attributes_exist(self, scanned_pages):
        with allure.step("Verify src and alt are not empty and class contains thumbnail"):
            problems = find_problems(scanned_pages, has_required_attributes, "missing or empty attribute")
            assert not problems, "\n".join(problems)

    @allure.title("Pagination works successfully")
    def test_pagination_works(self, scanned_pages):
        visited_urls = [scanned["url"] for scanned in scanned_pages]
        allure.attach("\n".join(visited_urls), name="visited pages", attachment_type=allure.attachment_type.TEXT)

        with allure.step(f"Verify {config.MAX_PAGINATION_PAGES} pages were visited"):
            assert len(scanned_pages) == config.MAX_PAGINATION_PAGES, f"Visited only {len(scanned_pages)} page(s)"

        with allure.step("Verify each Next click opened the expected page"):
            for page_number, url in enumerate(visited_urls, start=1):
                assert url == expected_page_url(page_number), f"Page {page_number}: got {url}"

    @allure.title("Image validations pass on all visited pages")
    def test_validations_pass_on_all_pages(self, scanned_pages):
        summary = []
        for page_number, scanned in enumerate(scanned_pages, start=1):
            valid_count = sum(1 for image in scanned["images"] if image["visible"] and has_required_attributes(image))
            summary.append(f"page {page_number}: {valid_count}/{len(scanned['images'])} images valid  {scanned['url']}")
        allure.attach("\n".join(summary), name="page summary", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Verify every image passes every check on every page"):
            problems = find_problems(
                scanned_pages,
                lambda image: image["visible"] and has_required_attributes(image),
                "failed validation",
            )
            assert not problems, "\n".join(problems)