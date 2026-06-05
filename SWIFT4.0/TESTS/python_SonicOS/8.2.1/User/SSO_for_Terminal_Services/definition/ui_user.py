import re
import sys
import argparse
import sys

sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
# sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
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

    def add_ts_agent(self, host, shared_key):
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
            self.click_element('xpath', "//button[@class='sw-button sw-button--light users-settings-auth__configure-sso']")
            time.sleep(10)
            logger.info("Action - Clicked confiure SSO")
            self.click_element('xpath', "//span[normalize-space()='Terminal Services']")
            time.sleep(10)
            logger.info("Action - Clicked Terminal Services")
            self.click_element('xpath', "//span[@class='sw-icon-button__label-cont sw-flexbox__flex-none'][normalize-space()='Add Agent']")
            time.sleep(5)
            logger.info("Action - Clicked Add Agent")
            self.clear_text_field("xpath","//input[@name='agentHost']")
            time.sleep(5)
            logger.info("clearing host feild")
            self.set_text_field('xpath', "//input[@name='agentKey']", shared_key)
            time.sleep(5)
            logger.info("input shared key")
            self.set_text_field('xpath', "//input[@name='confirmKey']", shared_key)
            time.sleep(5)
            logger.info("input confirm shared key")
            self.set_text_field('xpath', "//input[@name='agentHost']", host)
            time.sleep(5)
            logger.info("input host")
            self.click_element('xpath', "//button[normalize-space()='Save']")
            time.sleep(5)
            logger.info("Action - Clicked save")
            resp = self.does_page_have_text(host)
            time.sleep(5)
            Assertion.assert_equal(resp, True, "ERR: search for specified profile is failed")
            if resp == True:
                logger.info('True')
            assert resp == True, "TestCase Failed"
            time.sleep(5)
            return resp  
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def delete_ts_agent(self):    
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
            self.click_element('xpath', "//button[@class='sw-button sw-button--light users-settings-auth__configure-sso']")
            time.sleep(10)
            logger.info("Action - Clicked confiure SSO")
            self.click_element('xpath', "//span[normalize-space()='Terminal Services']")
            time.sleep(10)
            self.move_to_the_element('xpath', "//div[contains(text(),'10.10.10.15')]")
            time.sleep(5)
            logger.info("Action - selected row")
            self.click_element('xpath', "//span[@class='sw-icon-button sw-icon-button--no-border sw-icon-button--dark']//span[@class='sw-icon__inner sw-font-icon icon-trash']") 
            logger.info("Action - Clicked delete")
            time.sleep(5)
            self.click_element("xpath","//button[normalize-space()='Confirm']")
            time.sleep(5)
            logger.info("Action - Clicked confirm")
            resp = self.does_page_have_text("10.10.10.15")
            time.sleep(5)
            Assertion.assert_equal(resp, False, "ERR: search for specified profile is failed")
            if resp == False:
                logger.info('False')
            assert resp == False, "TestCase Failed"
            time.sleep(5)

            return resp
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")  

    def edit_ts_agent_shared_key_with_different_length(self):
        shared_key_odd = '7B316'
        shared_key_null = '0'
        shared_key_16 = '1234567890ABCDEF'
        shared_key_18 = '1234567890ABCDEF12'
        shared_key_non_hexadecimal = '1G2H3I4J5K6L7M8N'
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
            self.click_element('xpath', "//button[@class='sw-button sw-button--light users-settings-auth__configure-sso']")
            time.sleep(10)
            logger.info("Action - Clicked confiure SSO")
            self.click_element('xpath', "//span[normalize-space()='Terminal Services']")
            time.sleep(10)
            self.move_to_the_element('xpath', "//div[contains(text(),'10.10.10.16')]")
            time.sleep(5)
            logger.info("Action - selected row")
            self.click_element("xpath","//div[@class='sw-table-row-float-actions sw-flexbox sw-flexbox--center-items']//span[@class='sw-icon__inner sw-font-icon icon-pencil']")
            time.sleep(5)
            logger.info("Action - Clicked edit")
            self.set_text_field('xpath', "//input[@name='agentKey']", shared_key_odd)
            time.sleep(5)
            logger.info("input shared key")
            self.set_text_field('xpath', "//input[@name='confirmKey']", shared_key_odd)
            time.sleep(5)
            logger.info("input confirm shared key")
            out = self.does_page_have_text("Please enter an even number of characters and use (0-9,a-f,A-F) only!")
            time.sleep(5)
            Assertion.assert_equal(out, True, "ERR: search for specified profile is failed")


            self.clear_text_field("xpath","//input[@name='agentKey']")
            time.sleep(5)
            logger.info("clearing shared_key feild")
            self.clear_text_field("xpath","//input[@name='confirmKey']")
            time.sleep(5)
            logger.info("clearing shared_key feild")
            self.set_text_field('xpath', "//input[@name='agentKey']", shared_key_null)
            time.sleep(5)
            logger.info("input shared key")
            self.set_text_field('xpath', "//input[@name='confirmKey']", shared_key_null)
            time.sleep(5)
            logger.info("input confirm shared key")
            out = self.does_page_have_text("Please enter an even number of characters and use (0-9,a-f,A-F) only!")
            time.sleep(5)
            Assertion.assert_equal(out, True, "ERR: search for specified profile is failed")


            self.clear_text_field("xpath","//input[@name='agentKey']")
            time.sleep(5)
            logger.info("clearing shared_key feild")
            self.clear_text_field("xpath","//input[@name='confirmKey']")
            time.sleep(5)
            logger.info("clearing shared_key feild")
            self.set_text_field('xpath', "//input[@name='agentKey']", shared_key_non_hexadecimal)
            time.sleep(5)
            logger.info("input shared key")
            self.set_text_field('xpath', "//input[@name='confirmKey']", shared_key_non_hexadecimal)
            time.sleep(5)
            logger.info("input confirm shared key")
            out = self.does_page_have_text("Please enter an even number of characters and use (0-9,a-f,A-F) only!")
            time.sleep(5)
            Assertion.assert_equal(out, True, "ERR: search for specified profile is failed")


            self.clear_text_field("xpath","//input[@name='agentKey']")
            time.sleep(5)
            logger.info("clearing shared_key feild")
            self.clear_text_field("xpath","//input[@name='confirmKey']")
            time.sleep(5)
            logger.info("clearing shared_key feild")
            self.set_text_field('xpath', "//input[@name='agentKey']", shared_key_18)
            time.sleep(5)
            logger.info("input shared key")
            self.set_text_field('xpath', "//input[@name='confirmKey']", shared_key_18)
            time.sleep(5)
            logger.info("input confirm shared key")
            self.click_element('xpath', "//button[normalize-space()='Save']")
            time.sleep(5)
            logger.info("Action - Clicked save")
            out = self.does_page_have_text("Value or string length(18) out of bounds (max = 16)")
            time.sleep(5)
            Assertion.assert_equal(out, True, "ERR: search for specified profile is failed")
            self.click_element('xpath', "//button[normalize-space()='OK']")
            time.sleep(5)
            logger.info("Action - Clicked ok")


            self.clear_text_field("xpath","//input[@name='agentKey']")
            time.sleep(5)
            logger.info("clearing shared_key feild")
            self.clear_text_field("xpath","//input[@name='confirmKey']")
            time.sleep(5)
            logger.info("clearing shared_key feild")
            self.set_text_field('xpath', "//input[@name='agentKey']", shared_key_16)
            time.sleep(5)
            logger.info("input shared key")
            self.set_text_field('xpath', "//input[@name='confirmKey']", shared_key_16)
            time.sleep(5)
            logger.info("input confirm shared key")
            self.click_element('xpath', "//button[normalize-space()='Save']")
            time.sleep(5)
            logger.info("Action - Clicked save")
            resp = self.does_page_have_text("Please enter an even number of characters and use (0-9,a-f,A-F) only!")
            time.sleep(5)
            Assertion.assert_equal(resp, False, "ERR: search for specified profile is failed")
            if resp == False:
                logger.info('False')
            assert resp == False, "TestCase Failed"
            time.sleep(5)
      
            return resp
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def add_ts_agent_max(self, host, shared_key):
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
            self.click_element('xpath', "//button[@class='sw-button sw-button--light users-settings-auth__configure-sso']")
            time.sleep(10)
            logger.info("Action - Clicked confiure SSO")
            self.click_element('xpath', "//span[normalize-space()='Terminal Services']")
            time.sleep(10)
            logger.info("Action - Clicked Terminal Services")
            self.click_element('xpath', "//span[@class='sw-icon-button__label-cont sw-flexbox__flex-none'][normalize-space()='Add Agent']")
            time.sleep(5)
            resp = self.does_page_have_text("Maximum Terminal Service Agents Reached")
            time.sleep(5)
            Assertion.assert_equal(resp, True, "ERR: search for specified profile is failed")
            if resp == True:
                logger.info('True')
            assert resp == True, "TestCase Failed"
            time.sleep(5)
            return resp  
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Login group service by UI')
#     parser.add_argument("-method", type=str, dest='method', required=True, help="Specify the method to run.")
#     parser.add_argument('-url', type=str, dest='url', required=True, help='http server url')
#     parser.add_argument('-user', type=str, dest='user', required=True, help='user to login group service')
#     parser.add_argument('-pwd', type=str, dest='pwd', required=True, help='pwd to login group service')
#     args = parser.parse_args()
#     uiobj = FWPage(args.method, args.url, args.user, args.pwd)

#     if args.method == "add_ts_agent":
#         rc = uiobj.add_ts_agent()
#     elif args.method == "edit_ts_agent_shared_key_with_different_length":
#         rc = uiobj.edit_ts_agent_shared_key_with_different_length()
#     elif args.method == "delete_ts_agent":
#         rc = uiobj.delete_ts_agent()
