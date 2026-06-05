import re
import sys
import argparse
import sys
import time
sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')

from runner.settings import Params, logger
from modules.ui.fw_page import FWPage
from runner.utils.assertion import Assertion


class UIPage(FWPage):

    def __init__(self):
        super().__init__('192.168.168.168', 'admin', Params.G_NEW_PASSWORD)

    def disable_lockout_warning(self):
        try:
            self.login_ui()
            time.sleep(2)
            self.navigate_to_device_page()
            self.navigate_to_section("icon-system", "Administration", labelName="Administration")
            self.navigate_to_tab("Login / Multiple Administrators")
            logger.info("Login / Multiple Administrators successfully loaded")

            selector = self.get_selenium_selector('xpath')
            element = self.browser.find_element(selector, "//input[@type='hidden' and @name='enableAdminLockout']")
            self.browser.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", element)
            logger.info("Action: Clicked toggle")
            time.sleep(2)

            flag = self.does_page_have_text("It is highly recommended to keep 'Admin/User Lockout' enabled and ensure that 'Log Event Only Without Lockout' remains disabled.")
            time.sleep(2)
            self.close_browser()
            return flag
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("ERR: Failed to verify warning when disabling lockout.")
    
    def lockout_warning_when_login(self):
        try:
            self.get_browser()
            self.go_to_url("https://" + self.ip)
            time.sleep(5)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
            logger.info("Action - Clicking Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(10)
            
            flag = self.does_page_have_text("Enhance Security with Login Attempt Lockout")
            flag &= self.does_page_have_text("Learn how to enable password complexity and how to enable account lockout.")
            self.close_browser()
            return flag
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("ERR: Failed to verify warning about enabling lockout.")

    def multiple_attempts_with_wrong_password(self, user="admin", password=Params.G_NEW_PASSWORD, timeout=0):
        try:
            self.get_browser()
            self.go_to_url("https://" + self.ip)
            time.sleep(5)
            logger.info("Logging in")
            for i in range(3):
                logger.info(f"Attempt {i+1} with wrong password")
                logger.info("Configure - Setting username")
                self.set_text_field('class', 'sw-textfield__wrapper__input', user)
                logger.info("Configure - Setting password")
                self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', "wrongpassword")
                logger.info("Action - Clicking Login")
                self.click_element('class', 'sw-login__trigger')
                time.sleep(5)
            
            # waiting till lockout period get expired
            logger.info("Waiting till lockout period expires!")
            time.sleep(timeout)
            
            # after lockout period over trying login
            logger.info("Trying login after lockout period")
            self.go_to_url("https://" + self.ip)
            time.sleep(5)
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', password)
            logger.info("Action - Clicking Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(10)
            flag = False
            if self.does_page_have_text("Enhance Security with Login Attempt Lockout") or \
                          self.does_page_have_text("You have logged in successfully!") or \
                          self.does_page_have_text("Automatic Firmware Updates"):
                flag=True
            
            self.close_browser()
            return flag
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("login failed")