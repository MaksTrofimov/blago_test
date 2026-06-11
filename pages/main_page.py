from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class MainPage(BasePage):
    PAGE_PATH = ""
    EXPECTED_TITLE_TEXT = "Благо"
    EXPECTED_URL_PART = "blago.ru"

    HELP_SECTION_TITLE = (
        By.XPATH,
        "//*[contains(normalize-space(), 'Вы можете помочь')]"
    )

    FIRST_COMPANY_CARD = (
        By.XPATH,
        "(//*[contains(normalize-space(), 'Вы можете помочь')]/following::a[contains(@href, '/companies/view/')])[1]"
    )

    FIRST_ACTION_CARD = (
        By.XPATH,
        "(//a[contains(@href, '/actions/view/')])[1]"
    )

    def open(self):
        self.open_path(self.PAGE_PATH)

    def should_be_opened(self):
        current_url = self.get_current_url()
        assert self.EXPECTED_URL_PART in current_url, (
            f"Expected '{self.EXPECTED_URL_PART}' in URL, but got '{current_url}'"
        )

    def should_have_correct_title(self):
        assert self.title_contains(self.EXPECTED_TITLE_TEXT), (
            f"Expected '{self.EXPECTED_TITLE_TEXT}' in title, but got '{self.get_title()}'"
        )

    def should_have_help_section(self):
        self.wait_for_visible(self.HELP_SECTION_TITLE)

    def open_first_company_card(self):
        self.should_have_help_section()

        card = self.wait_for_clickable(self.FIRST_COMPANY_CARD)
        card_url = card.get_attribute("href")

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            card
        )
        card.click()

        return card_url

    def open_first_action_card(self):
        card = self.wait_for_clickable(self.FIRST_ACTION_CARD)
        card_url = card.get_attribute("href")

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            card
        )
        card.click()

        return card_url