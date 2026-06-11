import allure

from api.api_client import ApiClient
from api.response_utils import (
    extract_objects_list,
    get_object_identifier,
    find_object_by_identifier,
    get_object_name,
    get_company_main_info,
    to_pretty_json,
)
from utils.config import API_BASE_URL, API_COMPANIES_LIST_ENDPOINT


@allure.feature("API-тесты")
@allure.story("Объект организации")
@allure.title("Проверка получения одного объекта по идентификатору")
def test_get_company_by_id():
    client = ApiClient(API_BASE_URL)

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

    with allure.step("Проверить, что список организаций не пустой"):
        assert len(companies) > 0, "Companies list should not be empty"

    with allure.step("Получить идентификатор первого объекта"):
        first_company = companies[0]
        id_key, company_id = get_object_identifier(first_company)

    with allure.step("Найти объект по полученному идентификатору"):
        found_company = find_object_by_identifier(
            companies,
            id_key=id_key,
            expected_id=company_id,
        )

    with allure.step("Добавить основную информацию об организации в Allure-отчет"):
        main_info = get_company_main_info(found_company)

        allure.attach(
            to_pretty_json(main_info),
            name=f"Основная информация об организации с {id_key}={company_id}",
            attachment_type=allure.attachment_type.JSON,
        )

    with allure.step("Проверить, что найденный объект содержит идентификатор"):
        assert str(found_company.get(id_key)) == str(company_id), (
            f"Expected {id_key}='{company_id}', "
            f"but got '{found_company.get(id_key)}'"
        )

    with allure.step("Проверить, что найденный объект содержит название"):
        name_key, company_name = get_object_name(found_company)
        assert company_name, (
            f"Expected non-empty company name in field '{name_key}'"
        )