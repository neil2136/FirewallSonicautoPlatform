import re
import sys
import argparse
import sys
import os
import subprocess
import pyotp
import json
sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
# sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/LDAP_Mirrorred_groups/definition')
from settings import *

from runner.settings import logger
from modules.ui.ui_wrapper import Browser
# from modules.ui.ui_wrapper_test import Browser
from runner.utils.assertion import Assertion
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from selenium.webdriver import Firefox, FirefoxOptions

class FWPage(Browser):
    def __init__(self, url, user, pwd):
        self.url = url
        self.user = user
        self.password = pwd


    def login_ui(self):
        try:       
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
            logger.info("Action - Clicked Login")
            resp = self.click_element('class', 'sw-login__trigger')
            time.sleep(40)
            if self.browser.find_element('xpath', '(//span[@class="sw-icon__inner sw-font-icon icon-close-thin"])[2]'):
                    logger.info("Popup detected close it")  
                    self.click_element('xpath', '(//span[@class="sw-icon__inner sw-font-icon icon-close-thin"])[2]') 
            else: 
                 logger.info("No popup detected")
            logger.info("Login Test Flag.")
            time.sleep(10)
            self.click_element('xpath', "//span[normalize-space()='Device']")
            time.sleep(10)
            self.click_element('xpath', "//span[normalize-space()='Users']")
            time.sleep(5)
            logger.info("Action - Clicked Users")
            self.click_element('xpath', "//li[@class='sw-nav-group sw-nav-group--dark sw-nav-group--compact']//span[normalize-space()='Settings']")
            time.sleep(5)
            logger.info("Action - Clicked Settings")
            self.click_element('xpath', "//button[@class='sw-button sw-button--light users-settings-auth__configure-ldap']")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Users & Groups']")
            time.sleep(5)
            self.click_element('xpath', "//div[@class='sw-toggle sw-toggle--right sw-toggle--regular sw-toggle--light ldap-form-user__ldap-usr-grp-mirroring']")
            time.sleep(5)
            self.click_element('xpath', "//button[normalize-space()='No']")
            time.sleep(5)
            self.click_element('xpath', "//button[normalize-space()='Apply']")
            time.sleep(5)
           
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to enable/disable 'Disable Virtual Office on Non-LAN interfaces'")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Login group service by UI')
    parser.add_argument('-url', type=str, dest='url', required=True, help='http server url')
    parser.add_argument('-user', type=str, dest='user', required=True, help='user to login group service')
    parser.add_argument('-pwd', type=str, dest='pwd', required=True, help='pwd to login group service')
    args = parser.parse_args()
    uiobj = FWPage(args.url, args.user, args.pwd)
    rc1 = uiobj.login_ui()




