import re
import sys
import os
import argparse
import sys
from datetime import datetime, timedelta
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Lockout_User_Accounts')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
# print(sys.path)
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

    def navigate_to_device_adminstration_section(self):
        try:
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('xpath', "//input[@placeholder='Enter your password...']", self.password)
            logger.info("Action - Clicked Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(10)
            self.click_element('xpath', "//button[normalize-space()='Cancel']")
            time.sleep(5)
            self.click_element('xpath', "//span[@class='sw-icon__inner sw-font-icon icon-monitor']")
            time.sleep(5)
            self.click_element('xpath',
                               "//div[@class='sw-nav-item__content sw-flexbox sw-flexbox--center-items sw-flexbox__flex']//span[contains(text(),'Administration')]")
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def login_using_local_user(self):
        try:
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', 'testuser')
            logger.info("Configure - Setting password")
            self.set_text_field('xpath', "//input[@placeholder='Enter your password...']", 'password')
            logger.info("Action - Clicked Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(5)
            self.click_element('xpath', "//button[@type='button']")
            time.sleep(10)
            return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def login_using_guest_user(self):
        try:
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', 'testguestuser')
            logger.info("Configure - Setting password")
            self.set_text_field('xpath', "//input[@placeholder='Enter your password...']", 'password')
            logger.info("Action - Clicked Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(5)
            self.click_element('xpath', "//button[@type='button']")
            time.sleep(10)
            return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def invalid_login_using_local_user(self):
        try:
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', 'testuser')
            logger.info("Configure - Setting password")
            self.set_text_field('xpath', "//input[@placeholder='Enter your password...']", 'passwordd')
            logger.info("Action - Clicked Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(5)
            self.close_browser()
            return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def logout_using_local_user(self):
        try:
            self.switchToNewWindow()
            anchor = self.browser.find_element(By.LINK_TEXT, 'Logout')
            anchor.click()
            return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def tc1_check_user_account_lock_account_button(self):
        try:
            self.navigate_to_device_adminstration_section()
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Login / Multiple Administrators']")
            logger.info('Checking whether button of enable administrator/user account lockout exist')
            user_lockout = self.does_page_have_text("Admin/user lockout")
            user_account_lockout = self.does_page_have_text("Local admin/user account lockout")
            if user_lockout == True and user_account_lockout == True:
                logger.info(' enable administrator/user account lockout Button exist ')
                logger.info('True')
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def tc2_Lockout_time_due(self):
        try:
            logger.info('Check if we can login using local user')
            loc_usr = self.login_using_local_user()
            loc_usr_logout = self.logout_using_local_user()
            self.get_browser()
            self.go_to_url(self.url)
            for i in range(0, 7):
                logger.info("Logging in")
                self.set_text_field('class', 'sw-textfield__wrapper__input', 'testuser')
                self.set_text_field('xpath', "//input[@placeholder='Enter your password...']", 'passwordd')
                self.click_element('class', 'sw-login__trigger')
            logger.info("Check if User locked out message is displayed")
            lock_msg = self.does_page_have_text('User is locked out')
            logger.info('Wating for 5 mins')
            time.sleep(300)
            logger.info('Loggin in with valid password')
            loc_usr1 = self.login_using_local_user()
            if loc_usr == True and loc_usr_logout == True and lock_msg == True and loc_usr1 == True:
                logger.info('Verification Successful')
                logger.info('True')
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def tc3_Unlock_User_by_GUI(self):
        try:
            logger.info('Check if we can login using local user')
            loc_usr = self.login_using_local_user()
            loc_usr_logout = self.logout_using_local_user()
            self.get_browser()
            self.go_to_url(self.url)
            for i in range(0, 7):
                logger.info("Logging in")
                self.set_text_field('class', 'sw-textfield__wrapper__input', 'testuser')
                self.set_text_field('xpath', "//input[@placeholder='Enter your password...']", 'passwordd')
                self.click_element('class', 'sw-login__trigger')
            logger.info("Check if User locked out message is displayed")
            lock_msg = self.does_page_have_text('User is locked out')
            logger.info("Unlocking the user through GUI")
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('xpath', "//input[@placeholder='Enter your password...']", self.password)
            logger.info("Action - Clicked Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(10)
            self.click_element('xpath', "//button[normalize-space()='Cancel']")
            time.sleep(5)
            self.click_element('xpath', "//span[@class='sw-icon__inner sw-font-icon icon-monitor']")
            time.sleep(5)
            self.click_element('xpath', "//span[@class='sw-icon__inner sw-font-icon icon-user']")
            self.click_element('xpath',
                               "//li[@class='sw-nav-group sw-nav-group--dark sw-nav-group--compact']//ul[@class='sw-nav-group__items sw-nav-group__items--nested-level-0']//li[1]//div[1]//div[2]//span[1]")
            self.click_element('xpath', "//span[normalize-space()='Locked Out Users']")
            logger.info('Unlockig now')
            self.move_to_the_element('xpath', "//div[normalize-space()='testuser']")
            self.click_element('xpath', "//span[@class='sw-icon__inner sw-font-icon icon-unlocked']")

            logger.info('Verifying that local user can login after unlockig account')
            loc_usr1 = self.login_using_local_user()
            if loc_usr == True and loc_usr_logout == True and lock_msg == True and loc_usr1 == True:
                logger.info('Verification Successful')
                logger.info('True')
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def tc4_check_Log_event_only_without_lockout_button(self):
        try:
            self.navigate_to_device_adminstration_section()
            time.sleep(5)
            self.click_element('xpath', "//span[normalize-space()='Login / Multiple Administrators']")
            logger.info('Checking whether button of Log event only without lockout exist')
            log_event_only_button = self.does_page_have_text("Log event only without lockout")
            if log_event_only_button == True:
                logger.info(' Log event only without lockout Button exist ')
                logger.info('True')
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def tc5_tsr_file_check_lockout_user_account(self):
        try:
            logger.info('Check if we can login using local user')
            loc_usr = self.login_using_local_user()
            loc_usr_logout = self.logout_using_local_user()
            self.get_browser()
            self.go_to_url(self.url)
            for i in range(0, 7):
                logger.info("Logging in")
                self.set_text_field('class', 'sw-textfield__wrapper__input', 'testuser')
                self.set_text_field('xpath', "//input[@placeholder='Enter your password...']", 'passwordd')
                self.click_element('class', 'sw-login__trigger')
                time.sleep(2)
            logger.info("Check if User locked out message is displayed")
            lock_msg = self.does_page_have_text('User is locked out')
            if loc_usr == True and lock_msg == True:
                logger.info('Verification Successful')
                logger.info('True')
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def tc6_Verify_local_user_supported_for_this_feature(self):
        try:
            logger.info('Verify local user supported for this feature')
            loc_usr = self.login_using_local_user()
            loc_usr_logout = self.logout_using_local_user()
            self.get_browser()
            self.go_to_url(self.url)
            for i in range(0, 7):
                logger.info("Logging in")
                self.set_text_field('class', 'sw-textfield__wrapper__input', 'testuser')
                self.set_text_field('xpath', "//input[@placeholder='Enter your password...']", 'passwordd')
                self.click_element('class', 'sw-login__trigger')
                # if self.does_element_exist_now('xpath', "//span[@class='sw-icon__inner sw-font-icon icon-close-thin']"):
                #     self.click_element('xpath', "//span[@class='sw-icon__inner sw-font-icon icon-close-thin']")
                # time.sleep(2)
            logger.info("Check if User locked out message is displayed")
            lock_msg = self.does_page_have_text('User is locked out')
            print('lock_masg', lock_msg)
            if lock_msg == True:
                logger.info('Verification Successful')
                logger.info('True')
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def tc7_Locked_out_User_Account_list_check(self):
        try:
            logger.info('Locked out User Account list check')
            loc_usr = self.login_using_local_user()
            loc_usr_logout = self.logout_using_local_user()
            self.get_browser()
            self.go_to_url(self.url)
            for i in range(0, 7):
                logger.info("Logging in")
                self.set_text_field('class', 'sw-textfield__wrapper__input', 'testuser')
                self.set_text_field('xpath', "//input[@placeholder='Enter your password...']", 'passwordd')
                self.click_element('class', 'sw-login__trigger')
                time.sleep(2)
            logger.info("Check if User locked out message is displayed")
            lock_msg = self.does_page_have_text('User is locked out')
            logger.info("Check if locked user is present in Locked out User Account list")
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('xpath', "//input[@placeholder='Enter your password...']", self.password)
            logger.info("Action - Clicked Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(10)
            self.click_element('xpath', "//button[normalize-space()='Cancel']")
            time.sleep(5)
            self.click_element('xpath', "//span[@class='sw-icon__inner sw-font-icon icon-monitor']")
            time.sleep(5)
            self.click_element('xpath', "//span[@class='sw-icon__inner sw-font-icon icon-user']")
            self.click_element('xpath',
                               "//li[@class='sw-nav-group sw-nav-group--dark sw-nav-group--compact']//ul[@class='sw-nav-group__items sw-nav-group__items--nested-level-0']//li[1]//div[1]//div[2]//span[1]")
            self.click_element('xpath', "//span[normalize-space()='Locked Out Users']")

            locked_user = self.does_page_have_text('testuser')
            print('locked_user', locked_user)
            if loc_usr == True and loc_usr_logout == True and lock_msg == True and locked_user == True:
                logger.info('Verification Successful')
                logger.info('True')
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def tc8_Verify_guest_account_login_test(self):
        try:
            logger.info('Verify Guest account login test')
            guest_usr = self.login_using_guest_user()
            guest_usr_logout = self.logout_using_local_user()
            self.get_browser()
            self.go_to_url(self.url)
            for i in range(0, 7):
                logger.info("Logging in")
                self.set_text_field('class', 'sw-textfield__wrapper__input', 'testguestuser')
                self.set_text_field('xpath', "//input[@placeholder='Enter your password...']", 'passwordd')
                self.click_element('class', 'sw-login__trigger')
                time.sleep(2)
            logger.info("Check if User locked out message is displayed")
            lock_msg = self.does_page_have_text('User is locked out')

            if guest_usr == True and guest_usr_logout == True and lock_msg == True:
                logger.info('Verification Successful')
                logger.info('True')
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def tc13_Lockout_log_event(self):
        try:
            logger.info('Check if we can login using local user')
            loc_usr = self.login_using_local_user()
            loc_usr_logout = self.logout_using_local_user()
            self.get_browser()
            self.go_to_url(self.url)
            for i in range(0, 6):
                self.set_text_field('class', 'sw-textfield__wrapper__input', 'testuser')
                self.set_text_field('xpath', "//input[@placeholder='Enter your password...']", 'passwordd')
                self.click_element('class', 'sw-login__trigger')
                if self.does_element_exist_now('xpath', "//span[@class='sw-icon__inner sw-font-icon icon-close-thin']"):
                    self.click_element('xpath', "//span[@class='sw-icon__inner sw-font-icon icon-close-thin']")
            logger.info("Check if User locked out message is displayed")
            lock_msg = self.does_page_have_text('User is locked out')
            if loc_usr == True and loc_usr_logout == True and lock_msg == False:
                logger.info('Verification Successful')
                logger.info('True')
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def tc13_1_Lockout_log_event_login_as_local_user(self):
        try:
            loc_usr1 = self.login_using_local_user()
            if loc_usr1 == True:
                logger.info('Verification Successful')
                logger.info('True')

        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def tc14_Verify_sslvpn_login_test(self):
        try:
            logger.info('Verify SSLVPN account login test')
            self.get_browser()
            self.go_to_url(self.url)
            for i in range(0, 6):
                logger.info("Logging in")
                self.set_text_field('class', 'sw-textfield__wrapper__input', 'sslvpntest')
                self.set_text_field('xpath', "//input[@placeholder='Enter your password...']", 'P@ssw0rd')
                self.click_element('class', 'sw-login__trigger')
                time.sleep(2)
            logger.info("Check if User locked out message is displayed")
            lock_msg = self.does_page_have_text('User is locked out')

            if lock_msg == True:
                logger.info('Verification Successful')
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
        rc = uiobj.tc1_check_user_account_lock_account_button()
    elif args.method == "tc2":
        rc = uiobj.tc2_Lockout_time_due()
    elif args.method == "tc3":
        rc = uiobj.tc3_Unlock_User_by_GUI()
    elif args.method == "tc4":
        rc = uiobj.tc4_check_Log_event_only_without_lockout_button()
    elif args.method == "tc5":
        rc = uiobj.tc5_tsr_file_check_lockout_user_account()
    elif args.method == "tc6":
        rc = uiobj.tc6_Verify_local_user_supported_for_this_feature()
    elif args.method == "tc7":
        rc = uiobj.tc7_Locked_out_User_Account_list_check()
    elif args.method == "tc8":
        rc = uiobj.tc8_Verify_guest_account_login_test()
    elif args.method == "tc13":
        rc = uiobj.tc13_Lockout_log_event()
    elif args.method == "tc13_1":
        rc = uiobj.tc13_1_Lockout_log_event_login_as_local_user()
    elif args.method == "tc14":
        rc = uiobj.tc14_Verify_sslvpn_login_test()
