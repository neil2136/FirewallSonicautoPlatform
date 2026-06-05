import urllib3
from collections import OrderedDict
import json
import requests
from runner.settings import logger

class UserLoginApi:
    urllib3.disable_warnings()

    def __init__(self, headers, ip, username, password):
        # if headers is None:
        self.headers = OrderedDict([('Accept', 'application/json'),
                                    ('Content-Type', 'application/json'),
                                    ('Accept-Encoding', 'application/json'),
                                    ('charset', 'UTF-8')])
        self.ip = ip
        self.username = username
        self.password = password
        self.fwurl = 'https://' + self.ip + '/'
        self.loginapi = self.fwurl + 'api/sonicos/auth'
        self.startmgmtapi = self.fwurl + 'api/sonicos/start-management'
        self.configmodeapi = self.fwurl + 'api/sonicos/config-mode'
        # self.pendingapi = self.fwurl + 'api/sonicos/config/pending'
        # self.guestuserapi = self.fwurl + 'api/sonicos/user/guest/users'
        # self.localuserapi = self.fwurl + 'user/local/users'
        self.nonconfigapi = self.fwurl + 'api/sonicos/non-config-mode'

        self.initial_user_guest_account_json = {
            "user": {
                "guest": {
                    "user": [
                        {
                            "name": "None",
                            "password": "None",
                            "bearer_token": "None"

                        }]}}}

    def local_user_login(self):
        payload = {'override': False, 'snwl': True}
        payload = json.dumps(payload)
        urllib3.disable_warnings()
        resp = requests.post(self.loginapi, auth=(self.username, self.password), data=payload, headers=self.headers,
                             verify=False)
        response = resp.content.decode('utf-8')
        logger.info("Login response after decode:\r\n{}".format(response))
        try:
            login_response = json.loads(response)
            logger.info(login_response)
            if login_response['status']['success']:
                logger.info('Successfully login sonincos')
                for token in login_response['status']['info']:
                    if token['bearer_token']:
                        bearer_token = login_response['status']['info'][0]['bearer_token']
                        # post managment button in start managment page
                        self.headers = OrderedDict([('Accept', 'application/json'),
                                                    ('Content-Type', 'application/json'),
                                                    ('Accept-Encoding', 'application/json'),
                                                    ('charset', 'UTF-8'),
                                                    ('Authorization', 'Bearer ' + bearer_token)])
                        startmgmtresponse = requests.post(self.startmgmtapi, headers=self.headers, data={},
                                                          verify=False)
                        if startmgmtresponse.status_code == 200:
                            logger.info('Successfully post start managment.')
                        else:
                            logger.error('Post start managment failed. response json: ' + startmgmtresponse.json())
                            return False, False
                        # post config mode from start managment page to index page
                        configmoderesponse = requests.post(self.configmodeapi, headers=self.headers, data={},
                                                           verify=False)
                        status_code = configmoderesponse.status_code
                        resp = configmoderesponse.content.decode('utf-8')
                        return_msg = json.loads(resp)
                        logger.info(return_msg)
                        return_value = return_msg['status']['success']
                        if configmoderesponse.status_code == 200:
                            logger.info('Successfully post config mode in start managment page.')
                        elif configmoderesponse.status_code != 200 and return_msg['status']['info'][0][
                            'config_mode'] == 'No' or return_msg['status']['info'][0][
                            'message'] == 'Cannot change to config mode':
                            logger.info('non config mode, re-login')
                            resp = requests.post(self.nonconfigapi, headers=self.headers, verify=False)
                            status_code = resp.status_code
                            resp1 = resp.content.decode('utf-8')
                            return_msg = json.loads(resp1)
                            logger.info(return_msg)
                            return_value = return_msg['status']['success']
                        else:
                            logger.error('Post config mode failed. response json: ' + configmoderesponse.json())
                            return False, False
                        return True, bearer_token
                    else:
                        logger.error('Get the bearer_token failed !')
                        return False, False
            else:
                logger.info("Login error\nResponse is " + login_response['status'])
                return "Login error\nResponse is " + login_response['status'], False
        except:
            logger.error('Limit user Login failed !')
            return f"Login error\nResponse is {login_response['status']['info'][0]['message']}" , False