import re
import sys
import argparse
import sys
import time

sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
print(sys.path)
# from modules.ui.ui_wrapper_test import Browser #headless argument commented
from modules.ui.ui_wrapper import Browser  #running with headless without opening UI
from runner.utils.assertion import Assertion
from runner.settings import Params, logger

G_PASSWORD_NEW = Params.G_NEW_PASSWORD

class FWPage(Browser):
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password

    def login(self):
        try:
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_text_field('xpath', '//input[@name="username"]', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('xpath', '//input[@name="password"]', self.password)
            logger.info("Action - Clicked Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(20)

            if self.browser.find_element('xpath', '//input[@name="oldPw"]'):
                logger.info("Password change required, updating password.")
                self.set_text_field('xpath', '//input[@name="oldPw"]', self.password)
                new_password = G_PASSWORD_NEW
                self.set_text_field('xpath', '//input[@name="newPw"]', new_password)
                self.set_text_field('xpath', '//input[@name="confirmPw"]', new_password)
                self.click_element('xpath', '//button[text()="Change Password"]')
                time.sleep(5)
                
                # Check for login success message
                if self.browser.find_element('xpath', '//div[text()="You have logged in successfully!"]'):
                    logger.info("Password changed and logged in successfully!")
                    self.password = new_password
                    return True, "Password updated and login successful"

            logger.info("Login successful.")
            return True, "Logged in successfully"
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")
            return False, str(err)
        
    def login_failed(self):
        try:
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_text_field('xpath', '//input[@name="username"]', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('xpath', '//input[@name="password"]', self.password)
            logger.info("Action - Clicked Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(20)
            
            # Check for login error message
            resp = self.does_page_have_text("User login denied - User has no privileges for login from that location")
            if resp == True:
                logger.info("Login failed: User has no privileges for login from that location")
                return False, "User login denied - No privileges for login from that location"
            # if self.browser.find_element('xpath', "//p[text()='User login denied - User has no privileges for login from that location. 2 more login attempts before lockout.']"):
            #     logger.info("Login failed: User has no privileges for login from that location")
            #     return False, "User login denied - No privileges for login from that location"
            logger.info("Login successful.")
            return True, "Logged in successfully"
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")