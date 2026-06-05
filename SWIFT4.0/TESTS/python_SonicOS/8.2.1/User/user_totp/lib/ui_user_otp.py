
import re

import sys
import argparse
import sys
import os
import subprocess
import pyotp
import json
sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
print(sys.path)

from runner.settings import logger
#from ui_wrapper import Browser
from modules.ui.ui_wrapper import Browser
from runner.utils.assertion import Assertion

import time


class FWPage(Browser):
    def __init__(self, url, user, pwd):
        self.url = url
        self.user = user
        self.password = pwd


    def enter_otp(self):
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
            time.sleep(10)
            self.click_element('xpath', '//a[normalize-space()="text code."]')
            logger.info("clicked text code succesfully.")
            text =self.get_attribute_value('xpath','//div[@class="sw-popover__board__content__inner"]','innerText')
            logger.info(text)
            users = {}
            users[self.user] = text
            print("Current working directory: {0}".format(os.getcwd()))
            os.chdir('/tmp')
            print("Current working directory: {0}".format(os.getcwd()))
            save_path ='/tmp'
            file_name = "users.json"
            file_path = os.path.join(save_path, file_name)
            f = open(file_path, "w")
            m = json.dump(users, f)
            f.close()              
            totp = pyotp.TOTP(text)
            m = totp.now()
            logger.info(m)
            self.set_text_field('xpath', '//input[@name="tfa"]', m)
            logger.info("Entered correct code succesfully proceed")
            time.sleep(5)
            self.click_element('xpath','//button[normalize-space()="OK"]')
            logger.info("succesfully entered correct code")
            time.sleep(5)
            emer_text =self.get_element('xpath','//span[@class="login-ftr-totp__emphasis"]')
            text_content = emer_text.text
            logger.info(text_content)
            time.sleep(5)
            self.click_element('xpath','//button[@type="button"]')
            time.sleep(5)
            # self.click_element('xpath','//button[@type="button"]')
            # logger.info("portal page logout is succesful")
            time.sleep(10)
            self.set_input_text_field('xpath', '//input[@name="oldPw"]', self.password)
            time.sleep(5)
            self.set_input_text_field('xpath', '//input[@name="newPw"]', self.password + '1')
            time.sleep(5)
            self.set_input_text_field('xpath', '//input[@name="confirmPw"]', self.password + '1')
            time.sleep(5)
            self.click_element("xpath", '//*[text()="Change Password"]')            
            logger.info("Action - Clicked continue and Password changed succesfully")

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to launch enter totp code")





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Login group service by UI')
    parser.add_argument('-url', type=str, dest='url', required=True, help='http server url')
    parser.add_argument('-user', type=str, dest='user', required=True, help='user to login group service')
    parser.add_argument('-pwd', type=str, dest='pwd', required=True, help='pwd to login group service')
    args = parser.parse_args()
    uiobj = FWPage(args.url, args.user, args.pwd)
    rc1 = uiobj.enter_otp()


