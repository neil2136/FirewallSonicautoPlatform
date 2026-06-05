import pyotp

from inputs.constants import *
from libs.browser import Browser
from pytest_resources.common_require import *
from libs.mail import MailModule
from libs.screen_resolution import DEVMODE


class SSLVPNPortal(Browser):
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    # Log in to SSL-VPN Portal with Username/Password
    def sslvpn_portal_unpw_login(self, expected_failure=False):
        try:
            self.get_browser()
            self.maximize_window()
            self.go_to_url(self.url)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_element('text_field', 'name', 'username', self.username)
            logger.info("Configure - Setting password")
            self.set_element('text_field', 'name', 'password', self.password)
            logger.info("Action - Click Login")
            self.set_element('button', 'class', 'sw-login__trigger', "LOG IN")
            if expected_failure:
                self.wait_for_text(fw_unpw_login_failure_message)
                logger.info("SSL-VPN Portal login failed as expected...")
            else:
                self.wait_for_text("NetExtender App")
                logger.info("SSL-VPN Portal login Successful...")
                self.click_element('xpath', '/html/body/div/div/div/div[3]/div[3]/div/button')
                self.wait_for_text("Are you sure you want to logout?  All active connections will be terminated.")
                self.click_element('xpath', '/html/body/div[2]/div/div/div[2]/div/div[2]/button')
            self.close_browser()
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.error("SSL-VPN Portal login failed...")

    # Login to SSL-VPN Portal with TOTP
    def sslvpn_portal_login_with_totp(self, expected_failure=False):
        try:
            res_obj = DEVMODE()
            res_obj.change_resolution(1920, 1080)
            self.get_browser()
            self.maximize_window()
            self.go_to_url(self.url)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_element('text_field', 'name', 'username', self.username)
            logger.info("Configure - Setting password")
            self.set_element('text_field', 'name', 'password', self.password)
            logger.info("Action - Click Login")
            self.set_element('button', 'class', 'sw-login__trigger', "LOG IN")
            self.wait_for_text("text code")
            if expected_failure:
                # Setting the invalid TOTP value in the text field
                self.set_element('text_field', 'name', 'tfa', "invalid_totp")
                self.click_element('xpath', '/html/body/div/div/div/div/div[3]/div/div[2]/button')
                # Verifying that TOTP validation fails
                error_message = " is not authorized."
                self.wait_for_text(error_message)
                self.click_element('xpath', '/html/body/div[2]/div/div/div[2]/div/div/button')
                logger.info("SSL-VPN Portal login with TOTP is unsuccessful as expected...")
            else:
                # Click on Text Code
                self.click_element('xpath', '/html/body/div[1]/div/div/div/div[2]/div[3]/a')
                logger.info("Clicked text code successfully.")
                # Get the value of the text code to fetch TOTP from text code
                text_msg = self.get_attribute_value('xpath', '/html/body/div[2]/div[1]/div', 'innerText')
                logger.info(text_msg)
                # Fetching TOTP from text code
                totp = pyotp.TOTP(text_msg)
                otp_generated = totp.now()
                logger.info("Current OTP:" + otp_generated)
                # Setting the TOTP value in the text field
                self.set_element('text_field', 'name', 'tfa', otp_generated)
                self.click_element('xpath', '/html/body/div/div/div/div/div[3]/div/div[2]/button')
                # Verifying that TOTP is successfully validated and clicking on Continue
                self.wait_for_text('Your code has been verified.')
                self.click_element('xpath', '/html/body/div/div/div/div/div[3]/div/div/button')
                # Verifying SSL-VPN Portal has landed successfully into Virtual Office Home Page
                self.wait_for_text("NetExtender App")
                logger.info("SSL-VPN Portal login with TOTP is successful...")
                self.click_element('xpath', '/html/body/div/div/div/div[3]/div[3]/div/button')
                self.wait_for_text("Are you sure you want to logout?  All active connections will be terminated.")
                self.click_element('xpath', '/html/body/div[2]/div/div/div[2]/div/div[2]/button')
            self.close_browser()
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.error("SSL-VPN Portal login with TOTP failed...")

    # Login to SSL-VPN Portal with Mail OTP
    def sslvpn_portal_login_with_mail_otp(self, expected_failure=False):
        try:
            self.get_browser()
            self.maximize_window()
            self.go_to_url(self.url)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_element('text_field', 'name', 'username', self.username)
            logger.info("Configure - Setting password")
            self.set_element('text_field', 'name', 'password', self.password)
            logger.info("Action - Click Login")
            self.set_element('button', 'class', 'sw-login__trigger', "LOG IN")
            if expected_failure:
                # Setting the invalid mail OTP value in the text field
                self.set_element('text_field', 'name', 'tfa', "invalid_mail_otp")
                self.click_element('xpath', '/html/body/div/div/div/div/div[3]/div/div[2]/button')
                # Verifying that Mail OTP validation fails
                error_message = " is not authorized."
                self.wait_for_text(error_message)
                self.click_element('xpath', '/html/body/div[2]/div/div/div[2]/div/div/button')
                logger.info("SSL-VPN Portal login with Mail OTP is unsuccessful as expected...")
            else:
                # GET OTP from mail server
                mail_obj = MailModule()
                otp_received = mail_obj.get_otp_from_mail(smtp_username, smtp_password, smtp_server_ip)
                logger.info("OTP received from the mail server is: " + otp_received)
                # Setting the Mail OTP value in the text field
                self.set_element('text_field', 'name', 'tfa', otp_received)
                self.click_element('xpath', '/html/body/div/div/div/div/div[3]/div/div[2]/button')
                # Verifying that TOTP is successfully validated and clicking on Continue
                self.wait_for_text('Your password has been verified.')
                self.click_element('xpath', '/html/body/div/div/div/div/div[3]/div/div/button')
                # Verifying SSL-VPN Portal has landed successfully into Virtual Office Home Page
                self.wait_for_text("NetExtender App")
                logger.info("SSL-VPN Portal login with Mail OTP is successful...")
                self.click_element('xpath', '/html/body/div/div/div/div[3]/div[3]/div/button')
                self.wait_for_text("Are you sure you want to logout?  All active connections will be terminated.")
                self.click_element('xpath', '/html/body/div[2]/div/div/div[2]/div/div[2]/button')
            self.close_browser()
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.error("SSL-VPN Portal login with Mail OTP failed...")

