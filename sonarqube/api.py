import logging
import requests


class SonarQubeApi:

    def __init__(self, base_url, token):
        self._token = token
        self._base_url = base_url
        self._session = requests.Session()
        self._session.auth = token, ''

    def get_rules_by_language(self, language):
        api = "rules/search"
        params = {"ps": "500", "languages": language}
        return self.request(api, params, 200, "Cannot retrieve list of rules")

    def get_rules_by_tags(self, tags):
        api = "rules/search"
        params = {"ps": "500", "tags": tags}
        return self.request(api, params, 200, "Cannot retrieve list of rules")

    def request(self, api, params, expected_response_status_code, error_message, verb="get"):
        response = getattr(self._session, verb)(self._base_url + "/api/" + api, params=params)

        if response.status_code != expected_response_status_code:
            logging.error(response)
            logging.error(response.text)
            raise ConnectionError(error_message)

        return response
