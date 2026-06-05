import re
import sys
import argparse
import sys

sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
# sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
print(sys.path)
from runner.settings import logger
from modules.ui.ui_wrapper import Browser
# from modules.ui.ui_wrapper_test import Browser
from runner.utils.assertion import Assertion

import time

class FWPage(Browser):

    def __init__(self, url, user, pwd):
        self.url = url
        self.user = user
        self.password = pwd

    def login_ui(self, url, user, pwd):
        try:
            self.get_browser()
            self.go_to_url(url)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', pwd)
            logger.info("Action - Clicked Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(10)

            return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def login_ui_pwd_change(self, old_pwd, new_pwd):
        try:
            logger.info("Configure - Setting old password")
            self.set_text_field('xpath', "//input[@name='oldPw']", old_pwd)
            logger.info("Configure - Setting new password")
            self.set_text_field('xpath', "//input[@name='newPw']", new_pwd)
            logger.info("Configure - Setting confirm new password")
            self.set_text_field('xpath', "//input[@name='confirmPw']", new_pwd)
            logger.info("Action - Clicked change password")
            self.click_element('xpath', "//button[normalize-space()='Change Password']")
            return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def change_pw_voluntarily(self, old_pwd, new_pwd):
        try:
            # Click the element that triggers the new window (popup)
            self.click_element('xpath', "//button[@type='button']")

            # Get the current window handle (main window)
            main_window = self.browser.current_window_handle
            
            # Wait for the new window to open
            time.sleep(2)
            
            # Get all window handles
            window_handles = self.browser.window_handles
            
            # Switch to the new window
            for window in window_handles:
                if window != main_window:
                    self.browser.switch_to.window(window)
                    logger.debug2(f"Switched to new window: {window}")
                    break
            
            # Click the element inside the new window
            self.click_element('xpath', "//button[@type='button']")
            logger.info("Configure - Setting old password")
            self.set_text_field('xpath', "//input[@name='oldPw']", old_pwd)
            logger.info("Configure - Setting new password")
            self.set_text_field('xpath', "//input[@name='newPw']", new_pwd)
            logger.info("Configure - Setting confirm new password")
            self.set_text_field('xpath', "//input[@name='confirmPw']", new_pwd)
            logger.info("Action - Clicked change password")
            self.click_element('xpath', "//button[normalize-space()='Change Password']") 
            # Switch back to the main window
            self.browser.switch_to.window(main_window)
            logger.debug2(f"Switched back to main window: {main_window}")
            
        except Exception as err:
            logger.error(f"Exception occurred while performing actions in the new window: {err}")
            Assertion.fail(f"Action - Unable to perform actions in new window: {err}")

    def verify_warning_message(self):
        try:
            resp = self.does_page_have_text("Password length must be at least 8 and contains at least 1 upper case letter ,1 lower case letter, 1 numeric character")
            Assertion.assert_equal(resp, True, "ERR: warning message not displaying")
            if resp == True:
                logger.info('True')
            assert resp == True, "TestCase Failed"

            return resp
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def verify_error_message(self):
        try:
            resp = self.does_page_have_text("Password expired.")
            Assertion.assert_equal(resp, True, "ERR: error message not displaying")
            if resp == True:
                logger.info('True')
            assert resp == True, "TestCase Failed"

            return resp
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def accept_acceptable_policy(self, url, user, pwd):
        try:
            self.get_browser()
            self.go_to_url(url)
            logger.info("Logging in")
            self.click_element('xpath', "//button[@type='button']")
            logger.info("Action - Clicked accept button")
            time.sleep(10)
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', pwd)
            logger.info("Action - Clicked Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(10)

            return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")


