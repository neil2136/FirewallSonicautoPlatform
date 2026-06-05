import re
import sys
import argparse
import sys
import os
import json
sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
# sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
print(sys.path)
from runner.settings import logger
from modules.ui.ui_wrapper import Browser
# from modules.ui.ui_wrapper_test import Browser
from runner.utils.assertion import Assertion
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

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

    def navigate_to_radius_accounting_tab(self):
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
            self.click_element('xpath', "//span[normalize-space()='Device']")
            time.sleep(10)
            self.click_element('xpath', "//span[normalize-space()='Users']")
            time.sleep(5)
            logger.info("Action - Clicked Users")
            self.click_element('xpath', "//li[@class='sw-nav-group sw-nav-group--dark sw-nav-group--compact']//span[normalize-space()='Settings']")
            time.sleep(5)
            logger.info("Action - Clicked Settings")
            self.click_element('xpath', "//span[normalize-space()='Accounting']")
            time.sleep(5)
            logger.info("Action - Clicked Accounting")
            self.click_element('xpath', "//button[@class='sw-button sw-button--light users-settings-accounting__radius']")
            time.sleep(5)
            logger.info("Action - Clicked  Radius Accounting")
            return resp
       
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to navigate_to_radius_accounting_tab")

    def verify_radius_and_user_accounting_tab(self):
        try:
            response = self.does_page_have_text("RADIUS Servers")
            Assertion.assert_equal(response, True, "ERR: Radius accounting information not displaying")
            self.click_element('xpath', "//span[normalize-space()='General Settings']")
            time.sleep(5)
            logger.info("Action - Clicked  General Settings")
            res = self.does_page_have_text("RADIUS Server Timeout")
            Assertion.assert_equal(res, True, "ERR: User Radius accounting information not displaying")
            self.click_element('xpath', "//span[normalize-space()='User Accounting']")
            time.sleep(5)
            logger.info("Action - Clicked  User Accounting")
            resp = self.does_page_have_text("RADIUS User Accounting")
            Assertion.assert_equal(resp, True, "ERR: User Radius accounting information not displaying")
            if resp == True:
                logger.info('True')
            assert resp == True, "TestCase Failed"

            return resp
       
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to verify_radius_and_user_accounting_tab")

    def verify_tool_tip_for_send_accounting_data_to_all_servers(self):
        try:
            self.click_element('xpath', "//span[normalize-space()='General Settings']")
            time.sleep(5)
            logger.info("Action - Clicked  General Settings")
            element_to_hover = self.browser.find_element(By.XPATH, "//span[@class='sw-icon__inner sw-font-icon icon-info']")
            action = ActionChains(self.browser)
            action.move_to_element(element_to_hover).perform()
            time.sleep(3)
            logger.info("Action - Clicked  tool tip")
            resp = self.does_page_have_text("If this is checked then each accounting request message will be sent to all configured accounting servers")
            Assertion.assert_equal(resp, True, "ERR: tool tip information not displaying")
            if resp == True:
                logger.info('True')
            assert resp == True, "TestCase Failed"

            return resp
       
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to verify_tool_tip_for_send_accounting_data_to_all_servers")

    def verify_tool_tip_for_radius_accounting_test(self):
        try:
            self.click_element('xpath', "//span[normalize-space()='Test']")
            time.sleep(5)
            logger.info("Action - Clicked  Test")
            resp = self.does_page_have_text("To test the RADIUS accounting settings select the test, enter a user name and password that is valid on the RADIUS accounting server if relevant, and then click the Test button. Note that this will apply any changes that have been made.")
            Assertion.assert_equal(resp, True, "ERR: tool tip information not displaying")
            if resp == True:
                logger.info('True')
            assert resp == True, "TestCase Failed"

            return resp
       
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to verify_tool_tip_for_radius_accounting_test")



