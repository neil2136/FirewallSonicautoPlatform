from modules.ui.fw_page import FWPage
import time
import os
from runner.settings import logger
import requests
import re
from utm import Firewall
from modules.API.system import LicenseApi
import json

from modules.ui.ui_wrapper import ActionChains, Browser
from runner.utils.assertion import Assertion

class FWPage(FWPage):

    def navigate_to_section_updated(self, section_header, section_identifier, labelName=None):
        if self.does_element_exist_now('xpath', "//span[contains(@class, 'sw-breadcrumb__item__text') and text()='"+section_identifier+"']"):
            logger.info("Page :"+ section_identifier)
        else:
            if self.does_element_exist_now('xpath', "//span[contains(@class, '"+section_header +"')]/following::li/div/div/span[text()='" + section_identifier + "']"):
                logger.info("Section is already expanded")
            else:
                logger.info("Expanding section")
                icon = self.get_left_panel()
                if labelName is not None:
                    element_xpath = "//span[contains(@class, '"+section_header+"')]/following::span[text()='"+labelName+"'] "
                    self.click_relative_element(icon, 'xpath', element_xpath)
                else:
                    self.click_relative_element(icon, 'class', section_header)
                logger.info("Expanded section successfully")


    def navigate_to_sd_wan_groups_section(self):
        self.navigate_to_network_page()
        self.navigate_to_section_updated("icon-network-port-interface", "Groups", labelName="SDWAN")
        self.click_element('xpath', "//div[contains(@class,'sw-nav-item__inner')][.//span[normalize-space()='Groups']]")       
        self.wait_for_page_data_to_be_rendered()
        logger.debug("Navigated to Network > SDWAN > Groups")

    def navigate_to_routing_rules_page(self):
        self.navigate_to_policy_page()
        self.navigate_to_section_updated("icon-rules", "Routing Rules", labelName="Rules and Policies")
        self.click_element('xpath', "//div[contains(@class,'sw-nav-item__inner')][.//span[normalize-space()='Routing Rules']]")       
        self.wait_for_page_data_to_be_rendered()
        logger.debug("Navigated to Policy > Rules and Policies > Routing Rules")