import re
import argparse
import sys
import os
import subprocess
import time

sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
from runner.settings import logger
from modules.ui.ui_wrapper import Browser, WebDriverWait, EC
from runner.utils.assertion import Assertion


class FWPage(Browser):
    def __init__(self, url, user, pwd, serverip, postauth):
        self.url = url
        self.user = user
        self.password = pwd
        self.serverip = serverip
        self.postauth = postauth

    def ping_server(self):
        p = subprocess.Popen(f"ping -c 5 {self.serverip}", stdout=subprocess.PIPE, shell=True)
        out = p.stdout.read().decode('gbk')
        logger.info(out)
        if re.search("100% packet loss", out, re.I):
            return False
        else:
            return True

    def login_ui(self):
        try:
            status = os.system('pkill firefox')
            logger.info(f"kill firefox result:{status}")
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            redirecturl = self.get_current_browser_url()
            logger.info(f"redirecturl:{redirecturl}")
            if self.url in redirecturl:
                logger.error("Test Case Fail")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
            logger.info("Action - Clicked Login")
            self.click_element('xpath', '//*[text()="LOG IN"]')
        except Exception as err:
            logger.warning("Exception \t: " + str(err))
            logger.error("Test Case Fail")
            Assertion.fail("Firewall login failed1")

    def check_error_info_in_login_page(self):
        try:
            logger.info("Check error appears.")
            if self.does_element_exist_now('css', '.sw-status-info__text__title'):
                contnet = self.get_element('css', '.sw-status-info__text__title').text
                if "Error" in contnet:
                    logger.error("Test Case Fail")
        except Exception as err:
            logger.warning("Exception \t: " + str(err))
            logger.error("Test Case Fail")
            Assertion.fail("Firewall login failed1")

    def login_complete(self):
        try:
            time.sleep(5)
            logger.info("Login Test Flag.")
            logger.info("Click Confirm Button.")
            urlafterlogin1 = self.get_current_browser_url()
            logger.info(f"url after login:{urlafterlogin1}")
            self.click_element('xpath', '//button')
            time.sleep(10)
            urlafterlogin = self.get_current_browser_url()
            logger.info(f"url after login:{urlafterlogin}")
            if self.postauth:
                logger.info(f"postauth is {type(self.postauth)} {self.postauth}")
                post_url = "http://172.17.1.10/"
                if post_url not in urlafterlogin:
                    logger.error("Test Case Fail1")
                if not self.ping_server():
                    logger.error("Test Case Fail2")
            else:
                if self.url not in urlafterlogin:
                    logger.error(f"{self.url}")
                    logger.error("Test Case Fail3")
                if not self.ping_server():
                    logger.error("Test Case Fail4")
        except Exception as err:
            logger.warning("Exception \t: " + str(err))
            logger.error("Test Case Fail5")
            Assertion.fail("Firewall login failed2")

    def redirect_ui_fail_confirm(self):
        try:
            status = os.system('pkill firefox')
            logger.info(f"kill firefox result:{status}")
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            redirecturl = self.get_current_browser_url()
            logger.info(f"redirecturl:{redirecturl}")
            if self.url in redirecturl:
                logger.error("Test Case Pass")
            else:
                logger.error("Test Case Fail")
        except Exception as err:
            logger.warning("Exception \t: " + str(err))
            logger.error("Test Case Fail")
            Assertion.fail("Firewall login failed3")

    def redirect_ui_success_confirm(self):
        try:
            status = os.system('pkill firefox')
            logger.info(f"kill firefox result:{status}")
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            redirecturl = self.get_current_browser_url()
            logger.info(f"redirecturl:{redirecturl}")
            if self.url in redirecturl:
                logger.error("Test Case Fail")
            else:
                logger.error("Test Case Pass")
        except Exception as err:
            logger.warning("Exception \t: " + str(err))
            logger.error("Test Case Fail")
            Assertion.fail("Firewall login failed3")

    def status_page_logout(self):
        try:
            self.switchToNewWindow()
            self.click_element('xpath', '//*[text()="Logout"]')
            if self.ping_server():
                logger.error("Test Case Fail")
            else:
                logger.info("User logout success")
        except Exception as err:
            logger.warning("Exception \t: " + str(err))
            logger.error("Test Case Fail")
            Assertion.fail("User logout failed")

    def login_external_auth_server(self):
        try:
            status = os.system('pkill firefox')
            logger.info(f"kill firefox result:{status}")
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
            logger.warning("Exception \t: " + str(err))
            logger.error("Test Case Fail")
            logger.warning("Firewall login failed4")

    def custom_authentication_url_verify(self):
        try:
            status = os.system('pkill firefox')
            logger.info(f"kill firefox result:{status}")
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("Check footer and header")
            time.sleep(2)
            redirecturl = self.get_current_browser_url()
            logger.info(f"redirecturl:{redirecturl}")
            if self.url in redirecturl:
                logger.error("Test Case Fail")
            header_src_value = self.get_attribute_value('css', '.login-ftr-login__top-message iframe', "src")
            logger.info(f"header src is:{header_src_value}")
            footer_src_value = self.get_attribute_value('css', '.login-ftr-login__bottom-footer-url-message iframe',
                                                        "src")
            logger.info(f"footer src is:{footer_src_value}")
            logger.info(f"source is {self.browser.page_source}")
            if header_src_value != "http://172.17.1.10/" or footer_src_value != "http://172.17.1.10/":
                logger.error("Test Case Fail")
        except Exception as err:
            logger.warning("Exception \t: " + str(err))
            logger.error("Test Case Fail")
            Assertion.fail("Firewall login failed1")

    def custom_authentication_text_verify(self):
        try:
            status = os.system('pkill firefox')
            logger.info(f"kill firefox result:{status}")
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("Check footer and header")
            time.sleep(2)
            redirecturl = self.get_current_browser_url()
            logger.info(f"redirecturl:{redirecturl}")
            if self.url in redirecturl:
                logger.error("Test Case Fail")
            header_verify = self.does_page_have_text("autotest_guest2")
            footer_verify = self.does_page_have_text("autotest_guest1")
            logger.info(f"source is {self.browser.page_source}")
            if not header_verify or not footer_verify:
                logger.error("Test Case Fail")
        except Exception as err:
            logger.warning("Exception \t: " + str(err))
            logger.error("Test Case Fail")
            Assertion.fail("Firewall login failed1")

    def no_custom_authentication_verify(self):
        try:
            status = os.system('pkill firefox')
            logger.info(f"kill firefox result:{status}")
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("Check footer and header")
            time.sleep(2)
            redirecturl = self.get_current_browser_url()
            logger.info(f"redirecturl:{redirecturl}")
            if self.url in redirecturl:
                logger.error("Test Case Fail")
            header_verify1 = self.does_element_exist_now('css', '.login-ftr-login__top-message iframe')
            header_verify2 = self.does_element_exist_now('css', '.login-ftr-login__top-message .login-ftr-login__top-header-message')
            footer_verify = self.does_element_exist_now('xpath', '//div[contains(@class, "login-ftr-login__bottom-footer")]')
            if header_verify1 and header_verify2 or footer_verify:
                logger.error("Test Case Fail")
        except Exception as err:
            logger.warning("Exception \t: " + str(err))
            logger.error("Test Case Fail")
            Assertion.fail("Firewall login failed1")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Login guest service by UI')
    parser.add_argument('-url', type=str, dest='url', required=True, help='http server url')
    parser.add_argument('-user', type=str, dest='user', required=True, help='user to login guest service')
    parser.add_argument('-pwd', type=str, dest='pwd', required=True, help='pwd to login guest service')
    parser.add_argument('-stepstop', type=str, dest='stepstop', required=True, help='which step to stop')
    parser.add_argument('-serverip', type=str, dest='serverip', required=True, help='The ip address of http server')
    parser.add_argument('-postauth', type=int, dest='postauth', required=True, help='The url after login redirected')
    args = parser.parse_args()
    postauth_flag = bool(args.postauth)
    uiobj = FWPage(args.url, args.user, args.pwd, args.serverip, postauth_flag)
    if args.stepstop == "redirect":
        uiobj.redirect_ui_fail_confirm()
    elif args.stepstop == "login":
        uiobj.login_ui()
        uiobj.login_complete()
    elif args.stepstop == "logout":
        uiobj.login_ui()
        uiobj.login_complete()
        uiobj.status_page_logout()
    elif args.stepstop == "login_page":
        uiobj.login_ui()
        uiobj.check_error_info_in_login_page()
    elif args.stepstop == "redirect_success":
        uiobj.redirect_ui_success_confirm()
    elif args.stepstop == "custom_auth_url":
        uiobj.custom_authentication_url_verify()
    elif args.stepstop == "custom_auth_text":
        uiobj.custom_authentication_text_verify()
    elif args.stepstop == "disable_custom_auth":
        uiobj.no_custom_authentication_verify()
