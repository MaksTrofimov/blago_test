import allure

from pages.main_page import MainPage
from pages.action_page import ActionPage


@allure.feature("UI-тесты")
@allure.story("Карточка сбора")
@allure.title("Проверка отображения основных элементов карточки сбора")
def test_action_card_has_main_elements(driver, base_url):
    main_page = MainPage(driver, base_url)
    action_page = ActionPage(driver, base_url)

    with allure.step("Открыть главную страницу blago.ru"):
        main_page.open()

    with allure.step("Перейти к первой карточке действующего сбора"):
        main_page.open_first_action_card()

    with allure.step("Проверить, что открылась страница сбора"):
        action_page.should_be_opened()

    with allure.step("Проверить, что на странице отображается заголовок сбора"):
        action_page.should_have_title()

    with allure.step("Проверить, что на странице отображается описание сбора"):
        action_page.should_have_description()

    with allure.step("Проверить, что на странице отображается информация о ходе сбора"):
        action_page.should_have_collection_info()

    with allure.step("Проверить, что на странице есть элемент для перехода к пожертвованию"):
        action_page.should_have_donation_button()