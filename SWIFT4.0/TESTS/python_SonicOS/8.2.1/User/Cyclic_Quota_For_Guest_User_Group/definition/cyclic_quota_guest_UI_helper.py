import re
import sys
import argparse
import sys
import time

sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
# sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
print(sys.path)
from runner.settings import logger
from modules.ui.fw_page import FWPage
import os


class FWPage_new(FWPage):
    def __init__(self, ip='192.168.168.168', user='admin', password='S0nic@uto'):
        self.ip = ip
        self.user = user
        self.password = password


    def add_and_validate_cyclic_quota_local_user(self,name="test_ui"):
        try:
            self.login_ui()
            self.navigate_to_local_users_section()
            logger.info("Test")
            self.click_element("xpath", "//span[.//text()[contains(.,'Add User')]]")
            self.set_text_field("xpath", "//input[@placeholder='Enter Name...']", name)
            self.set_text_field("xpath", "//input[@placeholder='Enter password...']", "S0nic@uto")
            self.set_text_field("xpath", "//input[@type='password' and contains(@placeholder,'Confirm')]", "S0nic@uto")
            self.click_element("xpath", "//span[normalize-space()='Groups']")
            self.click_element("xpath","//li[contains(@class,'sw-tree-list-item')]""[.//span[normalize-space()='Guest Services']]")
            self.click_element("xpath","//div[contains(@class,'sw-transfer-list__selector-middle')]//span[contains(@class,'sw-icon-button')and not(contains(@class,'sw-icon-button--disabled'))and @title='Move marked to right']")
            self.click_element("xpath", "//span[normalize-space()='User Quota']")
            self.select_drop_down_value("Non Cyclic", "Day")
            self.set_text_field("xpath", "//input[@name='sessionLifetimeLimit']", "10")
            self.click_element("xpath", "//button[normalize-space()='Save']")
            time.sleep(15)
            res = self.does_page_have_text(name)
            self.logout_ui()
            return res
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Failed to check add_guest_services")
            self.logout_ui()
            return False

    def add_and_validate_guest_services(self,name="test_ui"):
        try:
            self.login_ui()
            self.navigate_to_users_guest_services()
            self.click_element("xpath", "//span[@class='sw-icon-button__label-cont sw-flexbox__flex-none'][normalize-space()='Add']")
            self.set_text_field("xpath", "//input[@name='profile-name']", name)
            self.select_drop_down_value("Non-Cyclic","Per Day")
            self.set_text_field("xpath", "//input[@name='session-lifetime']", "10")
            self.click_element("xpath","//button[normalize-space()='Add']")
            time.sleep(15)
            res = self.does_page_have_text(name)
            self.logout_ui()
            return res
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Failed to check add_guest_services")
            self.logout_ui()
            return False

    def add_and_validate_guest_account(self, name="test_ui"):
        try:
            self.login_ui()
            self.navigate_to_users_guest_accounts()
            self.click_element("xpath", "//span[contains(@class,'sw-icon-button')][.//span[normalize-space()='Add']]")
            self.clear_text_field("xpath", "//input[@name='name']")
            self.set_text_field("xpath", "//input[@name='name']", name)
            self.set_text_field("xpath", "//input[@name='Password']", "S0nic@uto")
            self.set_text_field("xpath", "//input[@name='ConfirmPassword']", "S0nic@uto")
            self.click_element("xpath", "//span[@class='sw-tab__inner__piece sw-flexbox__flex sw-flexbox sw-flexbox--center-items sw-flexbox--center-justify'][normalize-space()='Guest Services']")
            self.select_drop_down_value("Non Cyclic", "Per Day")
            self.set_text_field("xpath", "//input[@name='session_lifetime']", "10")
            self.click_element("xpath", "//button[normalize-space()='Save']")
            time.sleep(15)
            res = self.does_page_have_text(name)
            self.logout_ui()
            return res
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Failed to check add_guest_services")
            self.logout_ui()
            return False

    def get_drop_down_value(self, select_identifier, values, modal=False):
        try:
            logger.debug2(f"verifying drop down values \t: {values}")
            if modal is True:
                self.click_element('xpath', "//div[contains(@class, 'sw-modal__main-body')]"
                                            "//following::*[contains(text(), '" + select_identifier + "')]"
                                                                                                      "/following::*[contains(@class, 'sw-select__icon')]")
            else:
                self.click_element('xpath', "//span[contains(text(), '" + select_identifier + "')]/following::*"
                                                                                              "[contains(@class, 'sw-select__icon')]")

            for i in values:
                res = self.get_element('xpath', "//span[contains(text(), '" + select_identifier + "')]"
                                                                                                  "/following::div[contains(@class, 'sw-dropdown')]/"
                                                                                                  "span[text()='" + i + "']",
                                       visibility=False).text
                logger.info(f"Found drop down value - {res}")

            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            return False

    def validate_cyclic_quota_drop_down_guest_account(self):
        try:
            self.login_ui()
            self.navigate_to_users_guest_accounts()
            self.click_element("xpath", "//span[contains(@class,'sw-icon-button')][.//span[normalize-space()='Add']]")
            self.click_element("xpath", "//span[@class='sw-tab__inner__piece sw-flexbox__flex sw-flexbox sw-flexbox--center-items sw-flexbox--center-justify'][normalize-space()='Guest Services']")
            drop_down_values_to_verify=["Non Cyclic","Per Month","Per Day","Per Week"]
            drop_down_resp = self.get_drop_down_value(select_identifier="Non Cyclic", values=drop_down_values_to_verify, modal=False)
            self.logout_ui()
            return drop_down_resp
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Failed to check add_guest_services")
            self.logout_ui()
            return False
    def verify_toggle_button(self, attrib, attrib_val):
        if attrib_val.isdigit() != True:
            class_value = self.get_attribute_value(attrib, attrib_val, 'class')
            if "sw-toggle--off" in class_value:
                logger.info("Toggle is OFF")
                return False
            else:
                logger.info("Toggle is ONN")
                return True

    def wlan_zone_guest_services(self, enable=True):
        try:
            self.login_ui()
            self.navigate_to_zone_object()
            self.click_on_edit_element_after_hovering("WLAN")
            self.click_element("xpath", "//span[normalize-space()='Guest Services']")
            time.sleep(20)
            self.toggle_button("xpath",
                               "//div[@class='sw-toggle sw-toggle--right sw-toggle--regular sw-toggle--light sw-toggle--off']",
                               enable)
            # self.click_element("xpath", "//button[normalize-space()='Save']")
            # Locate the button element (replace with the actual method to find your button)
            button = self.click_button_using_action_chains(
                "//button[normalize-space()='Save']")  # Replace 'button-id' with the actual ID of your button# Scroll to the button element
            # actions = ActionChains(self.browser)
            # actions.move_to_element(button).perform()

            # self.click_element("xpath", "/html/body/div/div/div[2]/div[2]/div[2]/div[1]/div/section/div/div[3]/div/div[2]/div/div/div[4]/div/div[2]/button")
            time.sleep(10)
            self.logout_ui()
            return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Failed to check add_guest_services")
            self.logout_ui()
            return False

    def wlan_zone_guest_services_on(self, enable=True):
        try:
            self.login_ui()
            self.navigate_to_zone_object()
            self.click_on_edit_element_after_hovering("WLAN")
            self.click_element("xpath", "//span[normalize-space()='Guest Services']")
            time.sleep(20)
            self.toggle_button("xpath",
                               "//div[@class='sw-toggle sw-toggle--right sw-toggle--regular sw-toggle--light']", enable)
            # self.click_element("xpath", "//button[normalize-space()='Save']")
            # Locate the button element (replace with the actual method to find your button)
            button = self.click_button_using_action_chains(
                "//button[normalize-space()='Save']")  # Replace 'button-id' with the actual ID of your button# Scroll to the button element
            # actions = ActionChains(self.browser)
            # actions.move_to_element(button).perform()

            # self.click_element("xpath", "/html/body/div/div/div[2]/div[2]/div[2]/div[1]/div/section/div/div[3]/div/div[2]/div/div/div[4]/div/div[2]/button")
            time.sleep(10)
            self.logout_ui()
            return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Failed to check add_guest_services")
            self.logout_ui()
            return False

    def validate_wlan_zone_guest_services(self,enable=True):
        try:
            self.login_ui()
            self.navigate_to_zone_object()
            self.click_on_edit_element_after_hovering("WLAN")
            self.click_element("xpath", "//span[normalize-space()='Guest Services']")
            time.sleep(20)
            res = self.verify_toggle_button("xpath",
                                            "//div[@class='sw-toggle sw-toggle--right sw-toggle--regular sw-toggle--light']")
            self.logout_ui()
            if enable == res :
                return True
            else:
                return  False
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Failed to check add_guest_services")
            self.logout_ui()
            return False

    def get_value(self):
        try:
            self.login_ui()
            self.navigate_to_zone_object()
            self.click_on_edit_element_after_hovering("WLAN")
            self.click_element("xpath", "//span[normalize-space()='Guest Services']")
            time.sleep(20)
            res = self.get_attribute_value("xpath",
                                        "//div[@class='sw-toggle sw-toggle--right sw-toggle--regular sw-toggle--light']",
                                         "class")
            self.logout_ui()
            return  res
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Failed to check add_guest_services")
            self.logout_ui()
            return False


    def get_text(self,text="Per Day"):
        try:
            self.login_ui()
            self.navigate_to_users_guest_services()
            self.click_element("xpath",
                               "//span[@class='sw-icon-button__label-cont sw-flexbox__flex-none'][normalize-space()='Add']")
            self.set_text_field("xpath", "//input[@name='profile-name']", "test")
            self.select_drop_down_value("Non-Cyclic", text)
            res = self.browser.find_elements(
                "xpath",
                f"//div[contains(@class,'sw-form-row')]"
                f"//span[normalize-space(.)='{text}' "
                f"and not(ancestor::div[contains(@class,'sw-select')])]"
            )
            self.logout_ui()
            if len(res) == 3:
                return True
            else:
                logger.info(f"Expected 3 Per Day rows, found {len(res)}")
                return False

        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Failed to check add_guest_services")
            self.logout_ui()
            return False

