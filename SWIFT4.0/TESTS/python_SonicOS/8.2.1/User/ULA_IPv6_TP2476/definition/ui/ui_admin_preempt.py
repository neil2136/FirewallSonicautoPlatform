import re
import sys
import argparse
import sys

sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
from runner.settings import logger
from modules.ui.fw_page import FWPage
from runner.utils.assertion import Assertion
import time

class FWLogin(FWPage):
    def __init__(self, url, user, pwd):
        self.url = url
        self.user = user
        self.password = pwd

    def login_ui(self):
        try:
            self.get_browser()
            self.go_to_url(self.url)

            # verify login 
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
            self.click_element('class', 'sw-login__trigger')
            logger.info("Action - Clicked Login")
            time.sleep(5)
            if self.does_page_have_text("OK to preempt existing administrator?"):
                self.click_element('xpath', "//button[contains(@class, 'sw-button sw-button--light')]")
                logger.info("Action - Clicked config")
            logger.info("Waiting for warning")
            time.sleep(50)
            if self.does_page_have_text('You have been preempted by another administrator'):
                ele = self.get_element('xpath', "//div[contains(@class, 'sw-confirm-modal__dialog')]")
                logger.info(f"Received warning: {str(ele.text)}")
                time.sleep(10)
                self.click_element('xpath', "//button[@class='sw-button sw-button--light' and text()='OK']")
                logger.info("Action - Clicked on Ok")
                time.sleep(5)
                # self.click_element('xpath', "//button[normalize-space()='Cancel']")
                time.sleep(2)
                # navigate to local users and add user
                self.navigate_to_local_users_section()
                time.sleep(5)
                self.click_element('xpath', "//div[contains(@class, 'sw-checkbox__box sw-flexbox__flex-none sw-flexbox sw-flexbox--center-items sw-flexbox--center-justify')]")
                logger.info("Action - Checkbox")
                self.click_element('xpath', "//span[@class='sw-icon-button__label-cont sw-flexbox__flex-none' and text()='Delete User']")
                logger.info("Action - Clicked on delete user")
                time.sleep(2)
                self.click_element('xpath', "//button[@class='sw-button sw-button--light sw-button--default' and text()='Confirm']")
                logger.info("Action - Clicked on Confirm")
                time.sleep(2)
                Assertion.assert_equal(self.does_page_have_text('Non config mode'), True, "ERR: Failed to verify non cofig mode.")
                self.click_element('xpath', "//button[@class='sw-button sw-button--light sw-button--default' and text()='OK']")
                logger.info("Action - Clicked on Ok")
                time.sleep(2)
            else:
                 Assertion.fail("Failed to verify warning prompt")
            
            self.logout_ui()

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("FW login failed")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ULA login by UI')
    parser.add_argument('-url', type=str, dest='url', required=True, help='http server url')
    parser.add_argument('-user', type=str, dest='user', required=True, help='username to login')
    parser.add_argument('-pwd', type=str, dest='pwd', required=True, help='pwd to login')
    
    args = parser.parse_args()
        
    uiobj = FWLogin(args.url, args.user, args.pwd)
    rc = uiobj.login_ui()
