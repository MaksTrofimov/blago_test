from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class DonationFormPage(BasePage):
    UPPER = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯABCDEFGHIJKLMNOPQRSTUVWXYZ"
    LOWER = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz"

    CART_MODAL = (
        By.XPATH,
        "//*[contains(normalize-space(), 'У вас') "
        "and contains(normalize-space(), 'пожертвование')]"
    )

    AMOUNT_INPUTS = (
        By.XPATH,
        "//input[not(@type='hidden')]"
    )

    PAYMENT_BUTTON = (
        By.XPATH,
        "//*[not(ancestor::footer) and contains("
        f"translate(normalize-space(.), '{UPPER}', '{LOWER}'), "
        "'перейти к оплате'"
        ")]"
    )

    def should_be_opened_after_click(self, previous_url):
        try:
            WebDriverWait(self.driver, self.DEFAULT_TIMEOUT).until(
                lambda driver: (
                    self.is_element_visible(self.CART_MODAL)
                    or self.is_element_visible(self.PAYMENT_BUTTON)
                    or driver.current_url != previous_url
                )
            )
        except TimeoutException:
            raise AssertionError(
                "Donation cart or next donation step was not opened"
            )

    def should_have_cart_modal(self):
        modal = self.wait_for_visible(self.CART_MODAL)
        assert modal.is_displayed(), "Donation cart modal was not opened"

    def should_have_amount(self, expected_amount):
        expected_amount = str(expected_amount)

        modal = self.wait_for_visible(self.CART_MODAL)
        modal_text = modal.text.replace("\n", " ")

        if expected_amount in modal_text:
            return

        inputs = self.driver.find_elements(*self.AMOUNT_INPUTS)
        visible_values = []

        for input_element in inputs:
            if not input_element.is_displayed():
                continue

            value = input_element.get_attribute("value") or ""
            visible_values.append(value)

            if expected_amount in value:
                return

        raise AssertionError(
            f"Expected donation amount '{expected_amount}' was not found. "
            f"Modal text: '{modal_text}'. "
            f"Visible input values: {visible_values}"
        )

    def should_have_payment_button(self):
        button = self.wait_for_visible(self.PAYMENT_BUTTON)
        assert button.is_displayed(), "Payment button was not found"