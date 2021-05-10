import logging
import urllib.parse

from sonarqube.api import SonarQubeApi


class LintyCloudApi:

    def __init__(self, token):
        self._sonarqube_api = SonarQubeApi("https://sonar.linty-services.com", token)

    def provision_project(self, project_key, visibility):
        if self._sonarqube_api.check_if_project_exists(project_key):
            raise Exception(f"Cannot create '{project_key}' project as it already exists")
        else:
            if visibility == "private":
                username = "scanner"
            elif visibility == "public":
                username = "scanner-for-public-repositories"
            else:
                raise Exception(f"Unknown visibility '{visibility}': Only 'public' or 'private' is allowed.")

            self._sonarqube_api.create_project(project_key)
            self._sonarqube_api.update_project_visibility(project_key, visibility)
            self._sonarqube_api.grant_permission_on_project_to_user(["scan"], project_key, username)
            self._sonarqube_api.set_quality_profile_on_project(project_key, "vhdl", "VHDL all rules")
            project_url = f"{self._sonarqube_api._base_url}/dashboard?id={urllib.parse.quote(project_key)}"
            logging.info(f"Project provisioned at {project_url}")
