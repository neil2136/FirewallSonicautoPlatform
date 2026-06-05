import re
import sys
import argparse
import sys
import time

sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
# sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
# print(sys.path)
from runner.settings import logger
from modules.ui.ui_wrapper import Browser
from runner.utils.assertion import Assertion

class AUPLogin(Browser):
    def __init__(self, url, user, pwd):
        self.url = url
        self.user = user
        self.password = pwd

    def verify_aup(self):
        try:
            self.get_browser()
            self.go_to_url(self.url)
            time.sleep(15)
            flag = True if self.does_page_have_text("Acceptable User Policy") else False
            Assertion.assert_equal(flag, True, "ERR: Failed to verify AUP.")
            logger.info("Verified acceptable user policy")

            self.click_element("xpath", "//button[@type='button']")
            time.sleep(5)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
            logger.info("Action - Clicking Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(5)
            Assertion.assert_equal(self.does_page_have_text("You have logged in successfully!"), True, "ERR: Failed to Login.")

            self.close_browser()
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("login failed")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Login group service by UI')
    parser.add_argument('-url', type=str, dest='url', required=True, help='http server url')
    parser.add_argument('-user', type=str, dest='user', default="username", help='user to login group service')
    parser.add_argument('-pwd', type=str, dest='pwd', default="password", help='pwd to login group service')

    args = parser.parse_args()
    uiobj = AUPLogin(args.url, args.user, args.pwd)
    rc = uiobj.verify_aup()
