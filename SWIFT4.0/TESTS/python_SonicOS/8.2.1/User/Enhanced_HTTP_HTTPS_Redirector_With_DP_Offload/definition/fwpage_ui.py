import sys
import time
import os


sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')

TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User'

from runner.settings import logger
from modules.ui.fw_page_test import FWPage
from selenium.webdriver.common.by import By
from runner.utils.assertion import Assertion

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User')

from utm import Firewall
from networkdevice import Host
from runner.settings import Params

ip = "192.168.168.168"
trusted_username = "localuser"
trusted_user_password = "S0nic@uto"
http_msn_url = "http://12.12.1.40"
https_msn_url = "https://12.12.1.40"

fw_api = Firewall(ip, user='admin', password='S0nic@uto', supported_config_mode='api')
fw = Firewall(ip, user='admin', password='S0nic@uto', supported_config_mode='api-ssh')

PC2 = Host(Params.testbed + '-PC2')


class FWPage_UI(FWPage):
    def __init__(self, ip, user, pwd):
        super().__init__(ip, user)
        self.ip = ip
        self.user = user
        self.password = pwd

    def navigate_to_network_tab(self):
        time.sleep(15)
        self.click_element('xpath',
                           "//span[@class='sw-top-nav-item__label sw-flexbox__flex-none'][normalize-space()='Network']")
        logger.info("Navigating to network Tab")
        time.sleep(5)

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

    def navigate_to_diag_internal_settings_page(self):
        # Navigate to diag page
        self.go_to_url("https://" + self.ip + "/sonicui/7/m/diag")
        try:
            try:
                self.wait_for_text("Automatic Firmware Updates")
            except Exception as e:
                pass
            if self.browser.find_element("xpath", "//button[text()='OK']"):
                logger.info("Found Automatic Firmware Updates pop-up, clicking OK")
                self.click_element("xpath", "//button[text()='OK']")
        except Exception:
            logger.info("No 'Automatic Firmware Updates' pop-up found, proceeding further...")

        time.sleep(5)
        # Click on Internal Settings
        self.click_element("xpath", "//button[normalize-space()='Internal Settings']")

    def verify_internal_tcp_port_in_diag_page(self):
        # verify the option 'Internal TCP port number for redirecting unauthenticated HTTPS connections into the web server' available
        Assertion.assert_equal(self.does_page_have_text('Internal TCP port number for redirecting unauthenticated HTTPS connections into the web server'), True, "ERR: 'Internal TCP port number for redirecting unauthenticated HTTPS connections into the web server' is available in diag page")

        # Verify Internal TCP port number is 10281 by default
        Assertion.assert_equal(self.get_attribute_value('xpath', "//input[@name='internalTCPport']", "value"), "10281", "ERR: Internal TCP port number is not 10281 by default")

    def verify_default_setting_for_dp_offload_available(self):
        # verify the option 'Serve HTTP redirect pages in the DP' available
        Assertion.assert_equal(self.does_page_have_text('Serve HTTP redirect pages in the DP'), True, "ERR: 'Serve HTTP redirect pages in the DP' is available in diag page")

        # Verify 'Serve HTTP redirect pages in the DP' is enabled by default
        Assertion.assert_equal(self.verify_toggle_button('xpath', "//div[@class='sw-title-pane sw-title-pane--light sw-flexbox sw-flexbox--column sw-typo-default fw-mgmt-ftr-diag__UserAuthenticationSettings']//div[14]//div[1]//div[2]//span[1]//div[1]"), True, "ERR: 'Serve HTTP redirect pages in the DP' is not enabled by default")

        # Verify option 'Internal TCP port number for redirecting unauthenticated HTTPS connections into the web server' available and set to 10281
        self.verify_internal_tcp_port_in_diag_page()

        # verify the option 'FLUSH CACHED REDIRECT FILES' available
        Assertion.assert_equal(self.does_page_have_text('Flush Cached Redirect Files'), True, "ERR: 'FLUSH CACHED REDIRECT FILES' is available in diag page")


    def verify_http_port_number_and_changable(self):
        # verify the option 'Internal TCP port number for redirecting unauthenticated HTTPS connections into the web server' available
        Assertion.assert_equal(self.does_page_have_text(
            'Internal TCP port number for redirecting unauthenticated HTTPS connections into the web server'), True,
            "ERR: 'Internal TCP port number for redirecting unauthenticated HTTPS connections into the web server' is available in diag page")

        # Verify Internal TCP port number is 10281 by default
        Assertion.assert_equal(self.get_attribute_value('xpath',
                                                         "//input[@name='internalTCPport']",
                                                        "value"), "10281",
                               "ERR: Internal TCP port number is not 10281 by default")


        # Verify Internal TCP port number can be changed
        self.set_text_field("xpath", "//input[@name='internalTCPport']", "10282")
        self.click_element('xpath', "//button[normalize-space()='Accept']")
        self.wait_for_success_banner()
        logger.info("clicked Accept")

        Assertion.assert_equal(self.get_attribute_value('xpath',
                                                         "//input[@name='internalTCPport']",
                                                        "value"), "10282",
                               "ERR: Internal TCP port number change failed")

        # Verify Internal TCP port number can be changed
        self.set_text_field("xpath", "//input[@name='internalTCPport']", "10281")
        self.click_element('xpath', "//button[normalize-space()='Accept']")
        self.wait_for_success_banner()
        logger.info("clicked Accept")

        Assertion.assert_equal(self.get_attribute_value('xpath',
                                                        "//input[@name='internalTCPport']",
                                                        "value"), "10281",
                               "ERR: Internal TCP port number change failed")

    def verify_redirect_http_traffic_after_disable_dp_offload(self):
        # Disable the option 'Serve HTTP redirect pages in the DP'
        if self.verify_toggle_button('xpath', "//div[@class='sw-title-pane sw-title-pane--light sw-flexbox sw-flexbox--column sw-typo-default fw-mgmt-ftr-diag__UserAuthenticationSettings']//div[14]//div[1]//div[2]//span[1]//div[1]"):
            self.click_element('xpath', "//div[@class='sw-title-pane sw-title-pane--light sw-flexbox sw-flexbox--column sw-typo-default fw-mgmt-ftr-diag__UserAuthenticationSettings']//div[14]//div[1]//div[2]//span[1]//div[1]")
            self.click_element('xpath', "//button[normalize-space()='Accept']")
            self.wait_for_success_banner()
            logger.info("clicked Accept")

        # Verify 'Serve HTTP redirect pages in the DP' is enabled by default
        Assertion.assert_equal(self.verify_toggle_button('xpath',
                                                         "//div[@class='sw-title-pane sw-title-pane--light sw-flexbox sw-flexbox--column sw-typo-default fw-mgmt-ftr-diag__UserAuthenticationSettings']//div[14]//div[1]//div[2]//span[1]//div[1]"),
                               False, "ERR: 'Serve HTTP redirect pages in the DP' is not enabled by default")

    def verify_redirect(self, url):
        self.go_to_url(url)
        self.wait_for_text("Click here to login")
        if not self.does_page_have_text("Click here to login"):
            self.refresh_browser()
        self.click_element('xpath', "//a[normalize-space()='Click here to login']")
        self.wait_for_page_data_to_be_rendered()
        self.set_text_field("xpath", "//input[@name='username']", trusted_username)
        self.set_text_field("xpath", "//input[@name='password']", trusted_user_password)
        self.click_element('xpath', "//div[normalize-space()='LOG IN']")

    def verify_flush_cached_files(self, interface="one"):
        if interface == "one":
            pass
