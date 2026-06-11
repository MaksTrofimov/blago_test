import allure

from api.api_client import ApiClient
from api.response_utils import (
    extract_objects_list,
    get_companies_short_preview,
    to_pretty_json,
)
from utils.config import API_BASE_URL, API_COMPANIES_LIST_ENDPOINT


@allure.feature("API-тесты")
@allure.story("Список организаций")
@allure.title("Проверка получения списка объектов через API")
def test_get_companies_list():
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

    with allure.step("Извлечь список объектов из JSON-ответа"):
        companies = extract_objects_list(response_json)

    with allure.step("Добавить краткий список организаций в Allure-отчет"):
        companies_preview = get_companies_short_preview(companies, limit=10)

        allure.attach(
            to_pretty_json(companies_preview),
            name="Краткий список организаций: ID и название",
            attachment_type=allure.attachment_type.JSON,
        )

    with allure.step("Проверить, что список организаций не пустой"):
        assert len(companies) > 0, "Companies list should not be empty"

    with allure.step("Проверить, что элементы списка являются объектами"):
        assert all(isinstance(company, dict) for company in companies), (
            "Each company item should be a JSON object"
        )