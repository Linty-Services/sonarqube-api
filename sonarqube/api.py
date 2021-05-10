import logging
import requests


class SonarQubeApi:

    def __init__(self, base_url, token):
        self._token = token
        self._base_url = base_url
        self._session = requests.Session()
        self._session.auth = token, ''

    def check_if_project_exists(self, project_key):
        response = self.request("projects/search", {"projects": project_key}, 200,
                                f"ERROR: Cannot search for '{project_key}' project")
        return len(response.json()["components"]) != 0

    def create_project(self, project_key):
        self.request("projects/create", {"project": project_key, "name": project_key}, 200,
                     f"Cannot create '{project_key}' project", verb="post")
        logging.info(f"'{project_key}' project created")

    def update_project_visibility(self, project_key, visibility):
        self.request("projects/update_visibility", {"project": project_key, "visibility": visibility}, 204,
                     f"Cannot update visibility '{visibility}' on '{project_key}' project", verb="post")
        logging.info(f"Visibility set to '{visibility}' on '{project_key}' project")

    def grant_permission_on_project_to_user(self, permissions, project_key, username):
        for permission in permissions:
            self.request(
                "permissions/add_user", {"projectKey": project_key, "login": username, "permission": permission},
                204, f"Cannot grant '{permission}' permission on '{project_key}' project for '{username}' user",
                verb="post")
            logging.info(f"'{permission}' permission granted on '{project_key}' project for '{username}' user")

    def set_quality_profile_on_project(self, project_key, language, quality_profile):
        self.request("qualityprofiles/add_project",
                     {"project": project_key, "language": language, "qualityProfile": quality_profile}, 204,
                     f"Cannot set quality profile '{language}/{quality_profile}' on '{project_key}' project",
                     verb="post")
        logging.info(f"Quality profile set to '{language}/{quality_profile}' on '{project_key}' project")

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
