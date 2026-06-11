import pytest
import allure

from api.api_client import ApiClient
from api.response_utils import (
    extract_objects_list,
    get_object_identifier,
    find_object_by_identifier,
    get_identifier_values,
    generate_non_existing_identifier,
    to_pretty_json,
)
from utils.config import API_BASE_URL, API_COMPANIES_LIST_ENDPOINT


@allure.feature("API-тесты")
@allure.story("Объект организации")
@allure.title("Негативный API-тест с несуществующим ID")
def test_non_existing_company_id_is_not_found():
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

    with allure.step("Определить поле идентификатора объекта"):
        first_company = companies[0]
        id_key, _ = get_object_identifier(first_company)

    with allure.step("Сформировать несуществующий идентификатор"):
        existing_ids = get_identifier_values(companies, id_key)
        non_existing_id = generate_non_existing_identifier(existing_ids)

        diagnostic_data = {
            "id_field": id_key,
            "non_existing_id": non_existing_id,
            "objects_count": len(companies),
            "sample_existing_ids": list(existing_ids)[:5],
        }

        allure.attach(
            to_pretty_json(diagnostic_data),
            name="Диагностика несуществующего ID",
            attachment_type=allure.attachment_type.JSON,
        )

    with allure.step("Проверить, что объект с несуществующим ID не найден"):
        with pytest.raises(AssertionError) as error_info:
            find_object_by_identifier(
                companies,
                id_key=id_key,
                expected_id=non_existing_id,
            )

        result_data = {
            "result": "Object was not found as expected",
            "error_message": str(error_info.value),
        }

        allure.attach(
            to_pretty_json(result_data),
            name="Результат поиска несуществующего ID",
            attachment_type=allure.attachment_type.JSON,
        )