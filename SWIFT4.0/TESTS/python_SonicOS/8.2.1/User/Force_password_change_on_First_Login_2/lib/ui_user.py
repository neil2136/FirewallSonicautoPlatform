import requests
from requests.auth import HTTPBasicAuth
from requests_toolbelt.adapters import source
import json
import time
import urllib.request
import ssl
from base64 import b64encode
import urllib3
from collections import OrderedDict
from runner.settings import Params, logger


class FWlogin:
    def __init__(self, url, user, pwd):
        self.url = url
        self.user = user
        self.password = pwd
        urllib3.disable_warnings()
        
    def user_login(self,url,user, pwd):
        url = f"https://{url}/api/sonicos/auth"
        payload = {
            "domain": "LocalDomain",
            "override": False,
            "snwl": True
        }
        payload_json = json.dumps(payload).encode('utf-8')
        auth = b64encode(f"{user}:{pwd}".encode()).decode()
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Basic {auth}'
        }
        context = ssl._create_unverified_context()
        req = urllib.request.Request(url, data=payload_json, headers=headers)

        try:
            with urllib.request.urlopen(req, context=context) as response:
                response_data = response.read()
                response_status = response.getcode()
                logger.info(response_status)
                logger.info(response_data)
                if response_status == 200:
                    resp = json.loads(response_data)
                    bearer_token = resp['status']['info'][0]['bearer_token']
                    return True,bearer_token
                elif response_status == 401:
                    # response_status = response.getcode()
                    # logger.info(response_status)
                    logger.info(response_data)
                    logger.info("Unauthorized access (401). Check credentials or permissions.")
                    return False, None
                else:
                    logger.info(f"Login failed. Status code: {response_status}")
                    return False, None

        except urllib.error.HTTPError as e:
        # Handle HTTPError specifically
            response_status = e.code
            if e.fp:
                response_data = e.fp.read()
                logger.error(f"HTTP Error: {response_status} - {e.reason}")
                if response_status == 401:
                    logger.error(f"Response Data: {response_data.decode('utf-8')}")
                    return response_data.decode('utf-8')
                else:
                    return response_status, None
            else:
                logger.error(f"HTTP Error: {response_status} - {e.reason}")
                return response_status, None

        except urllib.error.URLError as e:
        # Handle URL errors (e.g., network problems)
            logger.error(f"URL Error: {e.reason}")
            return None, None
        
    





