import pyotp

from inputs.constants import *
from libs.browser import Browser
from pytest_resources.common_require import *
from libs.mail import MailModule
from libs.screen_resolution import DEVMODE


class AccessRule(Browser):
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    # Log in to Firewall and access resource successfully
    def verify_ula_and_access_resource(self, totp=False, mail_otp=False):
        try:
            res_obj = DEVMODE()
            res_obj.change_resolution(1920, 1080)
            self.get_browser(ula=True)
            self.maximize_window()
            self.go_to_url(self.url)
            time.sleep(5)
            self.switch_window()
            self.wait_for_text('Authentication Required')
            self.click_element('xpath', '/html/body/div/div/div[3]/a')
            if self.does_page_have_text("Your connection is not private"):
                self.click_element('id', 'details-button')
                self.click_element('id', 'proceed-link')
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_element('text_field', 'name', 'username', self.username)
            logger.info("Configure - Setting password")
            self.set_element('text_field', 'name', 'password', self.password)
            logger.info("Action - Click Login")
            self.set_element('button', 'class', 'sw-login__trigger', "LOG IN")
            if totp:
                self.wait_for_text("text code")
                # Click on Text Code
                self.click_element('xpath', '/html/body/div/div/div/div/div[2]/div[3]/a')
                logger.info("clicked text code successfully.")
                # Get the value of the text code to fetch TOTP from text code
                text_msg = self.get_attribute_value('xpath', '/html/body/div[2]/div[1]/div', 'innerText')
                logger.info(text_msg)
                # Fetching TOTP from text code
                totp = pyotp.TOTP(text_msg)
                otp_generated = totp.now()
                logger.info("Current OTP: " + otp_generated)
                # Setting the TOTP value in the text field
                self.set_element('text_field', 'name', 'tfa', otp_generated)
                self.click_element('xpath', '/html/body/div/div/div/div/div[3]/div/div[2]/button')
                # Verifying that TOTP is successfully validated and clicking on Continue
                self.wait_for_text('Your code has been verified.')
                self.click_element('xpath', '/html/body/div/div/div/div/div[3]/div/div/button')
            if mail_otp:
                # GET OTP from mail server
                mail_obj = MailModule()
                otp_received = mail_obj.get_otp_from_mail(smtp_username, smtp_password, smtp_server_ip)
                logger.info("OTP received from the mail server is: " + otp_received)
                # Setting the TOTP value in the text field
                self.set_element('text_field', 'name', 'tfa', otp_received)
                self.click_element('xpath', '/html/body/div/div/div/div/div[3]/div/div[2]/button')
                # Verifying that TOTP is successfully validated and clicking on Continue
                self.wait_for_text('Your password has been verified.')
                self.click_element('xpath', '/html/body/div/div/div/div/div[3]/div/div/button')
            # Closing the "Automatic Firmware Updates" notification pop-up window
            self.close_auto_upgrade_notification()
            # Verifying FireWall has landed successfully into Home Page
            self.wait_for_text("Home")
            logger.info("ULA verification Successful...")
            all_handles = self.get_browser_all_handles()
            self.browser.switch_to.window(all_handles[0])
            self.wait_for_text("News")
            self.browser.switch_to.window(all_handles[1])
            self.click_element('class', 'sw-avatar__initials')
            self.click_element('xpath', '/html/body/div[2]/div[1]/div[1]/div[1]/div/div/div/div[4]/span/span')
            self.wait_for_text("Do you want to continue logout?")
            self.click_element('xpath', '/html/body/div[2]/div/div/div[2]/div/div[2]/button')
            self.close_browser()
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.error("Resource access with ULA verification failed...")

    # Log in to Firewall and access resource successfully
    def verify_ula_and_access_resource_with_expected_failure(self, totp=False, mail_otp=False):
        try:
            res_obj = DEVMODE()
            res_obj.change_resolution(1920, 1080)
            self.get_browser(ula=True)
            self.maximize_window()
            self.go_to_url(self.url)
            time.sleep(5)
            self.switch_window()
            self.wait_for_text('Authentication Required')
            self.click_element('xpath', '/html/body/div/div/div[3]/a')
            if self.does_page_have_text("Your connection is not private"):
                self.click_element('id', 'details-button')
                self.click_element('id', 'proceed-link')
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_element('text_field', 'name', 'username', self.username)
            logger.info("Configure - Setting password")
            self.set_element('text_field', 'name', 'password', self.password)
            logger.info("Action - Click Login")
            self.set_element('button', 'class', 'sw-login__trigger', "LOG IN")
            if totp:
                self.wait_for_text("text code")
                # Setting the invalid TOTP value in the text field
                self.set_element('text_field', 'name', 'tfa', "invalid_totp")
                self.click_element('xpath', '/html/body/div/div/div/div/div[3]/div/div[2]/button')
                # Verifying that TOTP validation fails
                error_message = " is not authorized."
                self.wait_for_text(error_message)
                self.click_element('xpath', '/html/body/div[2]/div/div/div[2]/div/div/button')
                logger.info("Firewall login with TOTP is unsuccessful as expected...")
            elif mail_otp:
                # Setting the invalid Mail OTP value in the text field
                self.set_element('text_field', 'name', 'tfa', "invalid_mail_otp")
                self.click_element('xpath', '/html/body/div/div/div/div/div[3]/div/div[2]/button')
                # Verifying that Mail OTP validation fails
                error_message = " is not authorized."
                self.wait_for_text(error_message)
                self.click_element('xpath', '/html/body/div[2]/div/div/div[2]/div/div/button')
                logger.info("Firewall login with Mail OTP is unsuccessful as expected...")
            else:
                self.wait_for_text(fw_unpw_login_failure_message)
                logger.info("Firewall login failed as expected...")
            # Verifying FireWall has landed successfully into Home Page
            logger.info("ULA verification is unsuccessful...")
            all_handles = self.get_browser_all_handles()
            self.browser.switch_to.window(all_handles[0])
            failure_text_message = "Connect to network"
            self.wait_for_text(failure_text_message)
            self.browser.switch_to.window(all_handles[1])
            self.close_browser()
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.error("Resource access with ULA verification is successful with invalid authentication...")

    # Suppressing "Automatic Firmware Updates" notification pop-up window
    def close_auto_upgrade_notification(self):
        time.sleep(5)
        text_status = self.does_page_have_text('Automatic Firmware Updates')
        if text_status:
            self.click_element('xpath', "//button[@class='sw-button sw-button--light fw-app-main__button-cancel']")
        else:
            logger.info("No Automatic Update Firmware pop-up found...")
