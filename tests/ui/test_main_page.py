import allure

from pages.main_page import MainPage


@allure.feature("UI-тесты")
@allure.story("Главная страница")
@allure.title("Проверка доступности главной страницы и корректности заголовка")
def test_open_main_page(driver, base_url):
    main_page = MainPage(driver, base_url)

    with allure.step("Открыть главную страницу blago.ru"):
        main_page.open()

    with allure.step("Проверить, что открыта страница домена blago.ru"):
        main_page.should_be_opened()

    with allure.step("Проверить, что заголовок страницы содержит значение 'Благо'"):
        main_page.should_have_correct_title()