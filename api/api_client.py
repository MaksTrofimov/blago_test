import time

import requests
from requests.exceptions import RequestException, ReadTimeout, ConnectionError


class ApiClient:
    DEFAULT_TIMEOUT = 30
    DEFAULT_RETRIES = 3
    RETRY_DELAY_SECONDS = 2

    DEFAULT_HEADERS = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        ),
    }

    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)

    def get(self, endpoint, params=None, headers=None):
        url = f"{self.base_url}{endpoint}"

        request_headers = dict(self.DEFAULT_HEADERS)
        if headers:
            request_headers.update(headers)

        last_error = None

        for attempt in range(1, self.DEFAULT_RETRIES + 1):
            try:
                return self.session.get(
                    url,
                    params=params,
                    headers=request_headers,
                    timeout=self.DEFAULT_TIMEOUT,
                )
            except (ReadTimeout, ConnectionError) as error:
                last_error = error

                if attempt < self.DEFAULT_RETRIES:
                    time.sleep(self.RETRY_DELAY_SECONDS)
                    continue

                raise
            except RequestException:
                raise

        raise last_error