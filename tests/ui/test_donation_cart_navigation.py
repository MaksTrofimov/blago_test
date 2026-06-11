import allure

from pages.main_page import MainPage
from pages.action_page import ActionPage
from utils.config import TEST_DONATION_AMOUNT


@allure.feature("UI-тесты")
@allure.story("Корзина пожертвований")
@allure.title("Проверка добавления пожертвования в корзину")
def test_add_donation_to_cart_from_action_card(driver, base_url):
    main_page = MainPage(driver, base_url)
    action_page = ActionPage(driver, base_url)

    with allure.step("Открыть главную страницу blago.ru"):
        main_page.open()

    with allure.step("Перейти к первой карточке действующего сбора"):
        main_page.open_first_action_card()

    with allure.step("Проверить, что открылась страница сбора"):
        action_page.should_be_opened()

    with allure.step("Ввести корректную сумму пожертвования и нажать кнопку 'Пожертвовать'"):
        action_page.add_donation_to_cart(amount=TEST_DONATION_AMOUNT)

    with allure.step("Проверить, что пожертвование добавлено в корзину"):
        action_page.should_be_added_to_cart()