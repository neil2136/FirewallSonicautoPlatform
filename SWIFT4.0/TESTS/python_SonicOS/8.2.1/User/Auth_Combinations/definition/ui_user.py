import re
import sys
import argparse
import sys,os
import time
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
# sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
print(sys.path)
from runner.settings import logger
from modules.ui.ui_wrapper import Browser
# from modules.ui.ui_wrapper_test import Browser
from runner.utils.assertion import Assertion


class FWPage(Browser):
    def __init__(self, url, user, pwd):
        self.url = url
        self.user = user
        self.password = pwd

    def refresh_page(self):
        max_refresh_attempts = 4
        refresh_attempts = 0
        while refresh_attempts < max_refresh_attempts:
            logger.info("Attempting to refresh the page...")
            try:
                if not self.does_page_have_text("Login"):
                    logger.info(
                        f"Page not loaded correctly, refreshing now. Attempt {refresh_attempts + 1}/{max_refresh_attempts}")
                    logger.info("Reloading URL manually.")
                    self.go_to_url(self.url)
                    time.sleep(5)
                else:
                    logger.info("Page is loaded correctly, no refresh needed.")
                    return
            except Exception as e:
                logger.error(f"Error while refreshing the page: {e}")
            refresh_attempts += 1

    def login_ui(self):
        try:
            logger.info("Opening the Firefox Browser")
            self.get_browser()
            logger.info("Browser Successfully Invoked")
            self.go_to_url(self.url)
            logger.info("Logging in")
            # Refresh page check before entering credentials
            self.refresh_page()
            # Retry mechanism if login fields are not visible
            for i in range(5):
                if self.does_element_exist('class', 'sw-textfield__wrapper__input'):
                    break
                else:
                    logger.warning(f"Login fields not found, retry {i + 1}/5")
                    time.sleep(5)
                    self.refresh_page()
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)

            logger.info("Action - Clicked Login")
            self.wait_for_element_to_be_visible('class', 'sw-login__trigger')
            res = self.click_element('class', 'sw-login__trigger')
            time.sleep(10)
            self.refresh_page()
            res_url = self.get_current_browser_url()
            logger.info(f"Current URL after login: {res_url}")

            if res is True:
                logger.info("Login Test Flag True.")
                logger.info(f"Firewall login is successful with {self.user} user")
                return res, res_url
            else:
                logger.info(f"Firewall login is unsuccessful with {self.user} user")
                return res, res_url

        except Exception as err:
            logger.error(f"Exception \t: {err}")
            logger.info("Firewall login failed")
            return False, None
