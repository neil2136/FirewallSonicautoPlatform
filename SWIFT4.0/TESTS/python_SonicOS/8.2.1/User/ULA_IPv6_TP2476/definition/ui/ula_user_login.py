import re
import sys
import argparse
import sys

sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
from runner.settings import logger
from modules.ui.ui_wrapper import Browser
from runner.utils.assertion import Assertion
import time

class ULALogin(Browser):
    def __init__(self, url, user, pwd, attempt=0, failure=False):
        self.url = url
        self.user = user
        self.password = pwd
        self.attempt = attempt
        self.failure = failure

    def login_ui(self):
        try:
            self.get_browser()
            self.go_to_url(self.url)
            for i in range(self.attempt):
                logger.info("Configure - Setting username")
                self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
                logger.info("Configure - Setting password")
                self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', "wrongpassword")
                self.click_element('class', 'sw-login__trigger')
                logger.info("Action - Clicked Login")
                time.sleep(10)

            # verify login failure
            if self.failure:
                logger.info("Configure - Setting username")
                self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
                logger.info("Configure - Setting password")
                self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
                self.click_element('class', 'sw-login__trigger')
                logger.info("Action - Clicked Login")
                time.sleep(5)
                Assertion.assert_equal(self.does_page_have_text("You have logged in successfully!"), False, "ERR: Logged in.")
            else:
                # verify login success
                logger.info("Configure - Setting username")
                self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
                logger.info("Configure - Setting password")
                self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
                self.click_element('class', 'sw-login__trigger')
                logger.info("Action - Clicked Login")
                time.sleep(5)
                Assertion.assert_equal(self.does_page_have_text("You have logged in successfully!"), True, "ERR: Login failed.")
            
            self.close_browser()

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("ULA login failed")

def str_to_bool(value):
    if value == 'False':
        return False
    else:
        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ULA login by UI')
    parser.add_argument('-url', type=str, dest='url', required=True, help='http server url')
    parser.add_argument('-user', type=str, dest='user', required=True, help='username to login')
    parser.add_argument('-pwd', type=str, dest='pwd', required=True, help='pwd to login')
    parser.add_argument('-attempt', type=str, dest='attempt', required=True, help='Wrong password attempts')
    parser.add_argument('-failure', type=str_to_bool, dest='failure', required=True, help='Expected Failure')
    
    args = parser.parse_args()
        
    uiobj = ULALogin(args.url, args.user, args.pwd, int(args.attempt),args.failure)
    rc = uiobj.login_ui()
