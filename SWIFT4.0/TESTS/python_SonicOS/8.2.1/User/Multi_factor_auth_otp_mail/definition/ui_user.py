import re
import sys
import argparse
import sys
import os

sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
# sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
from runner.settings import logger
from modules.ui.ui_wrapper import Browser
# from modules.ui.ui_wrapper_test import Browser
from selenium.webdriver.common.by import By
from runner.utils.assertion import Assertion

import time
####################################################
from email.parser import Parser
from email.header import decode_header, Header
from email.utils import parseaddr
import poplib
import argparse


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def print_info(msg):
    # print from ,to ,subject
    for header in ['From', 'To', 'Subject']:
        value = msg.get(header, '')
        if value:
            if header == 'Subject':
                value = decode_str(value)
            else:
                hdr, addr = parseaddr(value)
                name = decode_str(hdr)
                value = u'%s <%s>' % (name, addr)
        print('%s: %s' % (header, value))
    # get content and attahments
    attachment_files = []
    try:
        for part in msg.walk():
            file_name = part.get_filename()
            contentType = part.get_content_type()
            mycode = part.get_content_charset()
            if file_name:
                h = Header(file_name)
                dh = decode_header(h)
                filename = dh[0][0]
                if dh[0][1]:
                    filename = decode_str(str(filename, dh[0][1]))
                attachment_files.append(filename)
                data = part.get_payload(decode=True)
                with open("/tmp/" + filename, 'wb') as f:
                    f.write(data)
                print('attachment is downloaded')
            elif contentType == 'text/plain':  # or contentType == 'text/html':
                data = part.get_payload(decode=True)
                content = data.decode(mycode)
                print(content)

        print('attachments:', attachment_files)
    except:
        print('failed to get attachemnts')


def get_email(pop3_server, user, password):
    try:
        server = poplib.POP3_SSL(pop3_server, 995)
        server.set_debuglevel(1)
        server.user(user)
        server.pass_(password)
        resp, mails, octets = server.list()
        print(mails)
        index = len(mails)
        print('unread email', index)
        resp, lines, octets = server.retr(index)
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        msg = Parser().parsestr(msg_content)
        print_info(msg)
        server.quit()
        return (msg)
    except Exception as err:
        print(err)


def delete_email(pop3_server, user, password):
    try:
        server = poplib.POP3_SSL(pop3_server, 995)
        server.set_debuglevel(1)
        server.user(user)
        server.pass_(password)
        resp, mails, octets = server.list()
        print(mails)
        index = len(mails)
        print('unread email', index)
        ret = ""
        for i in range(1, index + 1):
            print(i)
            ret = server.dele(i)
        print('6' * 60)
        print(ret)
        print('6' * 60)
        server.quit()
        return (ret)
    except Exception as err:
        print(err)


#########################################################

class FWPage(Browser):
    def __init__(self, url, user, pwd, fpwd=False, ula=False):
        self.url = url
        self.user = user
        self.password = pwd
        self.forced_pass = fpwd
        self.ula_check = ula

    def login_ui(self):
        try:
            self.get_browser()
            self.go_to_url(self.url)
            if self.ula_check:
                ula_policy_check = self.browser.find_element('xpath', "//*[contains(text(), 'Authentication Required')]")
                logger.info(ula_policy_check)
                if ula_policy_check:
                    logger.info("ULA policy page found.")
                    anchor = self.browser.find_element(By.LINK_TEXT, 'Click here to log in')
                    # Click the anchor tag
                    anchor.click()
                    time.sleep(5)
                else:
                    logger.info("ULA policy page not found.")
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
            logger.info("Action - Clicked Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(10)
            otp_login = self.get_element('class', 'login-ftr-otp__line')
            if not otp_login:
                logger.inf("OTP page not found")
                return False
            logger.info("OTP page found.")
            time.sleep(5)
            received_mail = get_email('172.17.1.5', 'test1', 'password')
            logger.info('8' * 60)
            logger.info(f'this is email resp {received_mail}')
            logger.info('8' * 60)
            login_otp = str(received_mail).split("\n")[-1]
            logger.info(f'OTP fetched from mail is {login_otp}')
            otp_text = self.does_element_exist('xpath', '//input[@name="tfa"]')
            logger.info(f'OTP text field exist: {otp_text}')
            logger.info("Enter 2FA OTP fetched from mail")
            self.set_text_field('xpath', "//input[@name='tfa']", login_otp)
            logger.info("Successfully entered 2FA OTP fetched from mail, clicking on OKAY.")
            time.sleep(2)
            ok_text = self.does_element_exist('xpath', '//button[contains(@class, "sw-button") and text() = "OK"]')
            logger.info(f'OKAY text field exist: {ok_text}')

            self.click_element('xpath', '//button[contains(@class, "sw-button") and text() = "OK"]')
            logger.info(f'Checking OTP...')
            time.sleep(3)
            
            logger.info("The OTP has been verified.")
            if self.forced_pass or self.forced_pass == 'True':
                logger.info('Continue to change password')
                self.click_element('xpath', '//button[contains(@class, "sw-button") and text() = "Continue"]')

                logger.info('Entering old and new passwords')
                self.set_text_field('xpath', '//input[@name="oldPw"]', self.password)
                self.set_text_field('xpath', '//input[@name="newPw"]', self.password + '1')
                self.set_text_field('xpath', '//input[@name="confirmPw"]', self.password + '1')
                self.click_element('xpath', '//button[contains(@class, "sw-button") and text() = "Change Password"]')
       
            logger.info("Firewall login is successfull")
            self.close_browser()
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")

    def close_browser(self):
        self.browser.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Login group service by UI')
    parser.add_argument('-url', type=str, dest='url', required=True, help='http server url')
    parser.add_argument('-user', type=str, dest='user', required=True, help='user to login group service')
    parser.add_argument('-pwd', type=str, dest='pwd', required=True, help='pwd to login group service')
    parser.add_argument('-fpwd', type=str, dest='fpwd', required=False, help='fpwd to login group service')
    parser.add_argument('-ula', type=str, dest='ula', required=False, help='ULA check')
    args = parser.parse_args()
    uiobj = FWPage(args.url, args.user, args.pwd, args.fpwd, args.ula)
    rc = uiobj.login_ui()