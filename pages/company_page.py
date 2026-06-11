from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CompanyPage(BasePage):
    EXPECTED_URL_PART = "/companies/view/"
    PAGE_PATH_TEMPLATE = "/companies/view/{company_id}"

    PAGE_TITLE = (By.TAG_NAME, "h1")

    def open_by_id(self, company_id):
        self.open_path(self.PAGE_PATH_TEMPLATE.format(company_id=company_id))

    def should_be_opened(self):
        current_url = self.get_current_url()
        assert self.EXPECTED_URL_PART in current_url, (
            f"Expected '{self.EXPECTED_URL_PART}' in URL, but got '{current_url}'"
        )

    def should_have_title(self):
        title = self.wait_for_visible(self.PAGE_TITLE)
        assert title.text.strip(), "Company page title should not be empty"

    def get_title_text(self):
        title = self.wait_for_visible(self.PAGE_TITLE)
        return title.text.strip()

    def should_have_company_name(self, expected_name):
        actual_name = self.get_title_text()

        expected_normalized = self._normalize_text(expected_name)
        actual_normalized = self._normalize_text(actual_name)

        expected_core = (
            expected_normalized
            .split("—")[0]
            .split("-")[0]
            .split("(")[0]
            .strip()
        )

        assert (
            expected_normalized in actual_normalized
            or actual_normalized in expected_normalized
            or expected_core in actual_normalized
        ), (
            f"Expected company name from API '{expected_name}' "
            f"to match UI title '{actual_name}'"
        )

    @staticmethod
    def _normalize_text(text):
        return " ".join(str(text).lower().split())