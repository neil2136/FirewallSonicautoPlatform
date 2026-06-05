
import argparse
import sys
import os
import pyotp
import json
import time
import constants
from runner.settings import logger


sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
print(sys.path)
from modules.ui.ui_wrapper import Browser



class FWPage(Browser):
    def __init__(self, url, user, pwd, scanner_page):
        self.url = url
        self.user = user
        self.password = pwd
        self.scanner_page_present = scanner_page


    def write_totp_to_file(self, totp_text, save_path):
        users = {self.user: totp_text}
        os.chdir('/tmp')
        # Print the current working directory
        print("Current working directory: {0}".format(os.getcwd()))
        json.dump(users, open(save_path, "w"))
        totp = pyotp.TOTP(totp_text).now()
        print(totp)
        return totp

    def read_totp_from_file(self, save_path):
        js = json.load(open(save_path, 'r'))
        m = js[self.user]
        print(m)
        return m

    def with_scanner_page_login(self):
        try:
            logger.info("Scanner page navigated......")
            self.click_element('xpath', "//a[normalize-space()='text code.']")
            time.sleep(20)
            logger.info("clicked text code successfully.")
            text_msg = self.get_attribute_value('xpath', "//div[@class='sw-popover__board__content__inner']", 'innerText')
            logger.info(text_msg)
            file_path = "/tmp/users.json"
            totp_code = self.write_totp_to_file(text_msg, file_path)
            self.set_input_text_field('xpath', "//input[@name='tfa']", totp_code)
            logger.info("Entered correct code successfully proceed")
            time.sleep(10)
            self.click_element('xpath', "//button[normalize-space()='OK']")
            time.sleep(10)
            self.click_element('xpath', "//button[@type='button']")
            logger.info("Verified continue to proceed")
            time.sleep(20)
            logger.info("portal page login is successful")
            self.read_totp_from_file(file_path)
            return True, "Success"
        except Exception as e:
            return False, str(e)

    def without_scanner_page_login(self):
        try:
            logger.info("2FA page Navigated..............")
            os.chdir('/tmp')
            # Print the current working directory
            print("Current directory: {0}".format(os.getcwd()))
            file_path = "/tmp/users.json"
            m = self.read_totp_from_file(file_path)
            logger.info(m)
            begin = time.time()
            totp_code = pyotp.TOTP(m).now()
            logger.info(totp_code)
            self.set_input_text_field('xpath', "//button[normalize-space()='OK']", totp_code)
            logger.info("Entered code successfully")
            end = time.time()
            print(f"Total time taken is {end - begin}")
            self.click_element('xpath', "//button[@type='button']")
            time.sleep(10)
            self.click_element('xpath', "//button[@type='button']")
            logger.info("Verified continue to proceed")
            time.sleep(20)
            logger.info("portal page login is successful")
            return True, "Success"
        except Exception as e:
            return False, str(e)

    def admin_login_page(self):
        try:
            logger.info("Login with admin privilages")
            self.click_element('xpath', "//button[@type='button']")
            logger.info("Clicked continue button successfully")
            self.quit()
            return True, "Success"
        except Exception as err:
            print("Exception \t: " + str(err))
            print("Failed to login")
            self.browser.close()
            return False, str(err)

    def enter_totp(self):
        try:
            logger.info(f"{self.user} {self.password}")
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("Logging in........")
            time.sleep(10)
            logger.info(f"Configure - Setting username: {constants.USERNAME_INPUT_FIELD}")
            self.set_input_text_field('xpath', constants.USERNAME_INPUT_FIELD, self.user)
            logger.info(f"Configure - Setting password: {constants.PASSWORD_INPUT_FIELD}")
            self.set_input_text_field('xpath', constants.PASSWORD_INPUT_FIELD, self.password)
            logger.info("Action - Clicked Login")
            self.click_element('xpath', constants.LOGIN_BUTTON)
            time.sleep(10)
            print("Login Test Flag.")
            print("self.scanner_page_present===", self.scanner_page_present)
            if self.scanner_page_present.lower() == "1":
                print("with scanner page")
                time.sleep(10)
                res = self.with_scanner_page_login()
            elif self.scanner_page_present.lower() == "2":
                print("without scanner page")
                time.sleep(10)
                res = self.without_scanner_page_login()
            elif self.scanner_page_present.lower() == "3":
                time.sleep(10)
                res = self.admin_login_page()
            elif self.scanner_page_present.lower() == "4":
                logger.info("Invalid totp")
                time.sleep(10)
                res = self.with_scanner_page_invalid_totp()      
            else:
                logger.info("Invalid Length")
                time.sleep(10)
                res = self.with_scanner_page_incorrect_totp()            
            print("RESP=====", res)
            if not res[0]:
                self.close_browser()
                return False, res[1]
            self.quit()
            return res[0], res[1]

        except Exception as err:
            print("Exception \t: " + str(err))
            print("Failed to launch")
            self.browser.close()
            return False, str(err)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Login UI')
    parser.add_argument('-url', type=str, dest='url', required=True, help='http server url')
    parser.add_argument('-user', type=str, dest='user', required=True, help='username to login')
    parser.add_argument('-pwd', type=str, dest='pwd', required=True, help='password to login')
    parser.add_argument('-scanner_page', type=str, dest='scanner_page', required=True, help='TOTP scanner page confirmation to login')
    args = parser.parse_args()
    ui_obj = FWPage(args.url, args.user, args.pwd, args.scanner_page)
    rc1 = ui_obj.enter_totp()

