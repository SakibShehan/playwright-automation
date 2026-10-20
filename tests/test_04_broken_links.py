import allure
import pytest


@allure.feature("Broken Links")
@pytest.mark.regression

class TestBrokenLinks:
    #Checks every unique link on the homepage returns HTTP 200

    @allure.title("All homepage links return HTTP 200")
    def test_all_links_return_200(self, home_page):
        with allure.step("Collect all anchor elements and extract href values"):
            links = home_page.get_unique_links()
            assert links, "No links found on homepage"

        with allure.step(f"Remove duplicates: {len(links)} unique links"):
            allure.attach("\n".join(links), name="unique links", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Send a request to each URL and verify the status code"):
            broken_links = []
            report_lines = []
            for url in links:
                status = home_page.get_status_code(url)
                report_lines.append(f"{status}  {url}")
                if status != 200:
                    broken_links.append(f"{status}  {url}")
            allure.attach("\n".join(report_lines), name="status codes", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Verify no broken links exist"):
            assert not broken_links, f"{len(broken_links)} broken link(s):\n" + "\n".join(broken_links)