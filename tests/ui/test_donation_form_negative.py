import pytest
import allure

from pages.main_page import MainPage
from pages.action_page import ActionPage


def open_first_action_page(driver, base_url):
    main_page = MainPage(driver, base_url)
    action_page = ActionPage(driver, base_url)

    main_page.open()
    main_page.open_first_action_card()
    action_page.should_be_opened()

    return action_page


@allure.feature("UI-тесты")
@allure.story("Форма пожертвования")
@allure.title("Негативный сценарий отправки формы пожертвования с пустой суммой")
def test_donation_form_with_empty_amount(driver, base_url):
    with allure.step("Открыть карточку действующего сбора"):
        action_page = open_first_action_page(driver, base_url)

    with allure.step("Очистить поле суммы и нажать кнопку 'Пожертвовать'"):
        action_page.submit_empty_donation_amount()

    with allure.step("Проверить, что пожертвование не добавлено в корзину"):
        action_page.should_not_be_added_to_cart()


@allure.feature("UI-тесты")
@allure.story("Форма пожертвования")
@allure.title("Негативный сценарий отправки формы пожертвования с некорректной числовой суммой")
@pytest.mark.parametrize(
    "invalid_amount",
    [
        "0",
        "-100",
    ]
)
def test_donation_form_with_invalid_numeric_amount(driver, base_url, invalid_amount):
    with allure.step("Открыть карточку действующего сбора"):
        action_page = open_first_action_page(driver, base_url)

    with allure.step(f"Ввести некорректную сумму '{invalid_amount}' и нажать кнопку 'Пожертвовать'"):
        action_page.submit_invalid_donation_amount(invalid_amount)

    with allure.step("Проверить, что пожертвование не добавлено в корзину"):
        action_page.should_not_be_added_to_cart()


@allure.feature("UI-тесты")
@allure.story("Форма пожертвования")
@allure.title("Негативный сценарий ввода текстового значения в поле суммы")
def test_donation_amount_field_does_not_accept_text(driver, base_url):
    with allure.step("Открыть карточку действующего сбора"):
        action_page = open_first_action_page(driver, base_url)

    with allure.step("Попытаться ввести текстовое значение в поле суммы"):
        action_page.should_not_accept_text_amount("abc")