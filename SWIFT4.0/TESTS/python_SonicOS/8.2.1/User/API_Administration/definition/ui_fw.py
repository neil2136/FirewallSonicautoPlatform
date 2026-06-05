import re
import sys
import argparse
import sys
import time

sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
# sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
print(sys.path)
from runner.settings import logger
# from modules.ui.ui_wrapper_test import Browser #headless argument commented
from modules.ui.ui_wrapper import Browser  #running with headless without opening UI
from runner.utils.assertion import Assertion

class FWPage(Browser):
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password

    def login_ui_pwd_change(self, old_pwd, new_pwd):
        try:
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_text_field('xpath', '//input[@name="username"]', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('xpath', '//input[@name="password"]', self.password)
            logger.info("Action - Clicked Login")
            self.click_element('class', 'sw-login__trigger')

            logger.info("Configure - Setting old password")
            self.set_text_field('xpath', "//input[@name='oldPw']", old_pwd)
            logger.info("Configure - Setting new password")
            self.set_text_field('xpath', "//input[@name='newPw']", new_pwd)
            logger.info("Configure - Setting confirm new password")
            self.set_text_field('xpath', "//input[@name='confirmPw']", new_pwd)
            logger.info("Action - Clicked change password")
            self.click_element('xpath', "//button[normalize-space()='Change Password']")
            logger.info("Login Test Flag.")
            return True, "Logged in Success"
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")
            return False, str(err)