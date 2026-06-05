import re
import sys
import argparse
import sys
import time
import random

sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
print(sys.path)
from runner.settings import logger
from modules.ui.ui_wrapper import Browser
from runner.utils.assertion import Assertion


class VOPage(Browser):
    def __init__(self, url, user, pwd):
        self.url = url
        self.user = user
        self.password = pwd
        self.new_password = "newpassword"
    
    def virtual_office_login(self):
        try:
            logger.info(f"Accessing web page: {self.url}")
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("Logging in to Virtual Office")
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
            logger.info("Action - Clicking Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(10)
            logger.info("Change password page should appear")
            logger.info("Entering old password")
            self.set_text_field('name', 'oldPw', self.password)
            logger.info("Entering new password")
            self.set_text_field('name', 'newPw', self.new_password)
            logger.info("Confirming new password")
            self.set_text_field('name', 'confirmPw', self.new_password)
            logger.info("Action - Clicking Change Password button")
            self.click_element('xpath', '//button[text()="Change Password"]')
            time.sleep(10)
            logger.info("Login Test Flag.")
            return True
        except Exception as err:
            logger.info("Exception: " + str(err))
            logger.info("Virtual Office Login failed")

    def virtual_office_logout(self):
        try:
            logger.info("Logging out")
            logger.info("Action - Clicking logout")
            self.click_element('xpath', '//div/button[text()="Logout"]')
            self.click_element('xpath', '//button[text()="Continue"]')
            logger.info("logout firefox... ")
            if self.does_element_exist('xpath', '//div[contains(text(), "You have been logged out.")]'):
                logger.info("Logged out")
            self.close_browser()
            self.quit()
            return True
        except Exception as err:
            logger.info("Exception: " + str(err))
            logger.info("Virtual Office Logout failed")

    def ula_login_ui(self, blocked_user=False):
        try:
            self.get_browser()
            self.go_to_url(self.url)
            time.sleep(4)
            
            # self.click_element('xpath','/html/body/div/div/div[3]/a')

            # Manually going to login page, since with Selenium, login link is not being shown second time
            # Verified the above functionality manually, no issues found
            if self.does_page_have_text("Authentication Required"):
                self.go_to_url("https://23.0.0.100")
            time.sleep(3)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
            logger.info("Action - Clicked Login")
            self.click_element('class', 'sw-login__trigger')
            if blocked_user:
                    logger.info("Checking if blocked user is denied access")
                    self.wait_for_text("User login denied - User has no privileges for login from that location")
                    logger.info("Blocked user denied access success")
                    self.quit()
                    return True
            time.sleep(10)
            logger.info("Login Test Flag.")
            self.click_element('xpath', '//button[text()="Continue"]')
            self.switchToDefaultWindow()
            self.go_to_url(self.url)
            logger.info("Checking if Apache webserver homepage is loaded or not")
            Assertion.assert_equal(self.does_page_have_text("This page is used to test the proper operation of the Apache HTTP server after it has been installed."), True, "ERR: Unble to reach WAN host even after ULA Login")
            logger.info("Apache webserver homepage is loaded successfully")
            return True
        except Exception as err:
            logger.error("Exception: " + str(err))
            Assertion.fail("ULA login failed")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Login group service by UI')
    parser.add_argument('-url', type=str, dest='url', required=True, help='http server url')
    parser.add_argument('-user', type=str, dest='user', required=True, help='user to login group service')
    parser.add_argument('-pwd', type=str, dest='pwd', required=True, help='pwd to login group service')
    parser.add_argument('custom_argument', type=str, help='customized argument based on the requirement')
    args = parser.parse_args()
    uiobj = VOPage(args.url, args.user, args.pwd)
    if args.custom_argument == 'portallogin':
        uiobj.virtual_office_login()
        uiobj.virtual_office_logout()
    elif args.custom_argument == 'ulaloginblockeduser':
        uiobj.ula_login_ui(blocked_user=True)
    elif args.custom_argument == 'ulalogin':
        uiobj.ula_login_ui()
