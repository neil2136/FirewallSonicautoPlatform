import re
import sys
import argparse
import sys

sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
#sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
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
            time.sleep(4)
            #Assertion.assert_equal(self.does_page_have_text("The policy set up by your network administrator requires that you authenticate yourself with this firewall before you can have access."), True, "ERR: Policy redirect failed.")
            if self.does_element_exist('xpath', "//a[text()='Click here to log in']"):
                self.click_element('xpath', "//a[text()='Click here to log in']")
            logger.info("Clicked policy login")
            time.sleep(3)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
            logger.info("Action - Clicked Login")
            # self.wait_for_element_to_be_visible('class', 'sw-login__trigger')
            self.click_element('class', 'sw-login__trigger')
            time.sleep(10)
            logger.info("Login Test Flag.")
            # return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Login group service by UI')
    parser.add_argument('-url', type=str, dest='url', required=True, help='http server url')
    parser.add_argument('-user', type=str, dest='user', required=True, help='user to login group service')
    parser.add_argument('-pwd', type=str, dest='pwd', required=True, help='pwd to login group service')
    args = parser.parse_args()
    uiobj = FWPage(args.url, args.user, args.pwd)
    rc = uiobj.login_ui()
    # rc = uiobj.login_ui()
