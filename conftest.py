import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from utils.config import BASE_URL


def pytest_addoption(parser):
    parser.addoption(
        "--keep-browser",
        action="store_true",
        default=False,
        help="Keep browser open after test until Enter is pressed"
    )


@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    yield driver

    if request.config.getoption("--keep-browser"):
        input("Тест завершен. Нажмите Enter, чтобы закрыть браузер...")

    driver.quit()


@pytest.fixture
def base_url():
    return BASE_URL