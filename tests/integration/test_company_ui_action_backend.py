import re

import allure

from api.api_client import ApiClient
from api.response_utils import (
    extract_objects_list,
    find_company_by_any_identifier,
    find_object_by_any_identifier_recursive,
    response_contains_company_reference,
    get_company_main_info,
    get_object_name,
    to_pretty_json,
)
from pages.companies_page import CompaniesPage
from pages.company_page import CompanyPage
from utils.config import API_BASE_URL, API_COMPANIES_LIST_ENDPOINT


def extract_company_id_from_url(url):
    match = re.search(r"/companies/view/([^/?#]+)", url)

    if not match:
        raise AssertionError(
            f"Could not extract company id from URL: {url}"
        )

    return match.group(1)


@allure.feature("Интеграционные тесты UI + API")
@allure.story("Связь пользовательского действия и backend-данных")
@allure.title("Проверка соответствия пользовательского действия данным backend")
def test_opened_company_card_exists_in_api_data(driver, base_url):
    client = ApiClient(API_BASE_URL)
    companies_page = CompaniesPage(driver, base_url)
    company_page = CompanyPage(driver, base_url)

    with allure.step("Открыть страницу списка организаций"):
        companies_page.open()

    with allure.step("Проверить, что открылась страница списка организаций"):
        companies_page.should_be_opened()

    with allure.step("Выполнить пользовательское действие — открыть первую карточку организации"):
        companies_page.open_first_company_card()

    with allure.step("Проверить, что открылась страница организации"):
        company_page.should_be_opened()

    with allure.step("Получить данные открытой страницы из UI"):
        opened_url = company_page.get_current_url()
        company_id_from_ui = extract_company_id_from_url(opened_url)
        company_title_from_ui = company_page.get_title_text()

        ui_data = {
            "opened_url": opened_url,
            "company_id_from_url": company_id_from_ui,
            "company_title_from_ui": company_title_from_ui,
        }

        allure.attach(
            to_pretty_json(ui_data),
            name="Данные, полученные после действия пользователя в UI",
            attachment_type=allure.attachment_type.JSON,
        )

        allure.attach(
            driver.get_screenshot_as_png(),
            name="Страница организации после перехода из UI",
            attachment_type=allure.attachment_type.PNG,
        )

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

    with allure.step("Проверить наличие открытой организации в backend-данных"):
        found_company = None
        id_key = None
        search_mode = None

        try:
            companies = extract_objects_list(response_json)
            id_key, found_company = find_company_by_any_identifier(
                companies,
                company_id_from_ui,
            )
            search_mode = "search in extracted objects list"
        except AssertionError:
            try:
                id_key, found_company = find_object_by_any_identifier_recursive(
                    response_json,
                    company_id_from_ui,
                )
                search_mode = "recursive search in JSON"
            except AssertionError:
                assert response_contains_company_reference(
                    response.text,
                    company_id_from_ui,
                    company_title_from_ui,
                ), (
                    f"Company with id '{company_id_from_ui}' and title "
                    f"'{company_title_from_ui}' was not found in backend response"
                )
                search_mode = "text reference in backend response"

        backend_data = {
            "search_mode": search_mode,
            "company_id_from_ui": company_id_from_ui,
            "company_title_from_ui": company_title_from_ui,
        }

        if found_company:
            backend_data["id_field"] = id_key
            backend_data["company_from_api"] = get_company_main_info(found_company)

        allure.attach(
            to_pretty_json(backend_data),
            name="Результат поиска организации в backend-данных",
            attachment_type=allure.attachment_type.JSON,
        )

    with allure.step("Проверить соответствие названия организации в UI и API"):
        if found_company:
            _, company_name_from_api = get_object_name(found_company)
            company_page.should_have_company_name(company_name_from_api)
        else:
            assert response_contains_company_reference(
                response.text,
                company_id_from_ui,
                company_title_from_ui,
            )