import re
import sys
import argparse
import sys,os
import time
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
print(sys.path)
from runner.settings import logger
from modules.ui.ui_wrapper_test import Browser
from runner.utils.assertion import Assertion




class FWPage(Browser):
    def __init__(self, url, user, pwd):
        self.url = url
        self.user = user
        self.password = pwd

    def login_ui(self):
        try:
            logger.info("Opening the Firefox Browser")
            self.get_browser()
            logger.info("Browser Successfully Invoked")
            self.go_to_url(self.url)
            time.sleep(10)
            logger.info("Logging in")
            self.refresh_browser()
            time.sleep(10)
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.info("Configure - Setting password")
            time.sleep(5)
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
            logger.info("Action - Clicked Login")
            self.wait_for_element_to_be_visible('class', 'sw-login__trigger')
            time.sleep(30)
            res=self.click_element('class', 'sw-login__trigger')
            time.sleep(30)
            print(res,"login")
            self.click_element("xpath","//span[@class='sw-top-nav-item__label sw-flexbox__flex-none'][normalize-space()='Device']")
            logger.info("Clicked on Device")
            self.click_element("xpath","//div[@class='sw-nav-item__content sw-flexbox sw-flexbox--center-items sw-flexbox__flex']//span[contains(text(),'Partitions')]")
            logger.info("Clicked on Partitions")
            res=self.click_element('xpath', "//span[@class='sw-flexbox__flex sw-flexbox sw-flexbox--center-items'][normalize-space()='All']")
            logger.info("Clicked on Auth Partitions")
            res=self.click_element('xpath',"//div[@id='sw-select__option-83249644342-test1']")
            logger.info("clicked on test1")

            return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")
            return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Login group service by UI')
    parser.add_argument('-url', type=str, dest='url', required=True, help='http server url')
    parser.add_argument('-user', type=str, dest='user', required=True, help='user to login group service')
    parser.add_argument('-pwd', type=str, dest='pwd', required=True, help='pwd to login group service')
    args = parser.parse_args()
    uiobj = FWPage(args.url, args.user, args.pwd)
    rc1 = uiobj.login_ui()
