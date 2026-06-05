import re
import sys
import argparse
import sys
from datetime import datetime, timedelta
#sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
#print(sys.path)
from runner.settings import logger
from modules.ui.ui_wrapper import Browser
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from runner.utils.assertion import Assertion

import time



class FWPage(Browser):
    def __init__(self, method, url, user, pwd):
        self.method = method
        self.url = url
        self.user = user
        self.password = pwd
        

    def firewall_login(self):
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
            time.sleep(20)
            logger.info("Login Test Flag.")
            self.browser.find_element("xpath",
                    "/html/body/div/div/div[2]/div[2]/div[1]/div/div[1]/div[3]/div/div[1]/div[2]/span[2]").click()
            time.sleep(5)
            self.browser.find_element("xpath",
                                "//li[4]//ul[1]//li[1]//div[1]//div[2]").click()
            time.sleep(5)
            self.browser.find_element("xpath",
                                "//li[@class='sw-nav-group sw-nav-group--dark sw-nav-group--compact']//ul[@class='sw-nav-group__items sw-nav-group__items--nested-level-0']//li[1]//div[1]//div[2]").click()
            time.sleep(5)
            self.browser.find_element("xpath",
                                "//body/div[@class='sw-app sw-app--light sw-app--mode-app sw-typo-default sw-flexbox sw-flexbox--column fw-app-main']/div[@class='sw-app__view sw-flexbox__flex sw-flexbox sw-flexbox--row']/div[@class='sw-app__main sw-flexbox__flex']/div[@class='sw-app__main-inner sw-app__main-inner--fit sw-flexbox sw-flexbox--column']/div[@class='sw-app__content sw-app__content--fit sw-app__content--scroll sw-flexbox__flex']/div[@class='fw-app-main__content sw-flexbox']/div[@class='fw-app-content fw-app-content--no-padding fw-app-content--override-cell-icon-for-global-mode sw-flexbox__flex']/section[@class='fw-app-content__inner']/div[@class='fw-ftr-log-monitor sw-flexbox sw-flexbox--column']/div[@class='sw-content-toolbar sw-content-toolbar--light sw-typo-default sw-content-toolbar--no-border-bottom fw-ftr-log-monitor__toolbar fw-ftr-log-monitor__toolbar--inconsistent sw-flexbox__flex-none']/div[@class='sw-content-toolbar__inner sw-flexbox sw-flexbox--center-items']/div[@class='sw-scroll-view sw-flexbox sw-flexbox--column fw-ftr-log-monitor__toolbar-scroll-view sw-flexbox__flex']/div[@class='sw-flexbox__flex sw-flexbox']/div[@class='sw-scroll-view__view sw-flexbox__flex']/div[@class='sw-scroll-view__view__cont']/div[@class='sw-scroll-view__slot-wrapper']/div[@class='fw-ftr-log-monitor__toolbar-content sw-flexbox sw-flexbox--center-items']/span[11]/span[1]").click()
            time.sleep(5)
            self.browser.find_element("xpath","//div[contains(text(),'General')]").click()
            time.sleep(5)
            logger.info("Verify checkbox - time")
            check_box_time = self.browser.find_element("xpath","/html/body/div/div/div[2]/div[2]/div[2]/div[1]/div/section/div/div[4]/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div/div[1]/div[3]/div/div/div/div/div")

            if check_box_time.is_enabled():
                logger.info("time - checkbox is enabled") 
            time.sleep(5)

            check_box_time.click()

            if check_box_time.is_enabled():
                logger.info("time - checkbox is enabled")

            time.sleep(5)
            logger.info("Verify checkbox - message")
            check_box_message = self.browser.find_element("xpath",
                                                    "/html/body/div/div/div[2]/div[2]/div[2]/div[1]/div/section/div/div[4]/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div/div[8]/div[3]/div/div/div/div/div")

            if check_box_message.is_enabled():
                logger.info("message - checkbox is enabled")

            logger.info("Verify checkbox click")
            check_box_message.click()

            if check_box_message.is_enabled():
                logger.info("message - checkbox is enabled")

            time.sleep(5)
            self.browser.find_element("xpath","//button[normalize-space()='Cancel']").click()
            time.sleep(5)
            text_value = self.browser.find_element("xpath", "/html/body/div/div/div[2]/div[2]/div[2]/div[1]/div/section/div/div[3]/div[1]/div/div[2]")
            verify_rows = text_value.text.split()[1]
            if int(verify_rows) > 0:
                logger.info("Data is available and is visible")
            logger.info("True")
            return True                  
        except Exception as err:
            return False
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def refresh_log(self):
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
            time.sleep(20)
            logger.info("Login Test Flag.")
            self.browser.find_element("xpath",
                    "/html/body/div/div/div[2]/div[2]/div[1]/div/div[1]/div[3]/div/div[1]/div[2]/span[2]").click()
            time.sleep(5)
            self.browser.find_element("xpath",
                                "//li[4]//ul[1]//li[1]//div[1]//div[2]").click()
            time.sleep(5)
            self.browser.find_element("xpath",
                                "//li[@class='sw-nav-group sw-nav-group--dark sw-nav-group--compact']//ul[@class='sw-nav-group__items sw-nav-group__items--nested-level-0']//li[1]//div[1]//div[2]").click()
            time.sleep(5)
            self.browser.find_element("xpath", "//span[@class='sw-radio__fake-radio-button sw-flexbox__flex-none']").click()
            time.sleep(5)
            self.browser.find_element("xpath", "//input[@placeholder='Select Date-Time Range']").clear()
            time.sleep(5)
            
            # Configure refresh 1 sec
            current_time = datetime.now()
            new_time = current_time + timedelta(seconds=1)
            time_value = str(current_time.strftime("%d/%m/%Y %H:%M:%S")) + '->' + str(new_time.strftime("%d/%m/%Y %H:%M:%S"))
            for i in range(0, len(time_value)):
                self.browser.find_element("xpath", "//input[@placeholder='Select Date-Time Range']").send_keys(time_value[i])
            time.sleep(5)
            self.browser.find_element("xpath", "//span[@class='sw-icon__inner sw-font-icon icon-calendar-date-range']").click()
            time.sleep(5)
            self.browser.find_element("xpath",
                                "//span[@class='fw-ftr-log-monitor__refresh-message']//span[@class='sw-icon-button__inner sw-flexbox sw-flexbox--center-items sw-flexbox--center-justify']").click()
            time.sleep(10)

            self.browser.find_element("xpath", "//input[@placeholder='Select Date-Time Range']").clear()
            time.sleep(5)
            # Configure refresh 10 sec
            current_time = datetime.now()
            new_time = current_time + timedelta(seconds=10)
            time_value = str(current_time.strftime("%d/%m/%Y %H:%M:%S")) + '->' + str(new_time.strftime("%d/%m/%Y %H:%M:%S"))
            for i in range(0, len(time_value)):
                self.browser.find_element("xpath", "//input[@placeholder='Select Date-Time Range']").send_keys(time_value[i])
            time.sleep(5)
            self.browser.find_element("xpath", "//span[@class='sw-icon__inner sw-font-icon icon-calendar-date-range']").click()
            time.sleep(5)
            self.browser.find_element("xpath",
                                "//span[@class='fw-ftr-log-monitor__refresh-message']//span[@class='sw-icon-button__inner sw-flexbox sw-flexbox--center-items sw-flexbox--center-justify']").click()

            time.sleep(10)
            self.browser.find_element("xpath", "//input[@placeholder='Select Date-Time Range']").clear()
            time.sleep(5)
            # Configure refresh 999 sec
            current_time = datetime.now()
            new_time = current_time + timedelta(seconds=999)
            time_value = str(current_time.strftime("%d/%m/%Y %H:%M:%S")) + '->' + str(new_time.strftime("%d/%m/%Y %H:%M:%S"))
            for i in range(0, len(time_value)):
                self.browser.find_element("xpath", "//input[@placeholder='Select Date-Time Range']").send_keys(time_value[i])
            time.sleep(5)
            self.browser.find_element("xpath", "//span[@class='sw-icon__inner sw-font-icon icon-calendar-date-range']").click()
            time.sleep(5)
            self.browser.find_element("xpath",
                                "//span[@class='fw-ftr-log-monitor__refresh-message']//span[@class='sw-icon-button__inner sw-flexbox sw-flexbox--center-items sw-flexbox--center-justify']").click()
            logger.info("True")
        except Exception as err:
            return False
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def refresh_log_new(self):
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
            time.sleep(20)
            logger.info("Login Test Flag.")
            self.browser.find_element("xpath",
                    "/html/body/div/div/div[2]/div[2]/div[1]/div/div[1]/div[3]/div/div[1]/div[2]/span[2]").click()
            time.sleep(5)
            self.browser.find_element("xpath",
                                "//li[4]//ul[1]//li[1]//div[1]//div[2]").click()
            time.sleep(5)
            self.browser.find_element("xpath",
                                "//li[@class='sw-nav-group sw-nav-group--dark sw-nav-group--compact']//ul[@class='sw-nav-group__items sw-nav-group__items--nested-level-0']//li[1]//div[1]//div[2]").click()
            time.sleep(5)
            self.browser.find_element("xpath",
                                "//div[@class='sw-slider__btn sw-flexbox__flex-none']").click()            
            self.browser.execute_script("window.open('', '_blank');")
            self.browser.switch_to.window(self.browser.window_handles[1])
            self.go_to_url(self.url)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
            logger.info("Action - Clicked Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(20)
            logger.info("Login Test Flag.")
            self.browser.find_element("xpath","/html/body/div/div/div[2]/div[2]/div[1]/div/div[1]/div[3]/div/div[1]/div[2]/span[2]").click()
            time.sleep(5)
            self.browser.find_element("xpath","//li[4]//ul[1]//li[1]//div[1]//div[2]").click()
            time.sleep(5)
            self.browser.find_element("xpath",
                                "//div[@class='sw-nav-item__content sw-flexbox sw-flexbox--center-items sw-flexbox__flex']//span[contains(text(),'System Logs')]").click()

            text_val = self.browser.find_element("xpath", "//span[@class='sw-flexbox__flex sw-flexbox sw-flexbox--center-items sw-flexbox--center-justify']").text
            if text_val == 'Last 2 min':
                logger.info("True")
            return True
        except Exception as err:
            return False
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

    if args.method == "firewall_login":
        rc = uiobj.firewall_login()
    elif args.method == "refresh_log":
        rc = uiobj.refresh_log()
    elif args.method == "refresh_log_new":
        rc = uiobj.refresh_log_new()
