import re
import sys
import argparse
import sys
import os
import json
sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
print(sys.path)
from runner.settings import logger
from modules.ui.ui_wrapper import Browser

from runner.utils.assertion import Assertion

import time


class FWPage(Browser):
    def __init__(self, url, user, pwd):
        self.url = url
        self.user = user
        self.password = pwd

    def login_ui(self):
        try:
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
            logger.info("Action - Clicked Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(10)
            logger.info("Login Test Flag.")
            self.click_element('xpath', '/html/body/div/div/div/div[3]/div/div/button')
            logger.info("CLicked on continue page")
            time.sleep(10)
            self.click_element('xpath', '/html/body/div/div/div/div[3]/div/div/button')
            logger.info("CLicked on continue page")
            time.sleep(10)
            self.click_element('/html/body/div/div/div/div[3]/div[3]/div/button')
            logger.info("CLicked on Manage page")
            time.sleep(10)
             
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to launch bookmark")

    # def login_external_auth_server(self):
    

if __name__ == '__main__':
    # uiobj = FWPage('https://[2001:db1::1093]', 'test', 'test')
    # rc = uiobj.login_external_auth_server()

    parser = argparse.ArgumentParser(description='Login guest service by UI')
    parser.add_argument('-url', type=str, dest='url', required=True, help='http server url')
    parser.add_argument('-user', type=str, dest='user', required=True, help='user to login guest service')
    parser.add_argument('-pwd', type=str, dest='pwd', required=True, help='pwd to login guest service')
    args = parser.parse_args()
    uiobj = FWPage(args.url, args.user, args.pwd)
    rc = uiobj.login_ui()
    print(rc)

    # uiobj = FWPage('https://[2001:db1::1093]', 'guest', 'password')
    # rc = uiobj.login_ui()
