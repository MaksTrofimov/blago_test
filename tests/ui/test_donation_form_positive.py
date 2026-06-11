import allure

from pages.main_page import MainPage
from pages.action_page import ActionPage
from pages.donation_form_page import DonationFormPage
from utils.config import TEST_DONATION_AMOUNT


@allure.feature("UI-тесты")
@allure.story("Форма пожертвования")
@allure.title("Позитивный сценарий заполнения формы пожертвования")
def test_fill_donation_form_with_valid_data(driver, base_url):
    main_page = MainPage(driver, base_url)
    action_page = ActionPage(driver, base_url)
    donation_form_page = DonationFormPage(driver, base_url)

    with allure.step("Открыть главную страницу blago.ru"):
        main_page.open()

    with allure.step("Перейти к первой карточке действующего сбора"):
        main_page.open_first_action_card()

    with allure.step("Проверить, что открылась страница сбора"):
        action_page.should_be_opened()

    with allure.step("Ввести корректную сумму пожертвования и добавить пожертвование в корзину"):
        action_page.add_donation_to_cart(amount=TEST_DONATION_AMOUNT)

    with allure.step("Проверить, что пожертвование добавлено в корзину"):
        action_page.should_be_added_to_cart()

    with allure.step("Перейти в корзину пожертвований"):
        previous_url = action_page.get_current_url()
        action_page.go_to_cart()

    with allure.step("Проверить, что открылась форма пожертвования"):
        donation_form_page.should_be_opened_after_click(previous_url)

    with allure.step("Проверить, что в форме отображается корректная сумма пожертвования"):
        donation_form_page.should_have_amount(TEST_DONATION_AMOUNT)

    with allure.step("Проверить, что доступна кнопка перехода к оплате"):
        donation_form_page.should_have_payment_button()