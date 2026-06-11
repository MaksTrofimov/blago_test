from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class CompaniesPage(BasePage):
    PAGE_PATH = "/companies"
    EXPECTED_URL_PART = "/companies"

    COMPANY_CARD_LINKS = (
        By.XPATH,
        "//a[contains(@href, '/companies/view/')]"
    )

    def open(self):
        self.open_path(self.PAGE_PATH)

    def should_be_opened(self):
        current_url = self.get_current_url()
        assert self.EXPECTED_URL_PART in current_url, (
            f"Expected '{self.EXPECTED_URL_PART}' in URL, but got '{current_url}'"
        )

    def open_first_company_card(self):
        link = self._get_first_visible_company_link()
        card_url = link.get_attribute("href")

        assert card_url, "Company card URL should not be empty"

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            link
        )

        # Открываем URL, найденный в интерфейсе.
        # Это устойчивее обычного click для страниц со сложной версткой.
        self.driver.get(card_url)

        WebDriverWait(self.driver, self.DEFAULT_TIMEOUT).until(
            lambda driver: "/companies/view/" in driver.current_url
        )

        return card_url

    def _get_first_visible_company_link(self):
        WebDriverWait(self.driver, self.DEFAULT_TIMEOUT).until(
            lambda driver: len(driver.find_elements(*self.COMPANY_CARD_LINKS)) > 0
        )

        links = self.driver.find_elements(*self.COMPANY_CARD_LINKS)

        for link in links:
            if link.is_displayed():
                return link

        # Если Selenium считает ссылки невидимыми из-за особенностей верстки,
        # берем первую ссылку, у которой есть href.
        for link in links:
            href = link.get_attribute("href")
            if href:
                return link

        raise AssertionError("Visible company card link was not found")