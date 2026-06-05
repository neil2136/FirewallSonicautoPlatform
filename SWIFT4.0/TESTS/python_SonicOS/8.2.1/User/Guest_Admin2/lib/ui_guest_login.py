import re
import sys
import argparse
import sys

sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
print(sys.path)
from runner.settings import logger
from modules.ui.ui_wrapper import Browser
from modules.ui.fw_page import FWPage
from runner.utils.assertion import Assertion

import time


class FWPage_local(FWPage):
    def __init__(self, url, user, pwd):
        self.url = url
        self.user = user
        self.password = pwd

    def verify_toggle_button(self, attrib, attrib_val):
        if attrib_val.isdigit() != True:
            class_value = self.get_attribute_value(attrib, attrib_val, 'class')
            if "sw-toggle--off" in class_value:
                return "OFF"
            else:
                return "ON"

    def logout_guest_admin(self):
        self.click_element('xpath', "//span[@class='sw-avatar__initials']")
        self.click_element('xpath', "//span[contains(text(),'End Management')]")
        self.switchToNewWindow()
        self.click_element('xpath', "//a[normalize-space()='Logout']")
        time.sleep(3)

        self.switchToDefaultWindow()
        self.close_browser()
        self.quit()

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
            self.click_element('class', 'sw-login__trigger')
            time.sleep(10)
            logger.info("Login Test Flag.")
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")


    def login_guest_admin_non_config(self):
        try:
            self.login_ui()

            self.wait_for_page_data_to_be_rendered()
            time.sleep(5)

            error_msg = self.get_element('xpath', "//div[@class='login-ftr-confirm__line sw-typo-heading-4']").text
            expected_msg = "You have logged in successfully!"
            if expected_msg not in error_msg:
                self.close_browser()
                self.quit()
                return False
            self.click_element('xpath', "//button[@type='button']")
            time.sleep(5)
            self.switchToNewWindow()
            self.click_element('xpath', "/html/body/div/div/div/div[3]/div[3]/div[2]/button")

            time.sleep(3)
            self.switchToDefaultWindow()
            self.wait_for_page_data_to_be_rendered()
            if not self.does_page_have_text("Cannot preempt existing administator"):
                print("Cannot preempt admin")
                time.sleep(5)
            self.click_element('xpath', "//button[@type='button']")
            self.wait_for_page_data_to_be_rendered()
            time.sleep(30)

            self.toggle_button('xpath', "/html/body/div/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/div", True)
            config_value = self.verify_toggle_button('xpath', "/html/body/div/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/div")
            if config_value == "ON":
                self.logout_guest_admin()
                return False

            self.logout_guest_admin()
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.info("Guest admin config change failed")
            self.logout_guest_admin()
            return False

    def login_admin_config_mode(self):
        try:
            self.login_ui()

            self.wait_for_page_data_to_be_rendered()
            time.sleep(5)

            error_msg = self.get_element('xpath', "//div[@class='login-ftr-confirm__line sw-typo-heading-4']").text
            expected_msg = "You have logged in successfully!"
            if expected_msg not in error_msg:
                self.close_browser()
                self.quit()
                return False
            self.click_element('xpath', "//button[@type='button']")
            time.sleep(5)
            self.switchToNewWindow()
            self.click_element('xpath', "/html/body/div/div/div/div[3]/div[3]/div[2]/button")

            time.sleep(3)
            self.switchToDefaultWindow()
            self.wait_for_page_data_to_be_rendered()
            time.sleep(10)

            self.toggle_button('xpath', "/html/body/div/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/div", True)
            config_value = self.verify_toggle_button('xpath', "/html/body/div/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/div")
            if config_value != "ON":
                self.logout_guest_admin()
                return False

            self.logout_guest_admin()
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.info("Guest admin login failed")
            self.logout_guest_admin()
            return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Login guest service by UI')
    parser.add_argument('-url', type=str, dest='url', required=True, help='http server url')
    parser.add_argument('-user', type=str, dest='user', required=True, help='user to login guest service')
    parser.add_argument('-pwd', type=str, dest='pwd', required=True, help='pwd to login guest service')
    parser.add_argument('-method', type=str, dest='method', required=True, help='method to login guest service')
    args = parser.parse_args()
    uiobj = FWPage_local(args.url, args.user, args.pwd)
    if args.method == "login_guest_admin_non_config":
        rc = uiobj.login_guest_admin_non_config()
        print(rc)
    else:
        rc = uiobj.login_admin_config_mode()
        print(rc)
