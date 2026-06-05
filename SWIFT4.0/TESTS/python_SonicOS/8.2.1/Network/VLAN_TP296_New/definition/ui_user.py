import re
import sys
import argparse
import sys
from datetime import datetime, timedelta

sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
# sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
# print(sys.path)
from runner.settings import logger
from modules.ui.ui_wrapper import Browser
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from runner.utils.assertion import Assertion

import time


class FWPage(Browser):
    def __init__(self, method, url, user, pwd):
        self.method = method
        self.url = url
        self.user = user
        self.password = pwd

    def firewall_login(self):
        try:
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
            logger.info("Action - Clicked Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(10)
            self.click_element('xpath', "//button[normalize-space()='Cancel']")
            time.sleep(5)
            logger.info("Login Test Flag.")
            self.click_element('xpath', "//span[@class='sw-icon__inner sw-font-icon icon-topo']")
            time.sleep(10)
            text = "X0:V100"
            xpath_expression = f"//div[contains(text(),'{text}')]"
            element = self.browser.find_element('xpath', xpath_expression)
            actions = ActionChains(self.browser)
            actions.move_to_element(element).perform()
            time.sleep(5)
            self.click_element('xpath',
                               "//div[@class='sw-table-row-float-actions sw-flexbox sw-flexbox--center-items']//span[@class='sw-icon__inner sw-font-icon icon-pencil']")
            time.sleep(5)
            vlan_element = self.browser.find_element('xpath',
                                                     "//div//input[@name='textfield-vlan-tag']")
            is_greyed_out = "disabled" in vlan_element.get_attribute("class") or vlan_element.get_attribute(
                "disabled") is not None

            if is_greyed_out:
                logger.info("VLAN TAG field is greyed out.")
                logger.info("True")
            return True
        except Exception as err:
            return False
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Login group service by UI')
    parser.add_argument("-method", type=str, dest='method', required=True, help="Specify the method to run.")
    parser.add_argument('-url', type=str, dest='url', required=True, help='http server url')
    parser.add_argument('-user', type=str, dest='user', required=True, help='user to login group service')
    parser.add_argument('-pwd', type=str, dest='pwd', required=True, help='pwd to login group service')
    args = parser.parse_args()
    uiobj = FWPage(args.method, args.url, args.user, args.pwd)

    if args.method == "firewall_login":
        rc = uiobj.firewall_login()
