import sys
import time
import os

sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')

from runner.settings import logger
from modules.ui.fw_page import FWPage
# from modules.ui.fw_page_test import FWPage
from selenium.webdriver.common.by import By
from runner.utils.assertion import Assertion

sys.path.append(os.environ["PYTHON_COMMON_HOME"])

from utm import Firewall
from networkdevice import Host
from runner.settings import Params

ip = "192.168.168.168"
G_NEW_PASSWORD = Params.G_NEW_PASSWORD

fw_api = Firewall(ip, user='admin', password=G_NEW_PASSWORD, supported_config_mode='api')
fw = Firewall(ip, user='admin', password=G_NEW_PASSWORD, supported_config_mode='api-ssh')


class FWPage_UI(FWPage):
    def __init__(self, ip, user, pwd):
        super().__init__(ip, user)
        self.ip = ip
        self.user = user
        self.password = pwd

    def navigate_to_device_tab(self):
        self.wait_for_page_data_to_be_rendered()
        self.click_element('xpath',
                           "//span[@class='sw-top-nav-item__label--default sw-flexbox__flex-none'][normalize-space()='Device']")
        logger.info("Navigating to Device Tab")
        self.wait_for_page_data_to_be_rendered()

    def navigate_to_users_settings_section(self):
        self.navigate_to_device_tab()
        self.wait_for_page_data_to_be_rendered()
        self.navigate_to_section("icon-user", "Status", labelName="Users")
        time.sleep(5)
        logger.info('navigated to status page')
        self.navigate_to_section("icon-user", "Settings", labelName="Users")
        self.wait_for_page_data_to_be_rendered()
        logger.debug("Navigated to Device > Users > settings")

    def wait_for_success_banner(self):
        try:
            logger.debug2("Waiting for success banner")
            self.wait_for_text("Success")
            self.wait_for_page_data_to_be_rendered()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Wait for success banner failed")

    def verify_toggle_button(self, attrib, attrib_val):
        if not attrib_val.isdigit():
            class_value = self.get_attribute_value(attrib, attrib_val, 'class')
            return "sw-toggle--off" not in class_value

    """DEVICE > USERS > SETTINGS UI LIBS"""

    def click_on_configur_sso(self):
        logger.info("Clicking on Configure SSO Button on Device > Users > Settings Authentication Page")
        # self.click_element('xpath',
        #                    "//button[@class='sw-btn sw-btn--light users-settings-auth__configure-sso'][normalize-space()='Configure']")
        self.click_element('xpath', "//button[@class='sw-button sw-button--light users-settings-auth__configure-sso']")
        self.wait_for_page_data_to_be_rendered()

    def click_on_radius_accounting_tab(self):
        logger.info("Clicking on Configure Radius Accounting Tab Button on SSO Configuration Tab")
        self.click_element('xpath',
                           "//span[@class='sw-tab__inner__piece sw-flexbox__flex sw-flexbox sw-flexbox--center-items sw-flexbox--center-justify'][normalize-space()='RADIUS Accounting']")
        self.wait_for_page_data_to_be_rendered()

    def click_on_create_new_radius_accounting_client(self):
        logger.info("Clicking on Create New button to Configure Radius Accounting Client")
        self.click_element('xpath',
                           "//span[@class='sw-icon-button__label-cont sw-flexbox__flex-none'][normalize-space()='Add Client']")
        self.wait_for_page_data_to_be_rendered()

    def click_on_save_in_add_radius_acc_client(self):
        logger.info("Clicking on Save button in create new Radius Accounting Client tab")
        # self.click_element('xpath',
        #                    "//button[@class='sw-btn sw-btn--light sw-btn--default add-radius-accounting-client__button-ok add-radius-accounting-client__ml-10'][normalize-space()='Save']")
        self.click_element('xpath', "//button[normalize-space()='Save']")
        self.wait_for_page_data_to_be_rendered()

    def click_on_close_in_add_radius_acc_client(self):
        logger.info("Clicking on Close button in create new Radius Accounting Client tab")
        # self.click_element('xpath',
        #                    "//button[@class='sw-btn sw-btn--light add-radius-accounting-client__button-ok'][normalize-space()='Cancel']")
        self.click_element('xpath',"//button[@class='sw-button sw-button--light add-radius-accounting-client__button-ok']")
        self.wait_for_page_data_to_be_rendered()

    def click_on_forwarding_tab_in_add_radius_acc_client(self):
        logger.info("Clicking on Forwarding Tab button in create new Radius Accounting Client tab")
        self.click_element('xpath',
                           "//span[@class='sw-tab__inner__piece sw-flexbox__flex sw-flexbox sw-flexbox--center-items sw-flexbox--center-justify'][normalize-space()='Forwarding']")
        self.wait_for_page_data_to_be_rendered()

    def config_radius_acc_client(self, radius_acc_client, match_pass=False, invalid_fwd_server=False, save=True,
                                 invalid_ip=False):
        self.click_on_configur_sso()
        self.click_on_radius_accounting_tab()
        self.click_on_create_new_radius_accounting_client()
        configs = radius_acc_client.keys()
        if "agentKey" in configs:
            self.set_text_field("xpath", "//input[@name='agentKey']", radius_acc_client["agentKey"])
        if "confirmKey" in configs:
            self.set_text_field("xpath", "//input[@name='confirmKey']", radius_acc_client["confirmKey"])
        if "clientHost" in configs:
            if radius_acc_client["clientHost"] == "":
                self.set_text_field("xpath", "//input[@name='clientHost']", "")
                Assertion.assert_equal(self.does_page_have_text("Field cannot be empty"), True,
                                       "ERR: Field cannot be empty warning error did not come up")
                logger.info("Verified Client Host Field Cannot be Empty Warning Message")
                self.set_text_field("xpath", "//input[@name='clientHost']", "8.8.3.3")
            else:
                self.set_text_field("xpath", "//input[@name='clientHost']", radius_acc_client["clientHost"])
                if invalid_ip:
                    Assertion.assert_equal(
                        self.does_page_have_text("Enter a valid HostName, IPV4 address or IPV6 address"), True,
                        "ERR: Invalid Client IP error did not come up")
                    self.set_text_field("xpath", "//input[@name='clientHost']", "8.8.3.3")
        if match_pass:
            Assertion.assert_equal(self.does_page_have_text("Shared keys does not match"), True,
                                   "ERR: Shared keys does not match warning error did not come up")
        if "forwarding" in configs:
            self.click_on_forwarding_tab_in_add_radius_acc_client()
            if "server1" in radius_acc_client["forwarding"]:
                if "ip" in radius_acc_client["forwarding"]["server1"]:
                    self.set_text_field("xpath", "//input[starts-with(@name, 'name')]",
                                        radius_acc_client["forwarding"]["server1"]["ip"])
            if invalid_fwd_server:
                Assertion.assert_equal(self.does_page_have_text("Enter a valid HostName, IPV4 address or IPV6 address"),
                                       True,
                                       "ERR: Invalid Forwarding Server IP error did not come up")
        if save:
            self.click_on_save_in_add_radius_acc_client()
        else:
            self.click_on_close_in_add_radius_acc_client()
