import requests
from random import randint
from urllib.parse import urlencode


class ScrapeOpsFakeBrowserHeaderAgentMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.scrapeops_api_key = settings.get("SCRAPEOPS_API_KEY")
        self.scrapeops_endpoint = settings.get(
            "SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT",
            "http://headers.scrapeops.io/v1/user-agents?",
        )
        self.scrapeops_fake_browser_headers_active = settings.get(
            "SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED", True
        )
        self.scrapeops_num_results = settings.get("SCRAPEOPS_NUM_RESULTS")
        self.headers_list = []
        self._get_browser_headers_list()
        self._scrapeops_fake_browser_headers_enabled()

    def _get_browser_headers_list(self):
        payload = {"api_key": self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload["num_results"] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.browser_headers_list: list = json_response.get("result", [])

    def _get_random_browser_header(self):
        random_index = randint(0, len(self.browser_headers_list) - 1)
        return self.browser_headers_list[random_index]

    def _scrapeops_fake_browser_headers_enabled(self):
        if (
            self.scrapeops_api_key is None
            or self.scrapeops_api_key == ""
            or not self.scrapeops_fake_browser_headers_active
        ):
            self.scrapeops_fake_browser_headers_active = False
        else:
            self.scrapeops_fake_browser_headers_active = True

    def process_request(self, request, spider):
        random_browser_header: dict = self._get_random_browser_header()

        header_keys = [
            "User-Agent",
            "Accept",
            "Accept-Language",
            "Accept-Encoding",
            "Referer",
            "Sec-GPC",
            "Connection",
            "Upgrade-Insecure-Requests",
            "Sec-Fetch-Dest",
            "Sec-Fetch-Mode",
            "Sec-Fetch-Site",
            "If-Modified-Since",
            "If-None-Match",
            "Priority",
        ]

        for key in header_keys:
            if key in random_browser_header.items():
                request.header[key] = random_browser_header[key]

        # print("************** New HEADER *****************")
        # print(request.headers)
