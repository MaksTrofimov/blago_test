import allure

from api.api_client import ApiClient
from api.response_utils import (
    extract_objects_list,
    get_object_identifier,
    get_object_name,
    get_company_main_info,
    to_pretty_json,
)
from pages.company_page import CompanyPage
from utils.config import API_BASE_URL, API_COMPANIES_LIST_ENDPOINT


@allure.feature("Интеграционные тесты UI + API")
@allure.story("Соответствие данных организации")
@allure.title("Проверка соответствия данных организации в UI и API")
def test_company_name_in_ui_matches_api(driver, base_url):
    client = ApiClient(API_BASE_URL)
    company_page = CompanyPage(driver, base_url)

    with allure.step("Отправить GET-запрос для получения списка организаций"):
        response = client.get(API_COMPANIES_LIST_ENDPOINT)

    with allure.step("Проверить успешный HTTP-статус ответа"):
        assert response.status_code == 200, (
            f"Expected status code 200, but got {response.status_code}. "
            f"Response text: {response.text[:300]}"
        )

    with allure.step("Преобразовать ответ сервера в JSON"):
        try:
            response_json = response.json()
        except ValueError:
            raise AssertionError(
                f"Response is not valid JSON. Response text: {response.text[:300]}"
            )

    with allure.step("Извлечь список организаций из JSON-ответа"):
        companies = extract_objects_list(response_json)
        assert len(companies) > 0, "Companies list should not be empty"

    with allure.step("Получить идентификатор и название первой организации"):
        company = companies[0]
        id_key, company_id = get_object_identifier(company)
        _, company_name = get_object_name(company)

        allure.attach(
            to_pretty_json(get_company_main_info(company)),
            name=f"Данные организации из API ({id_key}={company_id})",
            attachment_type=allure.attachment_type.JSON,
        )

    with allure.step("Открыть страницу организации в браузере по ID из API"):
        company_page.open_by_id(company_id)

    with allure.step("Проверить, что открылась страница организации"):
        company_page.should_be_opened()

    with allure.step("Проверить соответствие названия организации в UI и API"):
        company_page.should_have_company_name(company_name)

    with allure.step("Добавить скриншот страницы организации в Allure-отчет"):
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Страница организации в UI",
            attachment_type=allure.attachment_type.PNG,
        )