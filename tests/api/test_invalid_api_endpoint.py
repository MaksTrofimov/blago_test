import allure

from api.api_client import ApiClient
from api.response_utils import to_pretty_json
from utils.config import API_BASE_URL, API_INVALID_ENDPOINT


@allure.feature("API-тесты")
@allure.story("Некорректный API-запрос")
@allure.title("Негативный API-тест с несуществующим endpoint")
def test_invalid_api_endpoint_returns_client_error():
    client = ApiClient(API_BASE_URL)

    with allure.step("Отправить GET-запрос к несуществующему endpoint"):
        response = client.get(API_INVALID_ENDPOINT)

    with allure.step("Добавить информацию об ошибочном запросе в Allure-отчет"):
        diagnostic_data = {
            "request_endpoint": API_INVALID_ENDPOINT,
            "status_code": response.status_code,
            "response_text": response.text[:1000],
        }

        allure.attach(
            to_pretty_json(diagnostic_data),
            name="Несуществующий endpoint и ответ сервера",
            attachment_type=allure.attachment_type.JSON,
        )

    with allure.step("Проверить, что сервер вернул ошибку клиента"):
        assert 400 <= response.status_code < 500, (
            f"Expected 4xx status code, but got {response.status_code}. "
            f"Response text: {response.text[:300]}"
        )

    with allure.step("Проверить, что сервер не вернул внутреннюю ошибку"):
        assert response.status_code < 500, (
            f"Server returned internal error {response.status_code}. "
            f"Response text: {response.text[:300]}"
        )