from runner.settings import logger
import re
import os
import sys
import time
from nose_parameterized import parameterized
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from modules.ui.ui_wrapper import Browser
from runner.utils.assertion import Assertion
from runner.settings import Params


class FWChangePassword(Browser):
    def __init__(self, ip='192.168.168.168', user ='admin', password='password', new_password=Params.G_NEW_PASSWORD):
        self.ip = ip
        self.user = user
        self.password = password
        self.new_password = new_password

    def change_password(self, login_type=None, ):
        logger.info('Kill firefox process')
        os.system('pkill firefox')
        try:
            retries = 0
            while retries < 2:
                try:
                    self.get_browser()
                    self.go_to_url("https://" + self.ip)
                    logger.info("Logging in")
                    logger.debug("Configure - Setting username")
                    self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
                    logger.debug("Configure - Setting password")
                    self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
                    logger.info("Action - Click Login button")
                    self.click_element('class', 'sw-login__trigger')
                    time.sleep(10)
                    if self.did_page_load_successfully():
                        if self.did_page_load_successfully():
                            logger.info('Loged in successfully with old password.')
                            current_url = self.browser.current_url
                            logger.info('Current url is: ' + current_url)
                            count = 0
                            if login_type == "after_resotre" :
                                if "retroVisit" in current_url and count < 12:
                                    time.sleep(5)
                                    current_url = self.browser.current_url
                                    logger.info('Current url is: ' + current_url)
                                    count += 1
                                    logger.info(count)                                
                                elif "update-password" in current_url and count < 12:
                                    time.sleep(5)
                                    if self.does_element_exist_now('xpath', '//div[contains(text(),"Your default password must be changed at first time login")]'):
                                        logger.info('Please enter the old password: ' + self.password)
                                        self.set_text_field('name', 'oldPw', self.password)
                                        logger.info('Please enter a new password: ' + self.new_password)
                                        self.set_text_field('name', 'newPw', self.new_password)
                                        logger.info('Please Confirm New Password: ' + self.new_password)
                                        self.set_text_field('name', 'confirmPw', self.new_password)
                                        logger.info("Action - Click Change Password button")
                                        time.sleep(10)
                                        self.click_element('xpath', '//div/button[text()="Change Password"]')
                                        logger.info('Loged in successfully.')
                                        time.sleep(40)
                                        try:
                                            if self.did_page_load_successfully():
                                                if self.did_page_load_successfully():
                                                    logger.info('Changed to new password successfully.')
                                                    current_url = self.browser.current_url
                                                    logger.info('Current url is: ' + current_url)
                                                    time.sleep(20)
                                                    if "launchWizard" in current_url:
                                                        logger.info("Click click here button to login FW.")
                                                        if self.does_element_exist_now('xpath', '//div[contains(text(),"To manually configure SonicWall")]'):
                                                            self.click_element('xpath', '//div[contains(text(),"To manually configure SonicWall")]/a[contains(text(),"click here")]')
                                                            logger.info("Login FW Successfully after changing new password.")
                                                            
                                        except Exception as err:
                                            logger.error(f'Error! Reason: --> {err}')
                                            Assertion.fail("Action - Unable to click click here button")

                        # if "launchWizard" in current_url:
                        #         if self.does_element_exist_now('xpath', '//div[contains(text(),"To manually configure SonicWall")]'):
                        #             self.click_element('xpath', '//div[contains(text(),"To manually configure SonicWall")]/a[text()="click here."]')
                        self.close_browser()
                    return True
                except Exception as err:
                    retries = retries + 1
                    if retries < 2:
                        self.close_browser()
                        continue
                    else:
                        logger.info("Exception \t: " + str(err))
                        Assertion.fail("Action - Unable to Login")
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")

if __name__ == '__main__':
    nav = FWChangePassword()
    nav.change_password(login_type='after_resotre')
