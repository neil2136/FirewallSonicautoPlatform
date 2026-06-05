import warnings
import requests
import urllib3

from inputs.request_urls import *
from inputs.constants import *
from pytest_resources.common_require import *

# Suppress only the single InsecureRequestWarning from urllib3 needed to handle this issue
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore', message="Unverified HTTPS request")
warnings.simplefilter("ignore", ResourceWarning)
headers = {'content-type': 'application/json'}


class FirewallAPI:
    def __init__(self):
        self.test = None

    # API Login method
    def api_login(self):
        auth_json = {"override": True}
        payload = json.dumps(auth_json)
        urllib3.disable_warnings()
        resp = requests.post(url=auth_url, auth=(fw_username, fw_password), data=payload, headers=headers, verify=False)
        response = resp.content.decode('utf-8')
        logger.info("Login response after decode:\r\n{}".format(response))

    # API GET method
    def api_get(self, request_url, params=None):
        self.api_login()
        urllib3.disable_warnings()
        response = requests.get(url=request_url, params=params, verify=False)
        response_code = response.status_code
        response_content = response.content.decode('utf-8')
        logger.info("GET response after decode:\r\n{}".format(response_content))
        Assertion.assert_equal(response_code, 200, "Error: GET request failed...")
        get_response = json.loads(response_content)
        return get_response

    # API POST method
    def api_post(self, request_url, params=None, data=None):
        urllib3.disable_warnings()
        response = requests.post(url=request_url, params=params, data=data, verify=False)
        response_code = response.status_code
        response_content = response.content.decode('utf-8')
        logger.info("POST response after decode:\r\n{}".format(response_content))
        Assertion.assert_equal(response_code, 200, "Error: POST request failed...")
        post_response = json.loads(response_content)
        return post_response

    # API PUT method
    def api_put(self, request_url, params=None, data=None):
        urllib3.disable_warnings()
        response = requests.put(url=request_url, params=params, data=data, verify=False)
        response_code = response.status_code
        response_content = response.content.decode('utf-8')
        logger.info("PUT response after decode:\r\n{}".format(response_content))
        Assertion.assert_equal(response_code, 200, "Error: PUT request failed...")
        put_response = json.loads(response_content)
        return put_response

    # API Post Pending method
    def api_post_pending(self):
        urllib3.disable_warnings()
        response = requests.post(url=config_pending_url, headers=headers, verify=False)
        response_code = response.status_code
        response_content = response.content.decode('utf-8')
        logger.info("POST response after decode:\r\n{}".format(response_content))
        Assertion.assert_equal(response_code, 200, "Error: Apply pending changes failed...")
        pending_response = json.loads(response_content)
        return pending_response

    # API Logout
    def api_logout(self):
        urllib3.disable_warnings()
        resp = requests.delete(url=auth_url, headers=headers, verify=False)
        response = resp.content.decode('utf-8')
        logger.info("Logout response after decode:\r\n{}".format(response))

