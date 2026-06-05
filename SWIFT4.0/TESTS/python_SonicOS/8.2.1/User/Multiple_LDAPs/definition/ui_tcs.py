import re
import sys
import argparse
import sys
import time
sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
print(sys.path)
from runner.settings import logger
from modules.ui.ui_wrapper import Browser
from runner.utils.assertion import Assertion
from modules.ui.fw_page import FWPage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

class Ui_Tests(FWPage):
    def __init__(self, url, user, pwd):
        self.url = url
        self.user = user
        self.password = pwd

    def navigate_to_settings_user_auth_page(self):
        self.navigate_to_device_page()
        time.sleep(3)
        self.click_element("xpath", "//span[normalize-space()='Users']")
        time.sleep(3)
        self.click_element("xpath", "//li[@class='sw-nav-group sw-nav-group--dark sw-nav-group--compact']//span[contains(text(),'Settings')]")
        time.sleep(3)
        logger.info("Navigation done")

    def verify_toggle_button(self, attrib, attrib_val):
        if attrib_val.isdigit() != True:
            class_value = self.get_attribute_value(attrib, attrib_val, 'class')
            if "sw-toggle--off" in class_value:
                print("Toggle is OFF")
                return False
            else:
                print("Toggle is ONN")
                return True

    def get_drop_down_value(self, select_identifier, values, modal=False):
        try:
            logger.debug2(f"verifying drop down values \t: {values}")
            if modal is True:
                self.click_element('xpath', "//div[contains(@class, 'sw-modal__main-body')]"
                                            "//following::*[contains(text(), '"+select_identifier+"')]"
                                            "/following::*[contains(@class, 'sw-select__icon')]")
            else:
                self.click_element('xpath', "//span[contains(text(), '"+select_identifier+"')]/following::*"
                                        "[contains(@class, 'sw-select__icon')]")

            for i in values:
                res = self.get_element('xpath', "//span[contains(text(), '"+select_identifier+"')]"
                                                                        "/following::div[contains(@class, 'sw-dropdown')]/"
                                                                        "span[text()='"+ i +"']", visibility=False).text
                logger.info(f"Found drop down value - {res}")

            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            return False

    def get_drop_down_value_single(self, select_identifier, values, modal=False):
        try:
            logger.debug2(f"verifying drop down values \t: {values}")
            if modal is True:
                self.click_element('xpath', "//div[contains(@class, 'sw-modal__main-body')]"
                                            "//following::*[contains(text(), '"+select_identifier+"')]"
                                            "/following::*[contains(@class, 'sw-select__icon')]")
            else:
                self.click_element('xpath', "//span[contains(text(), '"+select_identifier+"')]/following::*"
                                        "[contains(@class, 'sw-select__icon')]")

            res = self.get_element('xpath', "//span[contains(text(), '" + select_identifier + "')]""/following::div[contains(@class, 'sw-dropdown')]", visibility=False).text

            for i in values:
                if i in res:
                    return True
            return False
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            return False

    def login_ui(self):
        try:
            print("starting")
            self.get_browser()
            print("after browser")
            self.go_to_url(self.url)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_input_text_field('xpath', '//input[@name="username"]', self.user)
            logger.info("Configure - Setting password")
            self.set_input_text_field('xpath', '//input[@name="password"]', self.password)
            logger.info("Action - Clicked Login")
            self.click_element('class', 'sw-login__trigger')
            logger.info("login done")
            time.sleep(10)
            self.wait_for_page_data_to_be_rendered()
            self.click_element('xpath', "//button[normalize-space()='Cancel']")
            logger.info("Login Test Flag.")
            return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def check_ldap_schema_list(self):
        try:
            self.login_ui()
            self.navigate_to_users_settings_web_login_section()
            self.click_element("xpath", "//input[@class='sw-select__label-input sw-flexbox__flex sw-typo-default']")
            self.click_element("xpath", "//span[normalize-space()='LDAP']")
            time.sleep(3)
            self.click_element("xpath", "//button[normalize-space()='OK']")
            self.click_element("xpath","//button[@class='sw-button sw-button--light users-settings-auth__configure-ldap']")
            self.click_element("xpath", "//span[contains(text(),'Add Server')]")
            self.click_element("xpath", "//span[normalize-space()='Schema']")
            self.click_element("xpath", "//input[@class='sw-select__label-input sw-flexbox__flex sw-typo-default']")
            # self.select_drop_down_value("xpath", "//span[@class='sw-flexbox__flex sw-flexbox sw-flexbox--center-items'][normalize-space()='Microsoft Active Directory']", "Microsoft Active Directory")
            res = self.select_drop_down_value("Microsoft Active Directory", "Microsoft Active Directory")
            print(f"dropdown resp - {res}")
            get_res = self.get_element('xpath', "//input[@name='ldap-srvr-usr-qual-logon-attr']").text
            print(f"dropdown resp - {get_res}")



            self.logout_ui()
            return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Failed to check default country count")
            self.logout_ui()
            return False

    def verify_toggle_allow_only_users_listed_locally(self):
        try:
            self.login_ui()
            self.navigate_to_settings_user_auth_page()
            self.click_element("xpath", "//button[@class='sw-button sw-button--light users-settings-auth__configure-ldap']")
            self.click_element("xpath", "//span[normalize-space()='Users & Groups']")
            toggle_res = self.verify_toggle_button("xpath", "//div[@class='sw-toggle sw-toggle--right sw-toggle--regular sw-toggle--light sw-toggle--off ldap-form-user__user-ldap-check-local']")
            if toggle_res:
                self.logout_ui()
                return False

            self.logout_ui()
            return True

        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Failed")
            self.logout_ui()
            return False

    def verify_drop_down_default_ldap_user_group(self):
        try:
            drop_down_values_to_verify = ['Create New User Group', '--None--', 'Content Filtering Bypass', 'Everyone', 'Limited Administrators', 'Trusted Users', 'Guest Services']
            self.login_ui()
            self.navigate_to_settings_user_auth_page()
            self.click_element("xpath", "//button[@class='sw-button sw-button--light users-settings-auth__configure-ldap']")
            self.click_element("xpath", "//span[normalize-space()='Users & Groups']")
            drop_down_resp = self.get_drop_down_value(select_identifier="--None--", values=drop_down_values_to_verify, modal=True)
            if not drop_down_resp:
                self.logout_ui()
                return False

            self.logout_ui()
            return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Failed")
            self.logout_ui()
            return False

    def verify_ldap_window_can_be_closed_without_saving(self):
        try:
            self.login_ui()
            self.navigate_to_settings_user_auth_page()
            self.click_element("xpath", "//button[@class='sw-button sw-button--light users-settings-auth__configure-ldap']")
            self.click_element("xpath", "//span[@class='sw-icon__inner sw-font-icon icon-add']")
            self.set_text_field("xpath", "//input[@name='ldap-srvr-host']", "1.1.1.1")
            self.click_element("xpath","//button[@class='sw-button sw-button--light users-settings-config-ldap__btn-cancel-server']")
            count = self.get_element("xpath", "//span[@class='sw-table-footer__total-cont__value']").text
            print(f"COUNT -- {count}")
            if "0 item" not in count:
                self.logout_ui()
                return False

            self.logout_ui()
            return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Failed")
            self.logout_ui()
            return False

    def verify_disabled_mirror_ldap_user_group_locally(self):
        try:
            self.login_ui()
            self.navigate_to_settings_user_auth_page()
            self.click_element("xpath", "//button[@class='sw-button sw-button--light users-settings-auth__configure-ldap']")
            self.click_element("xpath", "//span[normalize-space()='Users & Groups']")

            toggle_res = self.verify_toggle_button("xpath",
                                                   "//div[contains(@class, 'ldap-form-user__ldap-usr-grp-mirroring')]")
            if toggle_res:
                self.toggle_button("xpath", "//div[@class='sw-toggle sw-toggle--right sw-toggle--regular sw-toggle--light ldap-form-user__ldap-usr-grp-mirroring']", False)
                time.sleep(2)
                self.click_element("xpath", "//button[normalize-space()='No']")
            resp = self.does_element_exist_now("xpath", "//input[@name='ldap-srvr-host']")
            resp1 = self.does_element_exist_now("xpath", "//label[@class='sw-radio sw-radio--light sw-flexbox sw-flexbox--inline sw-flexbox--center-items ldap-form-user__ldap-usr-grp-mirror-what-1']//span[@class='sw-radio__fake-radio-button sw-flexbox__flex-none sw-radio__fake-radio-button--checked']")
            resp2 = self.does_element_exist_now("xpath", "//label[@class='sw-radio sw-radio--light sw-flexbox sw-flexbox--inline sw-flexbox--center-items ldap-form-user__ldap-usr-grp-mirror-what-0']//span[@class='sw-radio__fake-radio-button sw-flexbox__flex-none']")
            if resp or resp1 or resp2:
                self.logout_ui()
                return False

            self.logout_ui()
            return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Failed")
            self.logout_ui()
            return False

    def verify_tls_checkbox(self):
        try:
            self.login_ui()
            self.navigate_to_settings_user_auth_page()
            self.click_element("xpath", "//button[@class='sw-button sw-button--light users-settings-auth__configure-ldap']")

            self.wait_for_page_data_to_be_rendered()
            tls_enable_resp = self.verify_toggle_button("xpath", "//div[@class='sw-toggle sw-toggle--right sw-toggle--regular sw-toggle--light ldap-settings-servers-table__enable-radius-server']")
            tls_port_resp = self.does_page_have_text("636")
            if not tls_port_resp and not tls_enable_resp:
                self.logout_ui()
                return False

            self.toggle_button("xpath", "//div[@class='sw-toggle sw-toggle--right sw-toggle--regular sw-toggle--light ldap-settings-servers-table__enable-radius-server']", False)
            self.click_element("xpath", "//button[normalize-space()='Confirm']")
            time.sleep(5)
            self.wait_for_page_data_to_be_rendered()
            tls_port_resp = self.does_page_have_text("389")
            if not tls_port_resp:
                self.logout_ui()
                return False

            self.logout_ui()
            return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Failed")
            self.logout_ui()
            return False

    def verify_drop_down_values_for_ldap_schema(self):
        try:
            drop_down_values_to_verify = ['Microsoft Active Directory', 'RFC2798 InetOrgPerson', 'RFC2307 Network Information Service', 'Samba SMB', 'Novell eDirectory', 'User defined']
            self.login_ui()
            self.navigate_to_settings_user_auth_page()
            self.click_element("xpath", "//button[@class='sw-button sw-button--light users-settings-auth__configure-ldap']")
            self.click_element("xpath", "//span[@class='sw-icon__inner sw-font-icon icon-add']")
            self.click_element("xpath", "//span[normalize-space()='Schema']")
            drop_down_resp = self.get_drop_down_value(select_identifier="Microsoft Active Directory", values=drop_down_values_to_verify, modal=True)
            if not drop_down_resp:
                self.logout_ui()
                return False

            self.logout_ui()
            return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Failed")
            self.logout_ui()
            return False

    def verify_primary_domain_changes(self):
        try:
            self.login_ui()
            self.navigate_to_settings_user_auth_page()
            self.click_element("xpath", "//button[@class='sw-button sw-button--light users-settings-auth__configure-ldap']")
            self.click_element("xpath", "//span[@class='sw-icon__inner sw-font-icon icon-add']")
            self.click_element("xpath", "//span[normalize-space()='Directory']")
            self.click_element("xpath", "//input[@name='ldap-srvr-usr-domain']")

            primary_domain = self.browser.find_element('xpath', "//input[@name='ldap-srvr-usr-domain']")
            primary_domain.send_keys(Keys.CONTROL + 'a')
            for i in "test.com":
                primary_domain.send_keys(i)

            self.click_element("xpath", "//button[normalize-space()='Auto Configure']")
            resp1 = self.does_page_have_text("Also update domain in any user group trees that are in the same domain?")
            print(f"TEXT response {resp1}")
            resp2 = self.does_page_have_text("Select Cancel to change only the primary domain")
            print(f"TEXT response2 {resp2}")
            self.click_element("xpath", "//button[normalize-space()='OK']")

            tree_containing_user = self.get_element("xpath", "/html[1]/body[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/section[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[6]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/ul[1]/li[1]/div[1]/div[1]/span[1]/div[1]/span[1]").text
            tree_containing_user_group = self.get_element("xpath", "/html[1]/body[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/section[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[6]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[4]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/ul[1]/li[1]/div[1]/div[1]/span[1]/div[1]/span[1]").text

            if ("test.com/Users" not in tree_containing_user) or ("test.com/Users" not in tree_containing_user_group):
                if not resp1 or not resp2:
                    self.logout_ui()
                    return False

            self.logout_ui()
            return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Failed")
            self.logout_ui()
            return False

    def verify_default_local_user_group(self):
        try:
            drop_down_values_to_verify = ['TEST\\test', 'test@test.com']
            self.login_ui()
            self.navigate_to_settings_user_auth_page()
            self.click_element("xpath", "//button[@class='sw-button sw-button--light users-settings-auth__configure-ldap']")
            self.click_element("xpath", "//span[normalize-space()='Users & Groups']")

            drop_down_resp = self.get_drop_down_value_single(select_identifier="--None--", values=drop_down_values_to_verify, modal=True)
            print(f"drop down resp -- {drop_down_resp}")
            if not drop_down_resp:
                self.logout_ui()
                return False

            self.logout_ui()
            return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Failed")
            self.logout_ui()
            return False
