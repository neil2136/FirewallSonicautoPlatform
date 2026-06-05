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


class UI_Test(FWPage):

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

    def login_ui(self, url, user, password):
        try:
            self.get_browser()
            self.go_to_url(url)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', password)
            logger.info("Action - Clicked Login")
            # self.wait_for_element_to_be_visible('class', 'sw-login__trigger')
            self.click_element('class', 'sw-login__trigger')
            time.sleep(10)
            logger.info("Login Test Flag.")
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")

    def verify_password_constraints(self, user, password):
        try:
            url = "https://192.168.168.168"
            self.login_ui(url, user, password)
            pass_try = ['111', "1111111"]
            expected_error_msg = ["Password is too short", "Password length must be at least 5 and contains at least 1 lower case letter, 1 numeric character"]

            self.wait_for_page_data_to_be_rendered()
            time.sleep(5)
            password_change_diag = self.get_element('xpath', "//div[@class='login-ftr-update-pw__line sw-typo-heading-4']").text
            expected_pass = "Your password is too simple and must be changed"
            if expected_pass not in password_change_diag:
                logger.info("Password change dialog box did not appear")
                self.close_browser()
                self.quit()
                return False
            for i in range(2):
                self.set_text_field('xpath', "//input[@name='oldPw']", password)
                self.set_text_field('xpath', "//input[@name='newPw']", pass_try[i])
                self.set_text_field('xpath', "//input[@name='confirmPw']", pass_try[i])
                self.click_element('xpath', "//button[normalize-space()='Change Password']")
                time.sleep(3)
                error_msg = self.get_element('xpath', "//p[@class='sw-status-info__text__message__para']").text
                self.click_element('xpath', "//button[normalize-space()='OK']")
                if expected_error_msg[i] not in error_msg:
                    self.close_browser()
                    self.quit()
                    return False

            self.close_browser()
            self.quit()
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.info("Password verification failed")
            self.close_browser()
            self.quit()
            return False

    def verify_password_change(self, user, password, new_password):
        try:
            url = "https://192.168.168.168"
            self.login_ui(url, user, password)

            self.wait_for_page_data_to_be_rendered()
            time.sleep(5)
            password_change_diag = self.get_element('xpath', "//div[@class='login-ftr-update-pw__line sw-typo-heading-4']").text
            expected_pass = "Your password is too simple and must be changed"
            if expected_pass not in password_change_diag:
                logger.info("Password change dialog box did not appear")
                self.close_browser()
                self.quit()
                return False

            self.set_text_field('xpath', "//input[@name='oldPw']", password)
            self.set_text_field('xpath', "//input[@name='newPw']", new_password)
            self.set_text_field('xpath', "//input[@name='confirmPw']", new_password)
            self.click_element('xpath', "//button[normalize-space()='Change Password']")
            time.sleep(10)
            self.wait_for_page_data_to_be_rendered()
            error_msg = self.get_element('xpath', "//div[@class='login-ftr-confirm__line sw-typo-heading-4']").text
            expected_msg = "You have logged in successfully!"
            if expected_msg not in error_msg:
                self.close_browser()
                self.quit()
                return False
            self.click_element('xpath', "//button[@type='button']")
            time.sleep(5)
            self.switchToNewWindow()
            self.click_element('xpath', "//a[normalize-space()='Logout']")
            time.sleep(3)


            self.switchToDefaultWindow()
            self.close_browser()
            self.quit()
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.info("Password verification failed")
            self.close_browser()
            self.quit()
            return False

    def change_password_constraints_to_default(self):
        try:
            url = "https://192.168.168.168"
            user = "admin"
            password = "sonicauto"
            self.login_ui(url, user, password)
            self.navigate_to_system_administration()
            self.click_element('xpath', "//span[normalize-space()='Login / Multiple Administrators']")
            self.click_element('xpath', "/html/body/div/div/div[2]/div[2]/div[2]/div[1]/div/section/div/div[1]/div[2]/div/div/div/div[1]/div[2]/div/div[1]/div/div[6]/div/div[2]/div/div[1]")
            self.click_element('xpath', "//span[normalize-space()='None']")
            self.click_element('xpath', "//button[normalize-space()='Accept']")

            self.logout_ui()
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.info("Password verification failed")
            self.logout_ui()
            return False

    def login_external_auth_server(self):
        try:
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("Logging in")
            logger.debug("Configure - username")
            self.set_text_field('id', 'txtName', self.user)
            logger.debug("Configure - Setting password")
            self.set_text_field('id', 'txtPassword', self.password)
            logger.info("Action - Clicked Login")
            self.click_element('id', 'btnSubmit')
            html_code = self.get_page_source()
            logger.info(html_code)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")

    def login_guest_admin_non_config(self, user, password):
        try:

            url = "https://192.168.168.168"
            self.login_ui(url, user, password)

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
            self.click_element('xpath', "//button[@type='button']")

            time.sleep(3)
            self.switchToDefaultWindow()
            if not self.does_page_have_text("Cannot preempt existing administator"):
                time.sleep(5)
            self.click_element('xpath', "//button[@type='button']")
            self.wait_for_page_data_to_be_rendered()
            time.sleep(5)

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
