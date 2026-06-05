# from modules.UI7.common_require import *
import stat
from multiprocessing  import Process,current_process
# from modules.UI7.common_require import *
import argparse
import base64
import binascii
import copy
import hashlib
import hmac
import json
import pprint
import math
import os
import re
import requests
import socket
import socket
import ssl
import sys
import time
import warnings
import yaml
import traceback
import subprocess
from copy import deepcopy
from datetime import datetime
from datetime import timedelta
from os import path
from random import randint
#from easyprocess.__init__ import EasyProcess, EasyProcessError
#from pyvirtualdisplay.display import Display
#from xvfbwrapperlib.xvfbwrapper import Xvfb
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import unquote
from collections import OrderedDict
from runner.settings import logger
from ui_wrapper import Browser
import time

new_browser = Browser()


class UIHelper:

    # FUNCTIONALITY     : Clicks on add icon
    # INPUT             : None
    # RETURNS           : None
    def click_add_icon(self, label=None):
        try:
            logger.debug("Action - Clicking on Add icon")
            if label is None:
                new_browser.click_element('class', "icon-add")
            else:
                new_browser.click_element('xpath', "//span[contains(@class, 'icon-add')]/following::span[contains(text(), '" + label + "')]")
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to click add icon")

    # FUNCTIONALITY     : Clicks on close icon on a form
    # INPUT             : None
    # RETURNS           : None
    def click_close_icon(self):
        try:
            logger.debug("Action - Clicking Close")
            new_browser.click_element('class', 'icon-close-thin')
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to click close icon")

    # FUNCTIONALITY     : Clicks on delete button
    # INPUT             : None
    # RETURNS           : None
    def click_delete_icon(self):
        try:
            logger.debug("Action - Clicking on Delete icon")
            new_browser.click_element('class', "icon-trash")
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to click delete icon")

    # FUNCTIONALITY     : Clicks on confirm alert button
    # INPUT             : None
    # RETURNS           : None
    def accept_alert(self):
        try:
            logger.debug("Action - Clicking on Confirm button")
            new_browser.click_element('xpath', '//div[contains(@class, "sw-confirm-modal__footer")]/div/div/button'
                                                   '[text()="Submit" or text()="OK" or text()="Ok" or text()="Confirm"]')
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to accept the alert")

    # FUNCTIONALITY     : Clicks on cancel alert button
    # INPUT             : None
    # RETURNS           : None
    def cancel_alert(self):
        try:
            logger.debug("Action - Clicking on Cancel button")
            new_browser.click_element('xpath', '//div[contains(@class, "sw-confirm-modal__footer")]'
                                                   '/div/div/button[text()="Cancel"]')
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to click cancel icon")

    def submit_page(self):
        try:
            logger.debug("Action - Clicking on Save button")
            new_browser.click_element('xpath', '//div/button[text()="Save" or text()="Accept" or '
                                                   'text()="OK" or text()="Update" or text()="Authenticate" or text()="Ok" or text()="Submit"]')
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to click submit icon")

    # FUNCTIONALITY     : Clicks on GO button
    # INPUT             : None
    # RETURNS           : None
    def go_page(self):
        try:
            logger.debug("Action - Clicking on GO button")
            new_browser.click_element('xpath', '//div/button[text()="GO"]')
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to click GO button")

    # FUNCTIONALITY     : Clicks on cancel button
    # INPUT             : None
    # RETURNS           : None
    def cancel_page(self):
        try:
            logger.debug("Action - Clicking on Cancel button")
            new_browser.click_element('xpath', '//div/button[text()="Cancel"]')
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to click cancel button")

    # FUNCTIONALITY     : Clicks on close button
    # INPUT             : None
    # RETURNS           : None
    def close_page(self):
        try:
            logger.debug("Action - Clicking on Close button")
            new_browser.click_element('xpath', '//div/button[text()="Close"]')
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to click close button")

    def go_back(self):
        logger.debug("Action - Clicking on Go Back")
        new_browser.click_element('xpath', '//div/span/span[contains(@class, "icon-go-back")]')

    # FUNCTIONALITY     : Clicks on refresh button
    # INPUT             : None
    # RETURNS           : None
    def click_refresh_icon(self):
        try:
            logger.debug("Action - Clicking on Refresh icon")
            new_browser.click_element('class', "icon-refresh")
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to click refresh icon")

    # FUNCTIONALITY     : Clicks search tab and searches a desired string
    # INPUT             : String to be searched
    # RETURNS           : None
    def search_string(self, string_to_be_searched):
        try:
            logger.info("Searching for " + string_to_be_searched)
            logger.debug("Action - Clicking on Search icon")
            new_browser.click_element('class', "icon-search")
            getObject = new_browser.get_element('xpath','//input[contains(@placeholder, "Search")]')
            getObject.send_keys(Keys.CONTROL, "a")
            getObject.send_keys(Keys.BACKSPACE)
            #getObject.send_keys(string_to_be_searched)
            for key in string_to_be_searched:
                getObject.send_keys(key)
            getObject.send_keys(Keys.ENTER)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to search the given string")

    # FUNCTIONALITY     : Clicks on edit icon after hovering on the desired entry
    # INPUT             : the name of row entry(row identifier)
    # RETURNS           : None
    def click_on_edit_element_after_hovering(self, row_identifier, modal=False):
        try:
            row_identifier_xpath1 = "//td/div[text()='" + row_identifier + "']"
            row_identifier_xpath2 = "//td/div/div[text()='" + row_identifier + "']"
            row_identifier_xpath3 = "//div[text()='" + row_identifier + "' and contains(@class, 'sw-table-row__cell__wrapper')]"
            row_identifier_xpath4 = "//div[contains(text(),'" + row_identifier + "') and contains(@class, 'sw-table-row')]"
            row_identifier_xpath5 = "//div[contains(@class, 'sw-table-row')]/following::*[text()='" + row_identifier + "']"
            row_identifier_xpath6 = "//div[contains(@class, 'sw-table-row')]/following::*[contains(text(), '" + row_identifier + "')]"
            pencil_icon_xpath = "/following::*[contains(@class,'icon-pencil')]"
            modal_xpath = "//div[contains(@class, 'sw-modal__main-body')]//following::"
            if modal is False:

                new_browser.move_to_the_element('xpath',
                                                    row_identifier_xpath1 + "|" +
                                                    row_identifier_xpath2 + "|" +
                                                    row_identifier_xpath3 + "|" +
                                                    row_identifier_xpath4 + "|" +
                                                    row_identifier_xpath5 + "|" +
                                                    row_identifier_xpath6)
                self.click_element('xpath',
                                   row_identifier_xpath1 + pencil_icon_xpath + "|" +
                                   row_identifier_xpath2 + pencil_icon_xpath + "|" +
                                   row_identifier_xpath3 + pencil_icon_xpath + "|" +
                                   row_identifier_xpath4 + pencil_icon_xpath + "|" +
                                   row_identifier_xpath5 + pencil_icon_xpath + "|" +
                                   row_identifier_xpath6 + pencil_icon_xpath)
            else:
                new_browser.move_to_the_element('xpath',
                                                    modal_xpath + row_identifier_xpath1 + "|" +
                                                    modal_xpath + row_identifier_xpath2 + "|" +
                                                    modal_xpath + row_identifier_xpath3 + "|" +
                                                    modal_xpath + row_identifier_xpath4 + "|" +
                                                    modal_xpath + row_identifier_xpath5 + "|" +
                                                    modal_xpath + row_identifier_xpath6)
                self.click_element('xpath',
                                   modal_xpath + row_identifier_xpath1 + pencil_icon_xpath + "|" +
                                   modal_xpath + row_identifier_xpath2 + pencil_icon_xpath + "|" +
                                   modal_xpath + row_identifier_xpath3 + pencil_icon_xpath + "|" +
                                   modal_xpath + row_identifier_xpath4 + pencil_icon_xpath + "|" +
                                   modal_xpath + row_identifier_xpath5 + pencil_icon_xpath + "|" +
                                   modal_xpath + row_identifier_xpath6 + pencil_icon_xpath)
            self.ui_helper.wait_for_page_data_to_be_rendered()
            logger.debug2("Clicked on edit button for the entry:" + row_identifier)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Unable to click edit icon")

    # FUNCTIONALITY     : Clicks on disconnect icon after hovering on the desired entry
    # INPUT             : the name of row entry(row identifier)
    # RETURNS           : None
    def click_on_disconnect_element_after_hovering(self, row_identifier, modal=False):
        try:
            row_identifier_xpath1 = "//td/div[text()='" + row_identifier + "']"
            row_identifier_xpath2 = "//td/div/div[text()='" + row_identifier + "']"
            row_identifier_xpath3 = "//div[text()='" + row_identifier + "' and contains(@class, 'sw-table-row')]"
            row_identifier_xpath4 = "//div[contains(text(),'" + row_identifier + "') and contains(@class, 'sw-table-row')]"
            row_identifier_xpath5 = "//div[contains(@class, 'sw-table-row')]/following::*[text()='" + row_identifier + "']"
            row_identifier_xpath6 = "//div[contains(@class, 'sw-table-row')]/following::*[contains(text(), '" + row_identifier + "')]"
            disconnect_icon_xpath = "/following::*[contains(@class,'icon-user-remove')]"
            modal_xpath = "//div[contains(@class, 'sw-modal__main-body')]//following::"
            if modal is False:

                new_browser.move_to_the_element('xpath',
                                                    row_identifier_xpath1 + "|" +
                                                    row_identifier_xpath2 + "|" +
                                                    row_identifier_xpath3 + "|" +
                                                    row_identifier_xpath4 + "|" +
                                                    row_identifier_xpath5 + "|" +
                                                    row_identifier_xpath6)
                self.click_element('xpath',
                                   row_identifier_xpath1 + disconnect_icon_xpath + "|" +
                                   row_identifier_xpath2 + disconnect_icon_xpath + "|" +
                                   row_identifier_xpath3 + disconnect_icon_xpath + "|" +
                                   row_identifier_xpath4 + disconnect_icon_xpath + "|" +
                                   row_identifier_xpath5 + disconnect_icon_xpath + "|" +
                                   row_identifier_xpath6 + disconnect_icon_xpath)
            else:
                new_browser.move_to_the_element('xpath',
                                                    modal_xpath + row_identifier_xpath1 + "|" +
                                                    modal_xpath + row_identifier_xpath2 + "|" +
                                                    modal_xpath + row_identifier_xpath3 + "|" +
                                                    modal_xpath + row_identifier_xpath4 + "|" +
                                                    modal_xpath + row_identifier_xpath5 + "|" +
                                                    modal_xpath + row_identifier_xpath6)
                self.click_element('xpath',
                                   modal_xpath + row_identifier_xpath1 + disconnect_icon_xpath + "|" +
                                   modal_xpath + row_identifier_xpath2 + disconnect_icon_xpath + "|" +
                                   modal_xpath + row_identifier_xpath3 + disconnect_icon_xpath + "|" +
                                   modal_xpath + row_identifier_xpath4 + disconnect_icon_xpath + "|" +
                                   modal_xpath + row_identifier_xpath5 + disconnect_icon_xpath + "|" +
                                   modal_xpath + row_identifier_xpath6 + disconnect_icon_xpath)
            self.ui_helper.wait_for_page_data_to_be_rendered()
            logger.debug2("Clicked on disconnect button for the entry:" + row_identifier)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Unable to click disconnect icon")

    # FUNCTIONALITY     : Clicks on edit icon after hovering on the desired entry
    # INPUT             : the name of row entry(row identifier)
    # RETURNS           : None
    def click_on_delete_element_after_hovering(self, row_identifier, modal=False):
        try:
            row_identifier_xpath1 = "//td/div[text()='" + row_identifier + "']"
            row_identifier_xpath2 = "//td/div/div[text()='" + row_identifier + "']"
            row_identifier_xpath3 = "//div[text()='" + row_identifier + "' and contains(@class, 'sw-table-row')]"
            row_identifier_xpath4 = "//div[contains(text(),'" + row_identifier + "') and contains(@class, 'sw-table-row')]"
            row_identifier_xpath5 = "//div[contains(@class, 'sw-table-row')]/following::*[text()='" + row_identifier + "']"
            row_identifier_xpath6 = "//div[contains(@class, 'sw-table-row')]/following::*[contains(text(), '" + row_identifier + "')]"
            trash_icon_xpath = "/following::*[contains(@class,'icon-trash')]"
            modal_xpath = "//div[contains(@class, 'sw-modal__main-body')]//following::"
            if modal is False:

                new_browser.move_to_the_element('xpath',
                                                    row_identifier_xpath1 + "|" +
                                                    row_identifier_xpath2 + "|" +
                                                    row_identifier_xpath3 + "|" +
                                                    row_identifier_xpath4 + "|" +
                                                    row_identifier_xpath5 + "|" +
                                                    row_identifier_xpath6)
                self.click_element('xpath',
                                   row_identifier_xpath1 + trash_icon_xpath + "|" +
                                   row_identifier_xpath2 + trash_icon_xpath + "|" +
                                   row_identifier_xpath3 + trash_icon_xpath + "|" +
                                   row_identifier_xpath4 + trash_icon_xpath + "|" +
                                   row_identifier_xpath5 + trash_icon_xpath + "|" +
                                   row_identifier_xpath6 + trash_icon_xpath)
            else:
                new_browser.move_to_the_element('xpath',
                                                    modal_xpath + row_identifier_xpath1 + "|" +
                                                    modal_xpath + row_identifier_xpath2 + "|" +
                                                    modal_xpath + row_identifier_xpath3 + "|" +
                                                    modal_xpath + row_identifier_xpath4 + "|" +
                                                    modal_xpath + row_identifier_xpath5 + "|" +
                                                    modal_xpath + row_identifier_xpath6)
                self.click_element('xpath',
                                   modal_xpath + row_identifier_xpath1 + trash_icon_xpath + "|" +
                                   modal_xpath + row_identifier_xpath2 + trash_icon_xpath + "|" +
                                   modal_xpath + row_identifier_xpath3 + trash_icon_xpath + "|" +
                                   modal_xpath + row_identifier_xpath4 + trash_icon_xpath + "|" +
                                   modal_xpath + row_identifier_xpath5 + trash_icon_xpath + "|" +
                                   modal_xpath + row_identifier_xpath6 + trash_icon_xpath)
            self.ui_helper.wait_for_page_data_to_be_rendered()
            logger.debug2("Clicked on delete button for the entry:" + row_identifier)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Unable to click delete icon")

    # FUNCTIONALITY     : Select List value
    # INPUT             : UI Label of the list
    # RETURNS           : True/ False, based on verification
    def select_drop_down_value(self, select_identifier, select_value, modal=False):
        try:
            logger.debug2("Selecting drop down value \t: "+ str(select_value))
            if modal is True:
                self.click_element('xpath', "//div[contains(@class, 'sw-modal__main-body')]"
                                            "//following::*[contains(text(), '"+select_identifier+"')]"
                                            "/following::*[contains(@class, 'sw-select__icon')]")
            else:
                self.click_element('xpath', "//span[contains(text(), '"+select_identifier+"')]/following::*"
                                        "[contains(@class, 'sw-select__icon')]")
            element = new_browser.move_to_the_element('xpath',  "//span[contains(text(), '"+select_identifier+"')]"
                                                                    "/following::div[contains(@class, 'sw-dropdown')]/"
                                                                    "span[text()='"+ select_value+"']", False)
            element.click()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Action - Unable to select from drop down list")

    # FUNCTIONALITY     : Waits for Success message in an alert box and accept alert
    # INPUT             : None
    # RETURNS           : None
    def wait_for_success_alert(self):
        try:
            logger.debug2("Waiting for success message")
            new_browser.wait_for_text("Success")
            self.accept_alert()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Wait for success alert failed")

    # FUNCTIONALITY     : Waits for success message in banner and close it
    # INPUT             : None
    # RETURNS           : None
    def wait_for_success_banner(self):
        try:
            logger.debug2("Waiting for success message")
            new_browser.wait_for_text("Success")
            self.click_close_icon()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Wait for success banner failed")

    def wait_for_changes_made(self):
        try:
            logger.debug2("Waiting for changes made message")
            new_browser.wait_for_text("Changes made.")
            self.accept_alert()
            self.ui_helper.wait_for_page_data_to_be_rendered()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Wait for changes made banner failed")

    # FUNCTIONALITY     : Retrieves info icon text on hover
    # INPUT             : UI Label the info icon pertaining
    # RETURNS           : string in case of a single line/ list in case of multiple lines
    def retrieve_info_icon_text(self, label):
        logger.debug2("Retrieving info icon text from : " +label)
        new_browser.click_element('xpath', "//span[contains(text(), '"+label+"')]/following::*"
                                                                "[contains(@class, 'icon-info')]")
        elements = new_browser.get_elements('xpath', "//div[contains(@class, 'sw-tooltip__inner')]//span")
        if len(elements) == 1:
            return elements[0]
        else:
            return elements

    # FUNCTIONALITY     : Verify info icon text on hover
    # INPUT             : UI Label the info icon pertaining, verification list/string
    # RETURNS           : True/ False, based on verification
    def verify_info_icon_text(self, label, statement):
        try:
            data = self.retrieve_info_icon_text(label)
            data_texts =[]
            if type(data) is list:
                logger.debug2("Retrieved list data from info icon")
                for line in data:
                    logger.degridbug2("Data : "+ line.text)
                    data_texts.append(line.text)
                for value in statement:
                    logger.debug2("Finding string : " + value)
                    if value not in data_texts:
                        logger.debug2("Info text not found")
                        return False
            else:
                logger.debug2("Finding string : " + str(statement))
                if data != statement:
                    logger.debug2("Info text not found")
                    return False
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Verification of info text failed")

    # FUNCTIONALITY     : Select List value from a obiect
    # INPUT             : object, UI Label of the list
    # RETURNS           : True/ False, based on verification
    def select_obj_drop_down_value(self, obj, field_val=None):
        try:
            logger.debug2("Selecting drop down value \t: "+ str(field_val))
            obj.click()
            object = new_browser.get_invisible_element('xpath', '//*[text() = "' + field_val + '"]')
            new_browser.move_to_the_element(object)
            object.click()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Action - Unable to select from drop down list")

    # FUNCTIONALITY     : Gets only custom data by filtering
    # INPUT             : None
    # RETURNS           : None
    def filter_custom_data(self):
        try:
            logger.debug("Action - Getting only custom data")
            new_browser.click_element('class', "icon-filter")
            new_browser.click_element('xpath', '//*[contains(text(),"Custom")]')
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to filter custom data")

    # FUNCTIONALITY     : Configures text field
    # INPUT             : UI Label of the text field
    # RETURNS           : None
    def configure_text_field(self, text_box_label, text_value):
        try:
            logger.debug("Configure - Text field "+text_box_label+" with value  \t: "+ str(text_value))
            new_browser.set_text_field('xpath', '//div[contains(@class,"label") and text()="'+text_box_label+'"]/'
                                                    'following::input[@type="text" or @type="password"]|'
                                                    '//div[contains(@class, "label")]/span[text()="'+text_box_label+'"]/'
                                                    'following::input[@type="text" or @type="password"]|'
                                                    '//div[contains(@class, "label")]/span[contains(text(), "'+text_box_label+'")]/'
                                                    'following::input[@type="text" or @type="password"]|'
                                                    '//div[contains(@class, "label") and contains(text(),"'+text_box_label+'")]/'
                                                    'following::input[@type="text" or @type="password"]', text_value)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Configure - Unable to set text field")

    # FUNCTIONALITY     : Set radio button
    # INPUT             : UI Label of the radio button
    # RETURNS           : None
    def configure_radio_button(self, radio_button_label, group_name=None):
        try:
            logger.debug("Configure - Setting radio button \t: "+ str(radio_button_label ))
            if group_name is not None:
                new_browser.click_element('xpath',
                                              "//span[contains(text(), '" + group_name + "')]/following::*[contains(text(), '" + radio_button_label + "')]")
            else:
                new_browser.click_element('xpath','//span[text()="'+radio_button_label+'"]')

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Configure - Unable to set radio button")

    # FUNCTIONALITY     : Select toggle button
    # INPUT             : UI Label of the toggle button
    # RETURNS           : None
    def configure_toggle_button(self, toggle_label, configure_value, group_name=None, modal=False, label=True, position=None):
        try:
            self.ui_helper.wait_for_page_data_to_be_rendered()
            logger.debug('Configure - Toggling ' + toggle_label + ' with value \t: ' + str(configure_value))
            modal_xpath = '//div[contains(@class, "sw-modal__main-body")]'
            togglelabelxpath = 'div[contains(@class,"label")]'
            groupname_xpath1 = '//div[contains(text(), "' + str(group_name) + '")]'
            groupname_xpath2 = '//span[contains(text(), "' + str(group_name) + '")]'
            togglelabel_xpath1 = '//span[text()="' + toggle_label + '"]'
            togglelabel_xpath2 = '//span[contains(text(),"' + toggle_label + '")]'
            togglelabel_xpath3 = '//*[contains(text(), "' + toggle_label + '")] '
            groupname_xpath = [groupname_xpath1, groupname_xpath2]
            togglelabel_xpath = [togglelabel_xpath1, togglelabel_xpath2, togglelabel_xpath3]
            togglebutton_xpath = '/following::*[contains(@class,"sw-toggle")]'
            xpath_list = []

            for togglelabel in togglelabel_xpath:
                xpath = ''
                if modal is True:
                    xpath = xpath + modal_xpath
                if group_name is not None:
                    for groupname in groupname_xpath:
                        if label is True:
                            xpath_list.append(
                                xpath + groupname + '/following::' + togglelabelxpath + togglelabel + togglebutton_xpath)
                        else:
                            xpath_list.append(xpath + groupname + togglelabel + togglebutton_xpath)
                else:
                    if label is True:
                        xpath_list.append(xpath + '//' + togglelabelxpath + togglelabel + togglebutton_xpath)
                    else:
                        xpath_list.append(xpath + togglelabel + togglebutton_xpath)

            for xpath in xpath_list:
                if new_browser.does_element_exist_now('xpath', xpath):
                    elements = new_browser.get_elements('xpath', xpath)
                    element_status = True
                    if position is None:
                        position = 0
                    else:
                        position = position - 1

                    element = elements[position]
                    class_value = element.get_attribute("class")
                    if "sw-toggle--off" in class_value:
                        element_status = False
                    if element_status != configure_value:
                        logger.debug("Action - Toggling Element")
                        element.click()
                    return True

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Configure - Unable to toggle")

    # FUNCTIONALITY     : Configures text area
    # INPUT             : UI Label of the text area
    # RETURNS           : None
    def configure_text_area(self, text_area_label, text_area_value):
        try:
            logger.debug("Configure - Text field " + text_area_label + " with value  \t: " + str(text_area_value))
            new_browser.set_text_field('xpath', '//div[contains(@class,"text_area_label")]/span[text()="' + text_area_label + '"]/following::textarea', text_area_value)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Configure - Unable to set text area")

    # FUNCTIONALITY     : Gets the error message on the UI and compares it with the error message sent
    # INPUT             : Expected error message
    # RETURNS           : None
    def compare_error_message(self, errorMsg):
        try:
            errorMessage = new_browser.get_element('class', "sw-status-info__text__message")
            logger.debug2("Actual Error text\t: " + str(errorMessage.text))
            logger.debug2("Expected Error text\t: " + str(errorMsg))
            if type(errorMsg) is list:
                if errorMessage.text in errorMsg:
                    logger.debug(errorMessage.text)
                    return True
                else:
                    logger.info("Error Message mismatch:\t" + errorMessage.text)
                    raise Exception
            else:
                if errorMessage.text == errorMsg:
                    logger.debug(errorMessage.text)
                    return True
                else:
                    logger.info("Error Message mismatch:\t"+errorMessage.text)
                    raise Exception
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Error Message verification failed")

    # FUNCTIONALITY     : Verify error message on the UI
    # INPUT             : Expected error message
    # RETURNS           : None
    def verify_error_message_banner(self, errorMsg):
        try:
            self.ui_helper.compare_error_message(errorMsg)
            self.click_close_icon()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Error Message verification failed")

    # FUNCTIONALITY     : Verifies and accepts error alert
    # INPUT             : Expected error message
    # RETURNS           : None
    def verify_error_message_alert(self, errorMsg):
        try:
            self.ui_helper.compare_error_message(errorMsg)
            self.ui_helper.accept_alert()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Accept Error Message failed")

    # FUNCTIONALITY     : Imports file
    # INPUT             : Import button label, Path of the file that needs to be imported
    # RETURNS           : None
    def import_file(self, import_label, file_path):
        try:
            logger.debug("Configure - Import Signatures ")
            new_browser.move_to_the_element('class',
                                        'sw-file-upload')
            element = new_browser.get_element('xpath',
                                           '//div[contains(@class,"label")]/span[text()="' + import_label + '"]/following::button[@type="button"]')
            element.send_keys(file_path)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Configure - Unable to set text area")

    # FUNCTIONALITY     : Waits for complete page load
    # INPUT             : None
    # RETURNS           : None
    def wait_for_complete_page_load(self):
        try:
            page_state = self.browser.execute_script('return document.readyState;')
            time.sleep(1)
            while(page_state !='complete' and i<10):
                time.sleep(1)
                page_state = self.browser.execute_script('return document.readyState;')
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Complete page load failed")


    # FUNCTIONALITY     : Retrieve text field value
    # INPUT             : UI Label of the text field
    # RETURNS           : None
    def get_text_field_value(self, text_box_label):
        try:
            logger.debug("Get - Text field  " + text_box_label + "  value ")
            ele = new_browser.get_element('xpath',
                                           '//div[contains(@class,"label")]/span[text()="' + text_box_label + '"]/following::input[@type="text"]')
            value = ele.text
            return value
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Unable to get text field value")

    # FUNCTIONALITY     : Retrieve text field value by attribute
    # INPUT             : UI Label of the text field
    # RETURNS           : None
    def get_text_field_value_by_attribute(self, text_box_label):
        try:
            logger.debug("Get - Text field  " + text_box_label + "  value ")
            ele = new_browser.get_element('xpath','//div[contains(@class,"label") and text()="'+text_box_label+'"]/'
                                                    'following::input[@type="text" or @type="password"]|'
                                                    '//div[contains(@class, "label")]/span[text()="'+text_box_label+'"]/'
                                                    'following::input[@type="text" or @type="password"]|'
                                                    '//div[contains(@class, "label")]/span[contains(text(), "'+text_box_label+'")]/'
                                                    'following::input[@type="text" or @type="password"]|'
                                                    '//div[contains(@class, "label") and contains(text(),"'+text_box_label+'")]/'
                                                    'following::input[@type="text" or @type="password"]')
            value = ele.get_attribute('value')
            logger.debug("Value : " + str(value))
            return value
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Unable to get text field value")

    # FUNCTIONALITY     : Get radio button value
    # INPUT             : UI Label of the radio button
    # RETURNS           : None
    def get_radio_button_value(self, radio_button_label):
        try:
            logger.debug("Get -  Radio button value \t: " + str(radio_button_label))
            ele = new_browser.get_element('xpath',
                                              '//span[text()="' + radio_button_label + '"]/preceding::*[contains(@class, "sw-radio__fake-radio-button")]')
            class_value = ele.get_attribute('class')
            if 'sw-radio__fake-radio-button--checked' in class_value:
                return True
            else:
                return False
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Unable to get radio button")

    # FUNCTIONALITY     : Get toggle button value
    # INPUT             : UI Label of the toggle button
    # RETURNS           : None
    def get_toggle_button_value(self, toggle_label):
        try:
            logger.debug("Get - Toggle Value " + toggle_label)
            ele = new_browser.get_element('xpath',
                                              '//div/span[text()="' + toggle_label + '"]/following::*[contains(@class,"sw-toggle")]')
            class_value = ele.get_attribute('class')
            if 'sw-toggle--off' in class_value:
                return False
            else:
                return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Unable to get toggle value")

    # FUNCTIONALITY     : Get text area value
    # INPUT             : UI Label of the text area
    # RETURNS           : None
    def get_text_area_value(self, text_area_label):
        try:
            logger.debug("Get - Text field " + text_area_label + "  value ")
            ele = new_browser.get_element('xpath',
                                              '//div[contains(@class,"label")]/span[text()="' + text_area_label + '"]/following::textarea')
            value = ele.text
            return value
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Unable to get text area value")

    # FUNCTIONALITY     : Get Select List value
    # INPUT             : UI Label of the list
    # RETURNS           : True/ False, based on verification

    def get_drop_down_value(self, select_identifier):
        try:
            logger.debug2("Getting drop down value \t: " + str(select_identifier))
            ele = self.get_element('xpath',
                                   "//span[contains(text(), '" + select_identifier + "')]/following::*[contains(@class, 'sw-select__label-text')]")
            value = ele.text
            return value
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Action - Unable to select from drop down list")

    # FUNCTIONALITY     : Add content values to the list (text_field)
    # INPUT             : Text field value and text field label
    # RETURNS           : None
    def add_text_list(self, text_field_label, text_field_value):
        try:
            logger.debug("Configure - Text field " + text_field_label + " with value  \t: " + str(text_field_value))
            self.configure_text_field(text_field_label, text_field_value)
            new_browser.click_element('xpath',
                                          '//div[contains(@class,"label")]/span[text()="'+text_field_label+'"]/following::span[contains(@class,"icon-add")]')
            logger.debug2(text_field_value + "\t value is added to  the "+text_field_label+" list")
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Configure - Unable to add to the list")


    # FUNCTIONALITY     : Add content values to the list(drop_down)
    # INPUT             : Drop Down value
    # RETURNS           : None
    def add_drop_down_list(self, select_identifier, select_value):
        try:
            logger.debug("Configure - Drop down" + select_identifier + " with value  \t: " + str(select_value))
            self.select_drop_down_value(select_identifier, select_value)
            new_browser.click_element('xpath',
                                          '//div[contains(@class,"label")]/span[text()="'+select_identifier+'"]/following::span[contains(@class,"icon-add")]')
            logger.debug2(select_value + "\t value is added to  the "+select_identifier+" list")
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Configure - Unable to add to the list")

    # FUNCTIONALITY     : Retrieves only integer from a string
    # INPUT             : String
    # RETURNS           : Integers
    def retrieve_integer(self, value):
        if value.isdigit():
            return value
        else:
            # value = re.match(r'(^\d+$)',value).group(0)
            for val in value:
                if not val.isdigit():
                    value = value.replace(val, "")
            print(value)
            return value

    # FUNCTIONALITY     : Select List Values
    # INPUT             : List/ String
    # RETURNS           : None
    def select_group_values(self, select_list, tree="left"):
        try:
            logger.debug("Action - Select tree group values")
            if type(select_list) is not list:
                select_list[0] = select_list

            for select_value in select_list:
                self.click_element('xpath', "//div[@class='selector-"+tree+"']//*[contains(@class, 'sw-tree-list-item') and text()='"+select_value+"']")
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to select all tree values")

    # FUNCTIONALITY     : Select List Values
    # INPUT             : List/ String
    # RETURNS           : None
    def select_tree_values(self, select_list):
        try:
            logger.debug("Action - Select tree list values")
            self.select_group_values(select_list)
            self.click_forward_tree_play_icon()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to move forward tree values")

    # FUNCTIONALITY     : De-Select List Values
    # INPUT             : List/ String
    # RETURNS           : None
    def unselect_tree_values(self, select_list):
        try:
            logger.debug("Action - Select tree list values")
            self.select_group_values(select_list, tree='right')
            self.click_reverse_tree_play_icon()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to move reverse tree values")

    # FUNCTIONALITY     : Click on forward tree play icon
    # INPUT             : None
    # RETURNS           : None
    def click_forward_tree_play_icon(self):
        try:
            logger.debug("Action - Clicking Forward Play Icon")
            new_browser.click_element('xpath', "//div[@class='selector-middle']//*"
                                                   "/span[contains(@style, 'rotate(0deg);')]"
                                                   "//*[contains(@class, 'icon-play')]")
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to click forward play icon")

    # FUNCTIONALITY     : Click on forward tree play icon
    # INPUT             : None
    # RETURNS           : None
    def click_reverse_tree_play_icon(self):
        try:
            logger.debug("Action - Clicking Reverse Play Icon")
            new_browser.click_element('xpath', "//div[@class='selector-middle']//*"
                                                   "/span[contains(@style, 'rotate(180deg);')]"
                                                   "//*[contains(@class, 'icon-play')]")
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to click reverse play icon")

    # FUNCTIONALITY     : Click on forward play icon
    # INPUT             : None
    # RETURNS           : None
    def click_forward_play_icon(self):
        try:
            logger.debug("Action - Clicking Forward Play Icon")
            new_browser.click_element('xpath', "//span[contains(@style, 'rotate(0deg);')]"
                                                   "//*[contains(@class, 'icon-play')]")
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to click forward play icon")

    # FUNCTIONALITY     : Click on reverse play icon
    # INPUT             : None
    # RETURNS           : None
    def click_reverse_select_icon(self):
        try:
            logger.debug("Action - Clicking Reverse Play Icon")
            new_browser.click_element('xpath', "//span[contains(@style, 'rotate(180deg);')]"
                                                   "//*[contains(@class, 'icon-play')]")
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to click reverse play icon")

    # FUNCTIONALITY     : Click on forward all play icon
    # INPUT             : None
    # RETURNS           : None
    def click_forward_all_play_icon(self):
        try:
            logger.debug("Action - Clicking Forward All Play Icon")
            new_browser.click_element('xpath', "//span[contains(@style, 'rotate(180deg);')]"
                                                   "//*[contains(@class, 'icon-forward')]")
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to click forward all play icon")

    # FUNCTIONALITY     : Click on reverse all play icon
    # INPUT             : None
    # RETURNS           : None
    def click_reverse_all_select_icon(self):
        try:
            logger.debug("Action - Clicking Reverse All Play Icon")
            new_browser.click_element('xpath', "//span[contains(@style, 'rotate(0deg);')]"
                                                   "//*[contains(@class, 'icon-backward')]")
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to click reverse all play icon")

    def verify_left_tree_value(self, tree_list):
        if type(tree_list) is not list:
            tree_list[0] = tree_list

        for tree_value in tree_list:
            if not new_browser.does_element_exist('xpath', "//div[@class='selector-left']"
                                                               "//*[contains(@class, 'sw-tree-list-item') "
                                                               "and text()='" + tree_value + "']"):
                return False
        return True

    def verify_right_tree_value(self, tree_list):
        if type(tree_list) is not list:
            tree_list[0] = tree_list

        for tree_value in tree_list:
            if not new_browser.does_element_exist('xpath', "//div[@class='selector-right']"
                                                               "//*[contains(@class, 'sw-tree-list-item') "
                                                               "and text()='" + tree_value + "']"):
                return False
        return True

    # FUNCTIONALITY     : Select Checkbox button
    # INPUT             : checkbox_label :  UI Label of the Checkbox button
    #                   : configure_value : Boolean
    # RETURNS           : None
    def configure_checkbox_button(self, checkbox_label, configure_value):
        try:
            logger.debug("Configure - Checkbox " + checkbox_label + " with value \t: " + str(configure_value))
            new_browser.checkbox_button('xpath',
                                            "//div[contains(text(), '" + checkbox_label + "')]/preceding-sibling::div[contains(@class,'sw-checkbox__box')]/div[contains(@class, 'checkbox__box__mark')]",
                                            configure_value)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Configure - Unable to Checkbox")

    # FUNCTIONALITY     : Clicks submit when new window has same element as the base window
    # INPUT             :
    # RETURNS           :
    def submit_modal(self):
        try:
            logger.debug("Action - Clicking on Save button in modal")
            new_browser.click_element('xpath', "//div[contains(@class, 'sw-modal--pillar') and @style!='display: none;']//button[text()='Accept']")
            self.ui_helper.wait_for_page_data_to_be_rendered()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to click submit icon in modal")

    # FUNCTIONALITY     : Clicks cancel when new window has same element as the base window
    # INPUT             : None
    # RETURNS           : None
    def cancel_modal(self):
        try:
            logger.debug("Action - Clicking on Cancel button in modal")
            new_browser.click_element('xpath', "//div[contains(@class, 'sw-modal--pillar') and @style!='display: none;']//button[text()='Cancel']")
            self.ui_helper.wait_for_page_data_to_be_rendered()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to click cancel button")

    # FUNCTIONALITY     : Get Check box value
    # INPUT             : UI Label of the list
    # RETURNS           : True/ False, based on verification
    def get_checkbox_value(self, select_identifier):
        try:
            logger.debug2("Getting check box value \t: " + str(select_identifier))
            time.sleep(1)
            ele = new_browser.get_element('xpath',  "//div[contains(text(), '" + select_identifier +"')]"
                                                        "/preceding-sibling::div[contains(@class,'sw-checkbox__box')]"
                                                        "/div[contains(@class, 'checkbox__box__mark')]", visibility=False)
            class_value = ele.get_attribute('class')
            if "sw-checkbox__box__mark--no" in class_value:
                return False
            else:
                return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Action - Unable to get checkbox value")

    # FUNCTIONALITY     : Waits for all buffer to disappear
    # INPUT             : None
    # RETURNS           : None
    def wait_for_page_data_to_be_rendered(self):
        logger.info("Waiting for page data to be rendered completely!")
        self.ui_helper.wait_for_element_to_be_invisible('xpath', '//div[contains(@class, "sw-blocking-progress")]')