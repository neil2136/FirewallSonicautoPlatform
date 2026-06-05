import re
import sys
import argparse
import sys
import os
from optparse import OptionParser

sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
from networkdevice import Host
#sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
print(sys.path)
from runner.settings import logger
from modules.ui.ui_wrapper import Browser
from runner.utils.assertion import Assertion
import time
import json


class FWPage(Browser):
    def __init__(self, url, user, pwd):
        self.url = url
        self.user = user
        self.password = pwd

    def login_fw_ui(self):
        try:
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("start logging...")
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
            logger.info("Action - Clicked Login")
            # self.wait_for_element_to_be_visible('class', 'sw-login__trigger')
            self.click_element('class', 'sw-login__trigger')
            time.sleep(10)
            logger.info(f"Login fw successful.")
            return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def get_a_page_source(self):
        self.get_browser()
        self.go_to_url(self.turl)
        logger.info("Logging in to wan server via ui")
        return self.get_page_source()

    def close_browser(self):
        self.browser.close()


# uiobj = FWPage('https://12.12.1.50', 'test', 'test')
# rc = uiobj.login_external_auth_server()
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Login guest service by UI')
    parser.add_argument('-url', type=str, dest='url', required=True, help='fw https login url')
    parser.add_argument('-user', type=str, dest='user', required=True, help='user to login guest service')
    parser.add_argument('-pwd', type=str, dest='pwd', required=True, help='pwd to login guest service')
    args = parser.parse_args()
    print(args.url, args.user, args.pwd)
    ui_obj = FWPage(args.url, args.user, args.pwd)
    res = ui_obj.login_fw_ui()
    print(f'login fw result is {res}')


