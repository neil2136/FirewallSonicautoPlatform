import re
import sys
import argparse
import sys
import time
sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')

from runner.settings import Params, logger
from modules.ui.fw_page import FWPage
from runner.utils.assertion import Assertion


class UIPage(FWPage):

    def login(self, user, password, member):
        try:
            self.get_browser()
            self.go_to_url("https://" + self.ip)
            time.sleep(5)
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', password)
            logger.info("Action - Clicking Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(5)
            flag = False
            if self.does_page_have_text("You have logged in successfully!"):
                flag=True
            self.close_browser()
            return flag
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("login failed")