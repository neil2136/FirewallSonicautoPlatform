import re
import sys
import argparse
import sys
import os
import subprocess
import pyotp
import json
sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
import constants

print(sys.path)

from runner.settings import logger
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
            time.sleep(5)
            print("Current working directory: {0}".format(os.getcwd()))
            os.chdir('/tmp')
            # Print the current working directory
            print("Current working directory: {0}".format(os.getcwd()))
            # save_path ='/SWIFT4.0/TESTS/python_SonicOS/7.0.1/sslvpn/common_lib/'
            # file_name = "users.json"
            # file_path = os.path.join(save_path, file_name)
            save_path ='/tmp'
            file_name = "users.json"
            
            # save_path ='/SWIFT4.0/TESTS/python_SonicOS/7.0.1/sslvpn/common_lib/'
            # file_name = "users.json"
            file_path = os.path.join(save_path, file_name)
            data = open(file_path,"r")
            data_read_text = data.read()
            data.close()
            js = json.loads(data_read_text)
            m = js[self.user]
            logger.info(m)
            begin = time.time()
            totp = pyotp.TOTP(m)
            totp_text = totp.now()
            logger.info(totp_text)                
            self.set_text_field('xpath',"//input[@name='tfa']", m)
            logger.info("Entered code successfully")
            end = time.time()
            print(f"Total time taken is {end - begin}")
            self.click_element('xpath',"//button[text()='OK']")
            time.sleep(5)
            logger.info("portal page login is succesful")
            
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to launch bookmark")
            
    # def Invalid_otp(self):
    #     try:
    #         self.get_browser()
    #         self.go_to_url(self.url)
    #         logger.info("Logging in")
    #         logger.info("Configure - Setting username")
    #         self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
    #         logger.info("Configure - Setting password")
    #         self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
    #         logger.info("Action - Clicked Login")
    #         self.click_element('class', 'sw-login__trigger')
    #         time.sleep(10)
    #         logger.info("Login Test Flag.")
    #         time.sleep(15)
    #         self.set_text_field('xpath','/html/body/div/div/div/div[2]/div/div/div/div/div[2]/div/div/input','123456')
    #         logger.info("Entered code successfully")
    #     except Exception as err:
    #         logger.error("Exception \t: " + str(err))
    #         Assertion.fail("Entered otp is incorrect")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Login group service by UI')
    parser.add_argument('-url', type=str, dest='url', required=True, help='http server url')
    parser.add_argument('-user', type=str, dest='user', required=True, help='user to login group service')
    parser.add_argument('-pwd', type=str, dest='pwd', required=True, help='pwd to login group service')
    args = parser.parse_args()
    uiobj = FWPage(args.url, args.user, args.pwd)
    rc1 = uiobj.enter_otp()




