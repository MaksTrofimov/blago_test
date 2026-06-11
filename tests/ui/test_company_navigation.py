import allure

from pages.main_page import MainPage
from pages.company_page import CompanyPage


@allure.feature("UI-тесты")
@allure.story("Переходы с главной страницы")
@allure.title("Проверка перехода с главной страницы к карточке фонда")
def test_open_company_card_from_main_page(driver, base_url):
    main_page = MainPage(driver, base_url)
    company_page = CompanyPage(driver, base_url)

    with allure.step("Открыть главную страницу blago.ru"):
        main_page.open()

    with allure.step("Перейти к первой карточке фонда из блока 'Вы можете помочь'"):
        main_page.open_first_company_card()

    with allure.step("Проверить, что открылась страница фонда"):
        company_page.should_be_opened()

    with allure.step("Проверить, что на странице фонда отображается заголовок"):
        company_page.should_have_title()