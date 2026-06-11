from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class ActionPage(BasePage):
    EXPECTED_URL_PART = "/actions/view/"

    UPPER = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯABCDEFGHIJKLMNOPQRSTUVWXYZ"
    LOWER = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz"

    PAGE_TITLE = (By.TAG_NAME, "h1")

    DESCRIPTION = (
        By.XPATH,
        "//h1/following::p[normalize-space()][1]"
    )

    COLLECTION_INFO = (
        By.XPATH,
        "//*[contains(normalize-space(), 'Собрано') "
        "or contains(normalize-space(), 'пожертвован') "
        "or contains(normalize-space(), 'осталось')]"
    )

    DONATION_AMOUNT_INPUT = (
        By.XPATH,
        "(//input[contains(@placeholder, 'Сумма пожертвования') "
        "or contains(@name, 'amount') "
        "or contains(@id, 'amount')])[1]"
    )

    DONATION_BUTTON_LOCATORS = [
        (
            By.XPATH,
            "//*[not(ancestor::footer) and "
            "(self::a or self::button or @role='button') and "
            "contains("
            f"translate(normalize-space(.), '{UPPER}', '{LOWER}'), "
            "'пожертвовать'"
            ")]"
        ),
        (
            By.XPATH,
            "//*[not(ancestor::footer) and "
            "self::input and "
            "contains("
            f"translate(@value, '{UPPER}', '{LOWER}'), "
            "'пожертвовать'"
            ")]"
        ),
    ]

    ADDED_TO_CART_TEXT = (
        By.XPATH,
        "//*[contains("
        f"translate(normalize-space(.), '{UPPER}', '{LOWER}'), "
        "'добавлен'"
        ") and contains("
        f"translate(normalize-space(.), '{UPPER}', '{LOWER}'), "
        "'корзин'"
        ")]"
    )

    GO_TO_CART_BUTTON = (
        By.XPATH,
        "//*[self::a or self::button or @role='button']"
        "[contains("
        f"translate(normalize-space(.), '{UPPER}', '{LOWER}'), "
        "'перейти в корзину'"
        ")]"
    )

    def should_be_opened(self):
        current_url = self.get_current_url()
        assert self.EXPECTED_URL_PART in current_url, (
            f"Expected '{self.EXPECTED_URL_PART}' in URL, but got '{current_url}'"
        )

    def should_have_title(self):
        title = self.wait_for_visible(self.PAGE_TITLE)
        assert title.text.strip(), "Action page title should not be empty"

    def should_have_description(self):
        description = self.wait_for_visible(self.DESCRIPTION)
        assert description.text.strip(), "Action page description should not be empty"

    def should_have_collection_info(self):
        collection_info = self.wait_for_visible(self.COLLECTION_INFO)
        assert collection_info.text.strip(), "Collection info should not be empty"

    def should_have_donation_button(self):
        self._get_donation_button()

    def set_donation_amount(self, amount):
        amount_input = self.wait_for_visible(self.DONATION_AMOUNT_INPUT)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            amount_input
        )
        amount_input.clear()
        amount_input.send_keys(str(amount))

    def clear_donation_amount(self):
        amount_input = self.wait_for_visible(self.DONATION_AMOUNT_INPUT)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            amount_input
        )
        amount_input.clear()

    def click_donation_button(self):
        button = self._get_donation_button()
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button
        )
        button.click()

    def add_donation_to_cart(self, amount="100"):
        self.set_donation_amount(amount)
        self.click_donation_button()

    def submit_empty_donation_amount(self):
        self.clear_donation_amount()
        self.click_donation_button()

    def submit_invalid_donation_amount(self, amount):
        self.set_donation_amount(amount)
        self.click_donation_button()

    def should_be_added_to_cart(self):
        message = self.wait_for_visible(self.ADDED_TO_CART_TEXT)
        assert message.is_displayed(), "Donation was not added to cart"

    def should_not_be_added_to_cart(self):
        try:
            WebDriverWait(self.driver, 3).until(
                lambda driver: self.is_element_visible(self.ADDED_TO_CART_TEXT)
            )
        except TimeoutException:
            self.should_be_opened()
            return

        raise AssertionError("Invalid donation amount was added to cart")

    def go_to_cart(self):
        button = self.wait_for_clickable(self.GO_TO_CART_BUTTON)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button
        )
        button.click()

    def _get_donation_button(self):
        for locator in self.DONATION_BUTTON_LOCATORS:
            try:
                button = self.wait_for_clickable(locator, timeout=3)
                assert button.is_displayed(), "Donation button should be displayed"
                return button
            except TimeoutException:
                continue

        raise AssertionError("Donation button was not found on action page")
    
    def get_donation_amount_value(self):
        amount_input = self.wait_for_visible(self.DONATION_AMOUNT_INPUT)
        return amount_input.get_attribute("value") or ""


    def should_not_accept_text_amount(self, text_value):
        self.set_donation_amount(text_value)
        actual_value = self.get_donation_amount_value()

        assert text_value not in actual_value, (
            f"Text value '{text_value}' should not be accepted by donation amount field, "
            f"but actual value is '{actual_value}'"
        )