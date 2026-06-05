import chromedriver_autoinstaller
import time
import re
import os
import shutil
import platform

from pytest_resources.common_require import *
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from libs.common_lib import *


class Browser:

    def get_browser(self, ula=False):
        try:
            # Close any existing browser session
            com_obj = CommonLib()
            com_obj.kill_process(process_name='chrome.exe')
            com_obj.kill_process(process_name='chromedriver.exe')
            logger.info('Launching Google Chrome browser')
            options = webdriver.ChromeOptions()
            chromedriver_autoinstaller.install()
            if ula:
                logger.info("Not ignoring certificate errors")
            else:
                options.add_argument('--ignore-certificate-errors')
            options.add_argument('-safebrowsing-disable-download-protection')
            options.add_argument('safebrowsing-disable-extension-blacklist')
            options.add_argument('--guest')
            options.add_experimental_option("useAutomationExtension", False)
            options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
            options.add_experimental_option('detach', True)
            self.browser = webdriver.Chrome(options=options)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.error("Browser startup failed")

    # Maximize the current web browser window
    def maximize_window(self):
        self.browser.maximize_window()

    # Go to specified url
    def go_to_url(self, url):
        try:
            self.browser.get(url)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.error("URL Access failed..")

    # Waits for the element visibility until given period of time.
    def wait_for_element_to_be_visible(self, attrib, attrib_val, wait_time=180):
        try:
            logger.info("Waiting for the element to be visible")
            selector = self.get_selenium_selector(attrib)
            logger.info("Selenium selector attribute \t: [" + attrib + "]")
            logger.info("Selenium selector value \t: [" + attrib_val + "]")
            return WebDriverWait(self.browser, wait_time).until(
                EC.visibility_of_element_located((selector, attrib_val)))
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.error("Expected Condition : Element not visible")

    # Check whether the given string is present in web pag ot not.
    def does_page_have_text(self, text_to_search):
        logger.info("Checking if {} page is loaded.".format(self.browser.current_url))
        # page_state = self.browser.execute_script('return document.readyState;')
        page_state = None
        for attempt in range(5):
            try:
                i = 0
                while page_state != 'complete' and i < 10:
                    page_state = self.browser.execute_script('return document.readyState;')
                    logger.info("page state is :" + page_state + "...")
                    i += 1
            except JavascriptException:
                logger.error("Caught JavascriptException exception. Retrying to get page load status...")
                continue
            if attempt == 5:
                logger.info("Number of maximum retrying is done...")
                break
        src1 = self.browser.page_source
        # removes html tags like <b>..</b>, <i></i>,. etc from page source.
        html_tag = re.compile(r'<[^>]+>')
        src2 = html_tag.sub('', src1)
        text_found = re.search(re.escape(text_to_search), src2)
        if text_found is not None:
            return True
        else:
            return False

    # Wait for the text to appear for a fixed time
    def wait_for_text(self, text, wait_time=15):
        logger.info("Waiting for text \t: " + str(text))
        i = 0
        try:
            while i <= wait_time and not self.does_page_have_text(text):
                # Sleep while waiting for text to appear
                time.sleep(1)
                logger.info('Timeout: ' + str(i) + ' seconds elapsed waiting for "' + text + '"')
                i += 1
            assert i < wait_time, 'ERR: ' + str(wait_time) + ' seconds elapsed waiting for "' + text + '" to appear'
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.error("Page State : Unable to wait for text")
            raise

    # Return any given html attribute value
    def get_selenium_selector(self, attrib):
        try:
            if attrib == "name":
                return By.NAME
            elif attrib == "id":
                return By.ID
            elif attrib == "class":
                return By.CLASS_NAME
            elif attrib == "xpath":
                return By.XPATH
            elif attrib == "css":
                return By.CSS_SELECTOR
            elif attrib == "link_text":
                return By.LINK_TEXT
            elif attrib == "partial_link_text":
                return By.PARTIAL_LINK_TEXT
            elif attrib == "tag_name":
                return By.TAG_NAME
            else:
                raise AssertionError
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.error("Invalid selenium selector")

    # Set text_field, select_list, radio button and checkbox
    # by element's name, id, class, xpath and css-selector attributes
    def set_element(self, element, attrib, attrib_val, field_val=None):
        self.wait_for_element_to_be_visible(attrib, attrib_val)
        obj = None
        if attrib == "name":
            obj = self.browser.find_element(By.NAME, attrib_val)
        elif attrib == "id":
            obj = self.browser.find_element(By.ID, attrib_val)
        elif attrib == "class":
            obj = self.browser.find_element(By.CLASS_NAME, attrib_val)
        elif attrib == "xpath":
            obj = self.browser.find_element(By.XPATH, attrib_val)
        elif attrib == "css":
            obj = self.browser.find_element(By.CSS_SELECTOR, attrib_val)

        if element == "text_field":
            obj.send_keys(field_val)
        elif element == "select_list":
            Select(obj).select_by_visible_text(field_val)
        elif element == "check_box":
            obj.send_keys(Keys.SPACE)

        else:
            obj.click()

    # return an html element object.
    def get_element(self, attrib, attrib_val, visibility=True):
        try:
            logger.info("Getting element")
            if visibility:
                self.wait_for_element_to_be_visible(attrib, attrib_val)
            selector = self.get_selenium_selector(attrib)
            obj = self.browser.find_element(selector, attrib_val)
            return obj
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.error("Element : Unable to get element")

    # Click any element
    def click_element(self, attrib, attrib_val):
        retries = 0
        while retries < 10:
            retries = retries + 1
            try:
                self.wait_for_element_to_be_visible(attrib, attrib_val)
                obj = self.get_element(attrib, attrib_val)
                obj.click()
                return True
            except Exception as err:
                logger.error("Exception \t: " + str(err))
                logger.error("Click Exception : Retrying action")
                time.sleep(2)
                retries = retries + 1
                if retries < 10:
                    continue
                else:
                    logger.error("Exception \t: " + str(err))
                    logger.error("Action - Unable to click element")

    # return any given html attribute value
    def get_attribute_value(self, attrib_to_identify, attrib_val, attrib_to_get_val, visibility=True):
        try:
            logger.info("Getting attribute value for \t: " + str(attrib_to_get_val))
            if visibility:
                self.wait_for_element_to_be_visible(attrib_to_identify, attrib_val)
            selector = self.get_selenium_selector(attrib_to_identify)
            obj = self.browser.find_element(selector, attrib_val)
            return obj.get_attribute(attrib_to_get_val)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.error("Element : Unable to get attribute value of the element")

    # check whether the element is enabled
    def is_element_enabled(self, attrib, attrib_val):
        obj = None
        if attrib == "name":
            obj = self.browser.find_element(By.NAME, attrib_val)
        elif attrib == "id":
            obj = self.browser.find_element(By.ID, attrib_val)
        elif attrib == "class":
            obj = self.browser.find_element(By.CLASS_NAME, attrib_val)
        elif attrib == "xpath":
            obj = self.browser.find_element(By.XPATH, attrib_val)
        elif attrib == "css":
            obj = self.browser.find_element(By.CSS_SELECTOR, attrib_val)
        elif attrib == "link_text":
            obj = self.browser.find_element(By.LINK_TEXT, attrib_val)
        elif attrib == "partial_link_text":
            obj = self.browser.find_element(By.PARTIAL_LINK_TEXT, attrib_val)

        if obj.is_enabled():
            return True
        else:
            return False

    # Close the browser.
    def close_browser(self):
        self.browser.quit()

    # switches from one window to another
    def switch_window(self):
        for handle in self.browser.window_handles:
            self.browser.switch_to.window(handle)

    # Get browser handles
    def get_browser_all_handles(self):
        all_handles = self.browser.window_handles
        logger.info(all_handles)
        return all_handles

