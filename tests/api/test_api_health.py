import allure

from api.api_client import ApiClient
from api.response_utils import to_pretty_json
from utils.config import API_BASE_URL, API_HEALTH_ENDPOINT


@allure.feature("API-тесты")
@allure.story("Доступность API")
@allure.title("Проверка доступности API и корректности JSON-ответа")
def test_api_is_available_and_returns_json():
    client = ApiClient(API_BASE_URL)

    with allure.step("Отправить GET-запрос к API endpoint"):
        response = client.get(API_HEALTH_ENDPOINT)

    with allure.step("Проверить, что сервер вернул успешный HTTP-статус"):
        assert response.status_code == 200, (
            f"Expected status code 200, but got {response.status_code}. "
            f"Response text: {response.text[:300]}"
        )

    with allure.step("Проверить, что ответ сервера является корректным JSON"):
        try:
            response_json = response.json()
        except ValueError:
            raise AssertionError(
                f"Response is not valid JSON. Response text: {response.text[:300]}"
            )

    with allure.step("Добавить JSON-ответ в Allure-отчет"):
        allure.attach(
            to_pretty_json(response_json),
            name="JSON-ответ API",
            attachment_type=allure.attachment_type.JSON,
        )

    with allure.step("Проверить, что JSON-ответ имеет допустимую структуру верхнего уровня"):
        assert isinstance(response_json, (dict, list)), (
            f"Expected JSON object or array, but got {type(response_json)}"
        )