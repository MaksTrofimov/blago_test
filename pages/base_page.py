from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    DEFAULT_TIMEOUT = 10

    def __init__(self, driver, base_url=None):
        self.driver = driver
        self.base_url = base_url

    def open(self, url):
        self.driver.get(url)

    def open_path(self, path=""):
        if not self.base_url:
            raise ValueError("Base URL is not set")
        self.driver.get(f"{self.base_url}{path}")

    def get_title(self):
        return self.driver.title

    def title_contains(self, text):
        return text in self.driver.title

    def get_current_url(self):
        return self.driver.current_url

    def wait_for_visible(self, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def click(self, locator):
        element = self.wait_for_clickable(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element
        )
        element.click()

    def current_url_contains(self, text):
        return text in self.get_current_url()

    def wait_for_url_change(self, old_url, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.url_changes(old_url)
        )

    def is_element_visible(self, locator):
        elements = self.driver.find_elements(*locator)
        return any(element.is_displayed() for element in elements)