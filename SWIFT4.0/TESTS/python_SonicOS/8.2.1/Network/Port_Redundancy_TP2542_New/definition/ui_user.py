import re
import sys
import argparse
import sys
from datetime import datetime, timedelta
sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
# sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
#print(sys.path)
from runner.settings import logger
from modules.ui.ui_wrapper import Browser
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from runner.utils.assertion import Assertion
from selenium.webdriver.common.by import By

import time


class FWPage(Browser):
    def __init__(self, method, url, user, pwd):
        self.method = method
        self.url = url
        self.user = user
        self.password = pwd
        

    def tc1_verify_port_redudance_for_vlan_interface(self):
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
            self.click_element('xpath', "//span[@class='sw-icon__inner sw-font-icon icon-topo']")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Interfaces']")
            time.sleep(2)
            self.click_element('xpath', "//span[@class='sw-icon-button__label-cont sw-flexbox__flex-none'][normalize-space()='Add Interface']")
            self.click_element('xpath', "//span[normalize-space()='Virtual Interface']")
            self.click_element('xpath', "//span[normalize-space()='Advanced']")     
            port_redudancy_button = self.does_page_have_text('Redundant/Aggregate Ports')
            if port_redudancy_button == False:
                logger.info('True')      
        except Exception as err:
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

    if args.method == "tc1":
        rc = uiobj.tc1_verify_port_redudance_for_vlan_interface()
    # elif args.method == "tc2":
    #     rc = uiobj.tc2_max_min_button()