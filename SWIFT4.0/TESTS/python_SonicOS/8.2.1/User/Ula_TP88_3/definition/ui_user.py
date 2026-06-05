import re
import sys
import argparse
import sys

sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
# sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
print(sys.path)
from runner.settings import logger
# from modules.ui.ui_wrapper_test import Browser
from modules.ui.ui_wrapper import Browser
from runner.utils.assertion import Assertion

import time

class FWPage(Browser):
    def __init__(self, url, user, pwd, failure=False):
        self.url = url
        self.user = user
        self.password = pwd
        self.failure = failure

    def login_ui(self):
        try:
            self.get_browser()
            self.go_to_url(self.url)
            time.sleep(5)
            #Assertion.assert_equal(self.does_page_have_text("The policy set up by your network administrator requires that you authenticate yourself with this firewall before you can have access."), True, "ERR: Policy redirect failed.")
            # if self.does_element_exist('xpath','/html/body/div/div/div[3]/a'):
            if self.does_element_exist('xpath', "//a[text()='Click here to log in']"):
                self.click_element('xpath', "//a[text()='Click here to log in']")
            logger.info("Clicked policy login")
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
            logger.info("Action - Clicking Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(5)

            # verify login failure
            if self.failure:
                if self.does_page_have_text("You have logged in successfully!"):
                    time.sleep(5)
                    # self.click_element("xpath", "/html/body/div/div/div/div[3]/div/div/button")
                    self.click_element("xpath", "//button[normalize-space()='Continue']")
                    logger.info("Action - Clicked Continue")
                    time.sleep(5)
                    Assertion.assert_equal(self.does_page_have_text("Testing 123.."), False, "ERR: URL is accessible.")
                else:
                    Assertion.assert_equal(self.does_page_have_text("You have logged in successfully!"), False, "ERR: Logged in.")
            
            else:
                if self.user == 'admin':
                    self.go_to_url(self.url)
                    time.sleep(5)
                    Assertion.assert_equal(self.does_page_have_text("Testing 123.."), True, "ERR: URL Access Failed.")
                else:
                    Assertion.assert_equal(self.does_page_have_text("You have logged in successfully!"), True, "ERR: Login failed.")
                    time.sleep(5)
                    self.click_element("xpath", "//button[normalize-space()='Continue']")
                    logger.info("Action - Clicked Continue")
                    time.sleep(5)
                    Assertion.assert_equal(self.does_page_have_text("Testing 123.."), True, "ERR: URL Access Failed.")
                    all_handles = self.get_browser_all_handles()
                    self.browser.switch_to.window(self.browser.window_handles[1])
                    self.click_element('xpath', "//a[normalize-space()='Logout']")
                    logger.info("Action - Clicked Log out")
                    time.sleep(5)
                    self.browser.switch_to.window(self.browser.window_handles[0])
                    time.sleep(5)
                    logger.info("window switched")
            
            self.close_browser()
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("ULA login failed")
    
    def verify_direct_resource_access(self):
        try:
            self.get_browser()
            self.go_to_url(self.url)
            time.sleep(5)
            if self.failure:
                Assertion.assert_equal(self.does_page_have_text("Testing 123.."), False, f"ERR: Url({self.url}) Direct Access failed.")
            else:
                Assertion.assert_equal(self.does_page_have_text("Testing 123.."), True, f"ERR: Url({self.url}) Direct Access failed.")
            time.sleep(5)

            self.close_browser()
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("ULA login failed")

    def fw_login(self):
        try:
            self.get_browser()
            self.go_to_url("https://192.168.168.168")
            time.sleep(5)
            self.click_element('xpath','/html/body/div/div/div[3]/a')
            time.sleep(5)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
            logger.info("Action - Clicking Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(5)

            # verify login failure
            if self.failure:
                if self.does_page_have_text("You have logged in successfully!"):
                    time.sleep(5)
                    self.click_element("xpath", "//button[@type='button']")
                    logger.info("Action - Clicked Continue")
                    time.sleep(5)
                    logger.info(f"Accessing URL - {self.url}")
                    self.go_to_url(self.url)
                    time.sleep(5)
                    Assertion.assert_equal(self.does_page_have_text("Testing 123.."), False, "ERR: URL is accessible.")
                    all_handles = self.get_browser_all_handles()
                    self.browser.switch_to.window(self.browser.window_handles[1])
                    # self.click_element('xpath', '/html/body/div/div/div/div[3]/div[1]/div')
                    self.click_element('xpath', "//a[normalize-space()='Logout']")
                    logger.info("Action - Clicked Log out")
                    time.sleep(5)
                    self.browser.switch_to.window(self.browser.window_handles[0])
                    time.sleep(5)
                    logger.info("window switched")
            
            self.close_browser()
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("login failed")



def str_to_bool(value):
    if value == 'False':
        return False
    else:
        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Login group service by UI')
    parser.add_argument('-url', type=str, dest='url', required=True, help='http server url')
    parser.add_argument('-user', type=str, dest='user', default="username", help='user to login group service')
    parser.add_argument('-pwd', type=str, dest='pwd', default="password", help='pwd to login group service')
    parser.add_argument('-failure', type=str_to_bool, dest='failure', default=False, help='Expected Failure')
    parser.add_argument('-direct', type=str_to_bool, dest='direct', default=False, help='Direct Access')

    args = parser.parse_args()
    uiobj = FWPage(args.url, args.user, args.pwd, args.failure)
    if(args.direct):
        rc = uiobj.verify_direct_resource_access()
    else:
        rc = uiobj.login_ui()
    # rc = uiobj.login_ui()
