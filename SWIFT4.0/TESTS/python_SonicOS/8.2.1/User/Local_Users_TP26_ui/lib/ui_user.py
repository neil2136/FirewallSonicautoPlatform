import re
import sys
import argparse
import sys
from datetime import datetime, timedelta
from runner.settings import Params, logger

sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
# sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')

from runner.settings import logger
from modules.ui.ui_wrapper import Browser
# from modules.ui.ui_wrapper_test import Browser
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from runner.utils.assertion import Assertion
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

G_PASSWORD_NEW = Params.G_NEW_PASSWORD

class FWPage(Browser):
    def __init__(self, method, url, user, pwd):
        self.method = method
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
            time.sleep(10)
            logger.info("Login Test Flag.")
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed") 

    def add_user(self):
        new_password = G_PASSWORD_NEW
        name = "test_user"
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
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Device']")
            time.sleep(10)
            logger.info("clicked Device")
            self.click_element('xpath', "//span[contains(text(),'Users')]")
            time.sleep(5)
            logger.info("clicked Users")
            self.click_element('xpath', "//span[normalize-space()='Local Users & Groups']")
            time.sleep(5)
            logger.info("clicked Local Users & Groups")
            self.click_element('xpath', "//span[@class='sw-icon-button__label-cont sw-flexbox__flex-none'][normalize-space()='Add User']")
            time.sleep(5)
            logger.info("clicked Add user")
            self.set_text_field('xpath', "//input[@placeholder='Enter Name...']", name)
            logger.info("Action - Clicked Add user")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Enter password...']", new_password)
            logger.info("Action - Clicked Add user")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Confirm Password']", new_password)
            logger.info("Action - Clicked Add user")
            time.sleep(5)
            self.click_element('xpath', "//button[normalize-space()='Save']")
            time.sleep(5)
            res = self.does_page_have_text("test_user")
            Assertion.assert_equal(res, True, "ERR: Local user is not created")
            time.sleep(5)
            return True

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")  

    def edit_remove_user_privilage(self):
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
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Device']")
            time.sleep(10)
            logger.info("clicked Device")
            self.click_element('xpath', "//span[contains(text(),'Users')]")
            time.sleep(5)
            logger.info("clicked Users")
            self.click_element('xpath', "//span[normalize-space()='Local Users & Groups']")
            time.sleep(5)
            logger.info("clicked Local Users & Groups")
            self.move_to_the_element('xpath', "//span[normalize-space()='test2']")
            time.sleep(5)
            logger.info("Action - selected  row")
            self.click_element('xpath', "//span[@class='sw-icon__inner sw-font-icon icon-pencil']")
            time.sleep(10)
            logger.info("clicked user edit")
            self.click_element('xpath', "//span[normalize-space()='Groups']")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='SonicWALL Administrators']")
            time.sleep(5)
            self.click_element('xpath', "//span[@title='Move marked to left']//span[@class='sw-icon__inner sw-font-icon icon-play']")                              
            time.sleep(5)
            self.click_element('xpath', "//button[normalize-space()='Save']")
            time.sleep(5)
            self.click_element('xpath', "//span[@class='sw-icon-button__label-cont sw-flexbox__flex-none'][normalize-space()='Refresh']")
            time.sleep(5)
            resp = self.does_page_have_text("Full")
            Assertion.assert_equal(resp, False, "ERR: User edit failed")
            if resp == False:
                logger.info('False')
            assert resp == False, "TestCase Failed"
            return resp
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")  

    def edit_add_user_privilage(self):
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
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Device']")
            time.sleep(10)
            self.click_element('xpath', "//span[contains(text(),'Users')]")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Local Users & Groups']")
            time.sleep(5)
            self.move_to_the_element('xpath', "//span[normalize-space()='test1']")
            time.sleep(5)
            logger.info("Action - selected  row")
            self.click_element('xpath', "//span[@class='sw-icon__inner sw-font-icon icon-pencil']")
            time.sleep(10)
            logger.info("clicked user edit")
            self.click_element('xpath', "//span[normalize-space()='Groups']")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='SonicWALL Administrators']")
            time.sleep(5)
            self.click_element('xpath', "//span[@title='Move marked to right']//span[@class='sw-icon__inner sw-font-icon icon-play']")
            time.sleep(5)
            self.click_element('xpath', "//button[normalize-space()='Save']")
            time.sleep(5)
            self.click_element('xpath', "//span[@class='sw-icon-button__label-cont sw-flexbox__flex-none'][normalize-space()='Refresh']")
            time.sleep(5)
            resp = self.does_page_have_text("Full")
            Assertion.assert_equal(resp, True, "ERR: User edit failed")
            if resp == True:
                logger.info('True')
            assert resp == True, "TestCase Failed"
            return resp
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")  

    def adding_vpn_access_for_user(self):
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
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Device']")
            time.sleep(10)
            self.click_element('xpath', "//span[contains(text(),'Users')]")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Local Users & Groups']")
            time.sleep(5)
            self.move_to_the_element('xpath', "//span[normalize-space()='test19']")
            time.sleep(5)
            logger.info("Action - selected  row")
            self.click_element('xpath', "//div[@class='sw-table-row-float-actions sw-flexbox sw-flexbox--center-items']//span[@class='sw-icon__inner sw-font-icon icon-pencil']")
            time.sleep(10)
            logger.info("clicked user edit")
            self.click_element('xpath', "//span[@class='sw-tab__inner__piece sw-flexbox__flex sw-flexbox sw-flexbox--center-items sw-flexbox--center-justify'][normalize-space()='VPN Access']")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Firewalled Subnets']")
            time.sleep(5)
            self.click_element('xpath', "//span[@title='Move marked to right']//span[@class='sw-icon__inner sw-font-icon icon-play']")
            time.sleep(5)
            self.click_element('xpath', "//button[normalize-space()='Save']")
            time.sleep(10)
            self.move_to_the_element('xpath', "//span[normalize-space()='test19']")
            time.sleep(5)
            logger.info("Action - selected  row")
            element_to_hover = self.browser.find_element(By.XPATH, "//span[@class='sw-icon-button sw-icon-button--light']//span[@class='sw-icon__inner sw-font-icon icon-vpn']")
            action = ActionChains(self.browser)
            action.move_to_element(element_to_hover).perform()
            time.sleep(3)
            resp = self.does_page_have_text("Firewalled Subnets")
            Assertion.assert_equal(resp, True, "ERR:vpn access is not displaying")
            if resp == True:
                logger.info('True')
            assert resp == True, "TestCase Failed"
            return resp
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")

    def removing_vpn_access_for_user(self):
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
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Device']")
            time.sleep(10)
            self.click_element('xpath', "//span[contains(text(),'Users')]")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Local Users & Groups']")
            time.sleep(5)
            self.move_to_the_element('xpath', "//span[normalize-space()='test20']")
            time.sleep(5)
            logger.info("Action - selected  row")
            element_to_hover = self.browser.find_element(By.XPATH, "//span[@class='sw-icon-button sw-icon-button--light']//span[@class='sw-icon__inner sw-font-icon icon-vpn']")
            action = ActionChains(self.browser)
            action.move_to_element(element_to_hover).perform()
            time.sleep(3)
            res = self.does_page_have_text("Firewalled Subnets")
            Assertion.assert_equal(res, True, "ERR:vpn access is not displaying")
            time.sleep(5)
            self.move_to_the_element('xpath', "//span[normalize-space()='test20']")
            time.sleep(5)
            logger.info("Action - selected  row")
            self.click_element('xpath', "//div[@class='sw-table-row-float-actions sw-flexbox sw-flexbox--center-items']//span[@class='sw-icon__inner sw-font-icon icon-pencil']")
            time.sleep(10)
            logger.info("clicked user edit")
            self.click_element('xpath', "//span[@class='sw-tab__inner__piece sw-flexbox__flex sw-flexbox sw-flexbox--center-items sw-flexbox--center-justify'][normalize-space()='VPN Access']")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Firewalled Subnets']")
            time.sleep(5)
            self.click_element('xpath', "//span[@title='Move marked to left']//span[@class='sw-icon__inner sw-font-icon icon-play']")
            time.sleep(5)
            self.click_element('xpath', "//button[normalize-space()='Save']")
            time.sleep(5)
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")

    def delete_user(self):
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
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Device']")
            time.sleep(10)
            self.click_element('xpath', "//span[contains(text(),'Users')]")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Local Users & Groups']")
            time.sleep(5)
            self.move_to_the_element('xpath', "//span[normalize-space()='test3']")
            time.sleep(5)
            logger.info("Action - selected  row")
            self.click_element('xpath', "//span[@class='sw-icon-button sw-icon-button--no-border sw-icon-button--dark']//span[@class='sw-icon__inner sw-font-icon icon-trash']")
            time.sleep(10)
            logger.info("clicked delete icon")
            resp = self.does_page_have_text("Are you sure you want to delete test3 ?")
            Assertion.assert_equal(resp, True, "ERR: warning message is not displaying")
            time.sleep(5)
            self.click_element('xpath', "//button[normalize-space()='Confirm']")
            time.sleep(5)
            resp1 = self.does_page_have_text("test3")
            Assertion.assert_equal(resp1, False, "ERR: local user delete failed")
            if resp1 == False:
                logger.info('False')
            assert resp1 == False, "TestCase Failed"
            
            return resp1
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")

    def adding_multiple_vpn_access_for_user(self):
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
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Device']")
            time.sleep(10)
            self.click_element('xpath', "//span[contains(text(),'Users')]")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Local Users & Groups']")
            time.sleep(5)
            self.move_to_the_element('xpath', "//span[normalize-space()='test21']")
            time.sleep(5)
            logger.info("Action - selected  row")
            self.click_element('xpath', "//div[@class='sw-table-row-float-actions sw-flexbox sw-flexbox--center-items']//span[@class='sw-icon__inner sw-font-icon icon-pencil']")
            time.sleep(10)
            logger.info("clicked user edit")
            self.click_element('xpath', "//span[@class='sw-tab__inner__piece sw-flexbox__flex sw-flexbox sw-flexbox--center-items sw-flexbox--center-justify'][normalize-space()='VPN Access']")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='LAN Interface IP']")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='WAN Interface IP']")
            time.sleep(5)
            self.click_element('xpath', "//span[@title='Move marked to right']//span[@class='sw-icon__inner sw-font-icon icon-play']")
            time.sleep(5)
            self.click_element('xpath', "//button[normalize-space()='Save']")
            time.sleep(5)
            self.move_to_the_element('xpath', "//span[normalize-space()='test21']")
            time.sleep(5)
            logger.info("Action - selected  row")
            element_to_hover = self.browser.find_element(By.XPATH, "//span[@class='sw-icon-button sw-icon-button--light']//span[@class='sw-icon__inner sw-font-icon icon-vpn']")
            action = ActionChains(self.browser)
            action.move_to_element(element_to_hover).perform()
            time.sleep(3)
            resp = self.does_page_have_text("LAN Interface IP")
            Assertion.assert_equal(resp, True, "ERR:vpn access is not displaying")
            time.sleep(5)
            resp1 = self.does_page_have_text("WAN Interface IP")
            Assertion.assert_equal(resp1, True, "ERR:vpn access is not displaying")
            if resp == True and resp1 == True:
                logger.info('True')
            assert resp == True and resp1 == True, "TestCase Failed"
            return resp1
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")

    def removing_multiple_vpn_access_for_user(self):
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
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Device']")
            time.sleep(10)
            self.click_element('xpath', "//span[contains(text(),'Users')]")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Local Users & Groups']")
            time.sleep(5)
            self.move_to_the_element('xpath', "//span[normalize-space()='test22']")
            time.sleep(5)
            logger.info("Action - selected  row")
            element_to_hover = self.browser.find_element(By.XPATH, "//span[@class='sw-icon-button sw-icon-button--light']//span[@class='sw-icon__inner sw-font-icon icon-vpn']")
            action = ActionChains(self.browser)
            action.move_to_element(element_to_hover).perform()
            time.sleep(3)
            resp = self.does_page_have_text("LAN Interface IP")
            Assertion.assert_equal(resp, True, "ERR:vpn access is not displaying")
            time.sleep(5)
            resp1 = self.does_page_have_text("WAN Interface IP")
            Assertion.assert_equal(resp1, True, "ERR:vpn access is not displaying")
            time.sleep(5)
            self.move_to_the_element('xpath', "//span[normalize-space()='test22']")
            time.sleep(5)
            logger.info("Action - selected  row")
            self.click_element('xpath', "//div[@class='sw-table-row-float-actions sw-flexbox sw-flexbox--center-items']//span[@class='sw-icon__inner sw-font-icon icon-pencil']")
            time.sleep(10)
            logger.info("clicked user edit")
            self.click_element('xpath', "//span[@class='sw-tab__inner__piece sw-flexbox__flex sw-flexbox sw-flexbox--center-items sw-flexbox--center-justify'][normalize-space()='VPN Access']")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='LAN Interface IP']")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='WAN Interface IP']")
            time.sleep(5)
            self.click_element('xpath', "//span[@title='Move marked to left']//span[@class='sw-icon__inner sw-font-icon icon-play']")
            time.sleep(5)
            self.click_element('xpath', "//button[normalize-space()='Save']")
            time.sleep(5)
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")

    def adding_vpn_access_for_ldap_user(self):
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
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Device']")
            time.sleep(10)
            self.click_element('xpath', "//span[contains(text(),'Users')]")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Local Users & Groups']")
            time.sleep(5)
            # self.move_to_the_element('xpath', "//span[normalize-space()='All LDAP Users']")
            # time.sleep(5)
            # logger.info("Action - selected  row")
            self.click_element('xpath', "//span[normalize-space()='Local Groups']")
            time.sleep(5)
            self.move_to_the_element('xpath', "//span[normalize-space()='Limited Administrators']")
            time.sleep(5)
            logger.info("Action - selected  row")
            self.click_element('xpath', "//div[@class='sw-table-row-float-actions sw-flexbox sw-flexbox--center-items']//span[@class='sw-icon__inner sw-font-icon icon-pencil']")
            time.sleep(10)
            logger.info("clicked user edit")
            self.click_element('xpath', "//span[normalize-space()='Members']")
            logger.info("Action - Clicked member")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='All LDAP Users']")
            logger.info("Action - Clicked LDAP Users")
            time.sleep(5)
            self.click_element('xpath', "//span[@title='Move marked to right']//span[@class='sw-icon__inner sw-font-icon icon-play']")
            time.sleep(5)
            self.click_element('xpath', "//span[@class='sw-tab__inner__piece sw-flexbox__flex sw-flexbox sw-flexbox--center-items sw-flexbox--center-justify'][normalize-space()='VPN Access']")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Firewalled Subnets']")
            time.sleep(5)
            self.click_element('xpath', "//span[@title='Move marked to right']//span[@class='sw-icon__inner sw-font-icon icon-play']")
            time.sleep(5)
            self.click_element('xpath', "//button[normalize-space()='Save']")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Local Users & Groups']")
            time.sleep(5)
            self.move_to_the_element('xpath', "//span[normalize-space()='All LDAP Users']")
            time.sleep(5)
            logger.info("Action - selected  row")
            element_to_hover = self.browser.find_element(By.XPATH, "//span[@class='sw-icon-button sw-icon-button--light']//span[@class='sw-icon__inner sw-font-icon icon-vpn']")
            action = ActionChains(self.browser)
            action.move_to_element(element_to_hover).perform()
            time.sleep(3)
            resp = self.does_page_have_text("Firewalled Subnets")
            # Assertion.assert_equal(resp, True, "ERR:vpn access is not displaying")
            if resp == True:
                logger.info('True')
            # assert resp == True, "TestCase Failed"
            return resp
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")

    def verify_exapnd_veiw(self):
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
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Device']")
            time.sleep(10)
            self.click_element('xpath', "//span[contains(text(),'Users')]")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Local Users & Groups']")
            time.sleep(5)
            self.move_to_the_element('xpath', "//span[normalize-space()='test4']")
            time.sleep(5)
            logger.info("Action - selected  row")
            self.click_element('xpath', "//span[@class='sw-icon sw-icon--block']//span[@class='sw-icon__inner sw-font-icon icon-arrow-up']")
            time.sleep(10)
            logger.info("clicked expand veiw")
            resp = self.does_page_have_text("Everyone")
            Assertion.assert_equal(resp, True, "ERR: User expand veiw failed")
            resp1 = self.does_page_have_text("SonicWALL Administrators")
            Assertion.assert_equal(resp1, True, "ERR: User expand veiw failed")
            resp2 = self.does_page_have_text("Trusted Users")
            Assertion.assert_equal(resp2, True, "ERR: User expand veiw failed")
            resp3 = self.does_page_have_text("SSLVPN Services")
            Assertion.assert_equal(resp3, True, "ERR: User expand veiw failed")
            time.sleep(5)
            return resp3
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")  

    def delete_user_using_button(self):
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
            time.sleep(20)
            if self.browser.find_element('xpath', '(//span[@class="sw-icon__inner sw-font-icon icon-close-thin"])[2]'):
                    logger.info("Popup detected close it")  
                    self.click_element('xpath', '(//span[@class="sw-icon__inner sw-font-icon icon-close-thin"])[2]') 
            else: 
                 logger.info("No popup detected")
            logger.info("Login Test Flag.")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Device']")
            time.sleep(10)
            self.click_element('xpath', "//span[contains(text(),'Users')]")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Local Users & Groups']")
            time.sleep(5)
            self.move_to_the_element('xpath', "//span[normalize-space()='test5']")
            time.sleep(5)
            logger.info("Action - selected  row")
            # self.click_element('xpath', "/html/body/div/div/div/div[2]/div[3]/div[2]/div[1]/div/section/div/div[2]/div[2]/div/div[1]/div/div[1]/div/div/div/span/div/div/div/div/span/span")
            # self.click_element('xpath', "//span[@class='sw-icon__inner sw-font-icon icon-checkmark']")
            # //div[@class='sw-table-row sw-table-row--light sw-table-row--3435670314 sw-flexbox sw-table-row--auto sw-table-body__row-rendered-first--3435670314']//span[@class='sw-icon__inner sw-font-icon icon-checkmark']
            # //*[@id="app"]/div/div/div[2]/div[3]/div[2]/div[1]/div/section/div/div[2]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/span/span
            # logger.info("selected user")
            self.click_element('xpath', "//span[@class='sw-icon-button sw-icon-button--no-border sw-icon-button--dark']//span[@class='sw-icon__inner sw-font-icon icon-trash']")
            time.sleep(10)
            logger.info("clicked delete icon")
            resp = self.does_page_have_text("Are you sure you want to delete test5 ?")
            Assertion.assert_equal(resp, True, "ERR: warning message is not displaying")
            time.sleep(5)
            self.click_element('xpath', "//button[normalize-space()='Confirm']")
            time.sleep(5)
            # self.click_element('xpath', "//span[@class='sw-icon-button__label-cont sw-flexbox__flex-none'][normalize-space()='Delete User']")
            # time.sleep(10)
            # logger.info("clicked delete user")
            # resp = self.does_page_have_text("Are you sure you want to delete the selected entries?")
            # Assertion.assert_equal(resp, True, "ERR: warning message is not displaying")
            # time.sleep(5)
            # self.click_element('xpath', "//button[normalize-space()='Confirm']")
            # time.sleep(10)
            # logger.info("clicked confirm")
            resp1 = self.does_page_have_text("test5")
            Assertion.assert_equal(resp1, False, "ERR: local user delete failed")
            if resp1 == False:
                logger.info('False')
            assert resp1 == False, "TestCase Failed"
            
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")

    def disable_apply_password_constraints_of_all_user(self):
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
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Device']")
            time.sleep(10)
            self.click_element('xpath', "//span[contains(text(),'Users')]")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Local Users & Groups']")
            time.sleep(5)
            self.click_element('xpath', "//span[@class='sw-tab__inner__piece sw-flexbox__flex sw-flexbox sw-flexbox--center-items sw-flexbox--center-justify'][normalize-space()='Settings']")
            time.sleep(10)
            logger.info("clicked setting")
            self.click_element('xpath', "//div[@class='sw-form']//div[1]//div[1]//div[2]//div[1]")
            time.sleep(5)
            self.click_element('xpath', "//button[@type='button']")
            time.sleep(5)
            
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")

    def add_user_with_sonicwall_administrator_and_check_admin_column(self):
        new_password = G_PASSWORD_NEW
        name = "test7"
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
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Device']")
            time.sleep(10)
            self.click_element('xpath', "//span[contains(text(),'Users')]")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Local Users & Groups']")
            time.sleep(5)
            self.click_element('xpath', "//span[@class='sw-icon-button__label-cont sw-flexbox__flex-none'][normalize-space()='Add User']")
            time.sleep(5)
            logger.info("clicked Add user")
            self.set_text_field('xpath', "//input[@placeholder='Enter Name...']", name)
            logger.info("Action - Clicked Add user")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Enter password...']", new_password)
            logger.info("Action - Clicked Add user")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Confirm Password']", new_password)
            logger.info("Action - Clicked Add user")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Groups']")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='SonicWALL Administrators']")
            time.sleep(5)
            self.click_element('xpath', "//span[@title='Move marked to right']//span[@class='sw-icon__inner sw-font-icon icon-play']")
            time.sleep(5)
            self.click_element('xpath', "//button[normalize-space()='Save']")
            time.sleep(5)
            self.click_element('xpath', "//span[@class='sw-icon-button__label-cont sw-flexbox__flex-none'][normalize-space()='Refresh']")
            time.sleep(5)
            res = self.does_page_have_text("test7")
            Assertion.assert_equal(res, True, "ERR: Local user is not created")
            time.sleep(5)
            self.move_to_the_element('xpath', "//span[normalize-space()='test7']")
            time.sleep(5)
            logger.info("Action - selected  row")
            resp1 = self.does_page_have_text("Full")
            Assertion.assert_equal(resp1, True, "ERR: User edit failed")
            time.sleep(5)
            if resp == True and resp1 == True:
                logger.info('True')
            assert resp == True and resp1 == True, "TestCase Failed"
            return resp
        
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")

    def add_user_account_life_as_never_expires(self):
        new_password = G_PASSWORD_NEW
        name = "test9"
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
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Device']")
            time.sleep(10)
            self.click_element('xpath', "//span[contains(text(),'Users')]")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Local Users & Groups']")
            time.sleep(5)
            self.click_element('xpath', "//span[contains(text(),'Add User')]")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Enter Name...']", name)
            logger.info("Action - Clicked Add user")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Enter password...']", new_password)
            logger.info("Action - Clicked Add user")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Confirm password...']", new_password)
            logger.info("Action - Clicked Add user")
            time.sleep(5)
            self.select_drop_down_value('Account Lifetime', "Never Expires", modal=True)
            time.sleep(10)
            logger.info("selected Never Expires")
            self.click_element('xpath', "//button[normalize-space()='Save']")
            time.sleep(5)
            resp = self.does_page_have_text("test9")
            Assertion.assert_equal(resp, True, "ERR: Local user is not created")
            time.sleep(5)
            if resp == True:
                logger.info('True')
            assert resp == True, "TestCase Failed"

            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")  

    def add_user_with_sslvpn_service(self):
        new_password = G_PASSWORD_NEW
        name = "test12"
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
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Device']")
            time.sleep(10)
            self.click_element('xpath', "//span[contains(text(),'Users')]")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Local Users & Groups']")
            time.sleep(5)
            self.click_element('xpath', "//span[@class='sw-icon-button__label-cont sw-flexbox__flex-none'][normalize-space()='Add User']")
            time.sleep(5)
            logger.info("clicked Add user")
            self.set_text_field('xpath', "//input[@placeholder='Enter Name...']", name)
            logger.info("Action - Clicked Add user")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Enter password...']", new_password)
            logger.info("Action - Clicked Add user")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Confirm Password']", new_password)
            logger.info("Action - Clicked Add user")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Groups']")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='SSLVPN Services']")
            time.sleep(5)
            self.click_element('xpath', "//span[@title='Move marked to right']//span[@class='sw-icon__inner sw-font-icon icon-play']")
            time.sleep(5)
            self.click_element('xpath', "//button[normalize-space()='Save']")
            time.sleep(5)
            resp = self.does_page_have_text("test12")
            Assertion.assert_equal(resp, True, "ERR: Local user is not created")
            time.sleep(5)
            self.move_to_the_element('xpath', "//span[normalize-space()='test12']")
            time.sleep(5)
            logger.info("Action - selected  row")
            self.click_element('xpath', "//span[@class='sw-icon sw-icon--block']//span[@class='sw-icon__inner sw-font-icon icon-arrow-up']")
            time.sleep(10)
            logger.info("clicked expand veiw")
            resp3 = self.does_page_have_text("SSLVPN Services")
            Assertion.assert_equal(resp3, True, "ERR: User expand veiw failed")
            if resp3 == True:
                logger.info('True')
            assert resp3 == True, "TestCase Failed"
            return resp3
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")

    def remove_user_with_sslvpn_service(self):
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
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Device']")
            time.sleep(10)
            self.click_element('xpath', "//span[contains(text(),'Users')]")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Local Users & Groups']")
            time.sleep(5)
            self.move_to_the_element('xpath', "//span[normalize-space()='test12']")
            time.sleep(5)
            logger.info("Action - selected  row")
            self.click_element('xpath', "//span[@class='sw-icon__inner sw-font-icon icon-pencil']")
            time.sleep(10)
            logger.info("clicked user edit")
            self.click_element('xpath', "//span[normalize-space()='Groups']")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='SSLVPN Services']")
            time.sleep(5)
            self.click_element('xpath', "//span[@title='Move marked to left']//span[@class='sw-icon__inner sw-font-icon icon-play']")
            time.sleep(5)
            self.click_element('xpath', "//button[normalize-space()='Save']")
            time.sleep(5)
            self.move_to_the_element('xpath', "//span[normalize-space()='test12']")
            time.sleep(5)
            logger.info("Action - selected  row")
            self.click_element('xpath', "//span[@class='sw-icon sw-icon--block']//span[@class='sw-icon__inner sw-font-icon icon-arrow-up']")
            time.sleep(10)
            logger.info("clicked expand veiw")
            resp3 = self.does_page_have_text("SSLVPN Services")
            Assertion.assert_equal(resp3, False, "ERR: User expand veiw failed")
            if resp3 == False:
                logger.info('False')
            assert resp3 == False, "TestCase Failed"
            return resp3

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")

    def add_user_with_guest_service_and_verify_tab(self):
        new_password = G_PASSWORD_NEW
        name = "test13"
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
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Device']")
            time.sleep(10)
            self.click_element('xpath', "//span[contains(text(),'Users')]")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Local Users & Groups']")
            time.sleep(5)
            self.click_element('xpath', "//span[@class='sw-icon-button__label-cont sw-flexbox__flex-none'][normalize-space()='Add User']")
            time.sleep(5)
            logger.info("clicked Add user")
            self.set_text_field('xpath', "//input[@placeholder='Enter Name...']", name)
            logger.info("Action - Clicked Add user")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Enter password...']", new_password)
            logger.info("Action - Clicked Add user")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Confirm Password']", new_password)
            logger.info("Action - Clicked Add user")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Groups']")
            time.sleep(5)
            self.click_element('xpath', "/html/body/div/div/div/div[2]/div[3]/div[2]/div[1]/div/section/div/div[2]/div[3]/div/div[2]/div/div/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div/div/ul/li[3]/div/div/span")
            time.sleep(5)
            self.click_element('xpath', "//span[@title='Move marked to right']//span[@class='sw-icon__inner sw-font-icon icon-play']")
            time.sleep(5)
            self.click_element('xpath', "//span[@class='sw-tab__inner__piece sw-flexbox__flex sw-flexbox sw-flexbox--center-items sw-flexbox--center-justify'][normalize-space()='Guest Services']")
            time.sleep(5)
            resp = self.does_page_have_text("Guest Services")
            Assertion.assert_equal(resp, True, "ERR: Local user is not created")
            time.sleep(5)
            self.click_element('xpath', "//button[normalize-space()='Save']")
            time.sleep(5)
            resp = self.does_page_have_text("test13")
            Assertion.assert_equal(resp, True, "ERR: Local user is not created")
            if resp == True:
                logger.info('True')
            assert resp == True, "TestCase Failed"

            return resp
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")

    def verify_book_mark_without_sslvpn_serviceuser(self):
        new_password = G_PASSWORD_NEW
        name = "test15"
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
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Device']")
            time.sleep(10)
            self.click_element('xpath', "//span[contains(text(),'Users')]")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Local Users & Groups']")
            time.sleep(5)
            self.click_element('xpath', "//span[@class='sw-icon-button__label-cont sw-flexbox__flex-none'][normalize-space()='Add User']")
            time.sleep(5)
            logger.info("clicked Add user")
            self.set_text_field('xpath', "//input[@placeholder='Enter Name...']", name)
            logger.info("Action - Clicked Add user")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Enter password...']", new_password)
            logger.info("Action - Clicked Add user")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Confirm Password']", new_password)
            logger.info("Action - Clicked Add user")
            time.sleep(5)
            self.click_element('xpath', "//button[normalize-space()='Save']")
            time.sleep(5)
            resp = self.does_page_have_text("test15")
            Assertion.assert_equal(resp, True, "ERR: Local user is not created")
            time.sleep(5)
            self.move_to_the_element('xpath', "//span[normalize-space()='test15']")
            time.sleep(5)
            logger.info("Action - selected  row")
            element_to_hover = self.browser.find_element(By.XPATH, "//div[@class='sw-table-row-float-actions sw-flexbox sw-flexbox--center-items']//span[@class='sw-icon__inner sw-font-icon icon-bookmark']")
            action = ActionChains(self.browser)
            action.move_to_element(element_to_hover).perform()
            time.sleep(3)
            logger.info("clicked Book mark icon")
            resp3 = self.does_page_have_text("Add membership to the SSLVPN Services group and submit the change to enable adding bookmarks.")
            Assertion.assert_equal(resp3, True, "ERR: testcase failed")
            if resp3 == True:
                logger.info('True')
            assert resp3 == True, "TestCase Failed"
            return resp3

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")  

    def add_bookmark(self):
        bookmark_name = "Book_mark"
        bookmark_ip = "10.10.10.10"
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
            self.click_element('xpath', "//span[contains(text(),'Users')]")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Local Users & Groups']")
            time.sleep(5)
            self.move_to_the_element('xpath', "//span[normalize-space()='test16']")
            time.sleep(5)
            logger.info("Action - selected  row")
            self.click_element('xpath', "//span[@class='sw-icon-button sw-icon-button--no-border sw-icon-button--dark']//span[@class='sw-icon__inner sw-font-icon icon-bookmark']")
            time.sleep(10)
            logger.info("clicked Bookmark icon")
            self.click_element('xpath', "//span[@class='sw-icon-button sw-icon-button--light fw-mgmt-ftr-lcoal-users-settings-bookmark__content-toolbar-add']//span[@class='sw-icon__inner sw-font-icon icon-add']")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Enter bookmark name...']", bookmark_name)
            logger.info("Configure - name of bookmark")
            self.set_text_field('xpath', "//input[@placeholder='Enter Name or IP Address...']", bookmark_ip)
            logger.info("Configure - ip of bookmark")
            self.click_element('xpath', "//button[normalize-space()='Save']")
            logger.info("clicked save")
            time.sleep(10)
            self.click_element('xpath', "//button[normalize-space()='Close']")
            logger.info("clicked close")

            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")
        
    def delete_bookmark(self):
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
            self.click_element('xpath', "//span[contains(text(),'Users')]")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Local Users & Groups']")
            time.sleep(5)
            self.move_to_the_element('xpath', "//span[normalize-space()='test17']")
            time.sleep(5)
            logger.info("Action - selected  row")
            self.click_element('xpath', "//span[@class='sw-icon-button sw-icon-button--no-border sw-icon-button--dark']//span[@class='sw-icon__inner sw-font-icon icon-bookmark']")
            time.sleep(10)
            logger.info("clicked Bookmark icon")
            self.move_to_the_element('xpath', "//div[contains(text(),'Book_mark')]")
            time.sleep(5)
            logger.info("Action - selected  row")
            self.click_element('xpath', "//div[@class='sw-table-row-float-actions sw-flexbox sw-flexbox--center-items']//span[@class='sw-icon__inner sw-font-icon icon-trash']")
            time.sleep(5)
            resp3 = self.does_page_have_text("Book_mark")
            Assertion.assert_equal(resp3, False, "ERR: delete Book mark failed")
            if resp3 == False:
                logger.info('False')
            assert resp3 == False, "TestCase Failed"
            return resp3

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")

    def ui_user_change_pw(self):
        new_password = "P@ssw0rd"
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
            logger.info("Login Test Flag.")
            logger.info("Configure - Setting old password")
            self.set_text_field('xpath', "//input[@name='oldPw']", self.password)
            logger.info("Configure - Setting new password")
            self.set_text_field('xpath', "//input[@name='newPw']", new_password)
            logger.info("Configure - Setting confirm new password")
            self.set_text_field('xpath', "//input[@name='confirmPw']", new_password)
            logger.info("Action - Clicked change password")
            self.click_element('xpath', "//button[normalize-space()='Change Password']")
            logger.info("Action - Clicked continue")
            self.click_element('xpath', "//button[@type='button']")
            time.sleep(10)
            return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def add_ldap_user_to_group(self):
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
            self.click_element('xpath', "//span[contains(text(),'Users')]")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Local Users & Groups']")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Local Groups']")
            time.sleep(5)
            self.move_to_the_element('xpath', "//span[normalize-space()='SonicWALL Administrators']")
            time.sleep(5)
            logger.info("Action - selected  row")
            time.sleep(5)
            self.click_element('xpath', "//div[@class='sw-table-row-float-actions sw-flexbox sw-flexbox--center-items']//span[@class='sw-icon__inner sw-font-icon icon-pencil']")
            logger.info("clicked user edit")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Members']")
            logger.info("Action - Clicked member")
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='All LDAP Users']")
            logger.info("Action - Clicked LDAP Users")
            time.sleep(5)
            self.click_element('xpath', "//span[@title='Move marked to right']//span[@class='sw-icon__inner sw-font-icon icon-play']")
            time.sleep(5)
            self.click_element('xpath', "//button[normalize-space()='Save']")
            time.sleep(5)

            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Login group service by UI')
    parser.add_argument("-method", type=str, dest='method', required=True, help="Specify the method to run.")
    parser.add_argument('-url', type=str, dest='url', required=True, help='http server url')
    parser.add_argument('-user', type=str, dest='user', required=True, help='user to login group service')
    parser.add_argument('-pwd', type=str, dest='pwd', required=True, help='pwd to login group service')
    args = parser.parse_args()
    uiobj = FWPage(args.method, args.url, args.user, args.pwd)

    if args.method == "add_user":
        rc = uiobj.add_user()
    elif args.method == "edit_remove_user_privilage":
        rc = uiobj.edit_remove_user_privilage()
    elif args.method == "edit_add_user_privilage":
        rc = uiobj.edit_add_user_privilage()
    elif args.method == "login_ui":
        rc = uiobj.login_ui()
    elif args.method == "delete_user":
        rc = uiobj.delete_user()
    elif args.method == "adding_vpn_access_for_user":
        rc = uiobj.adding_vpn_access_for_user()
    elif args.method == "removing_vpn_access_for_user":
        rc = uiobj.removing_vpn_access_for_user()
    elif args.method == "adding_multiple_vpn_access_for_user":
        rc = uiobj.adding_multiple_vpn_access_for_user()
    elif args.method == "removing_multiple_vpn_access_for_user":
        rc = uiobj.removing_multiple_vpn_access_for_user()
    elif args.method == "adding_vpn_access_for_ldap_user":
        rc = uiobj.adding_vpn_access_for_ldap_user()
    elif args.method == "verify_exapnd_veiw":
        rc = uiobj.verify_exapnd_veiw()
    elif args.method == "delete_user_using_button":
        rc = uiobj.delete_user_using_button()
    elif args.method == "disable_apply_password_constraints_of_all_user":
        rc = uiobj.disable_apply_password_constraints_of_all_user()
    elif args.method == "add_user_with_sonicwall_administrator_and_check_admin_column":
        rc = uiobj.add_user_with_sonicwall_administrator_and_check_admin_column()
    elif args.method == "add_user_account_life_as_never_expires":
        rc = uiobj.add_user_account_life_as_never_expires()
    elif args.method == "add_user_with_sslvpn_service":
        rc = uiobj.add_user_with_sslvpn_service()
    elif args.method == "remove_user_with_sslvpn_service":
        rc = uiobj.remove_user_with_sslvpn_service()
    elif args.method == "add_user_with_guest_service_and_verify_tab":
        rc = uiobj.add_user_with_guest_service_and_verify_tab()
    elif args.method == "verify_book_mark_without_sslvpn_serviceuser":
        rc = uiobj.verify_book_mark_without_sslvpn_serviceuser()
    elif args.method == "add_bookmark":
        rc = uiobj.add_bookmark()
    elif args.method == "delete_bookmark":
        rc = uiobj.delete_bookmark()
    elif args.method == "ui_user_change_pw":
        rc = uiobj.ui_user_change_pw()
    elif args.method == "add_ldap_user_to_group":
        rc = uiobj.add_ldap_user_to_group()
