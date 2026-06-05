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
import shutil
import platform
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
if 'ubuntu' not in platform.version().lower():
    from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import unquote
from collections import OrderedDict
from runner.settings import logger
from runner.utils.assertion import Assertion


class Browser:

    def _get_firefox_profile(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.dir", "/root/Downloads")
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", ",".join([
            "application/x-tar", "application/gzip", "application/x-gzip", "application/octet-stream",
            "application/x-gtar", "application/tar", "application/x-tgz", "application/zip", "text/csv",
            "application/csv", "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/xml", "text/xml"
        ]))
        profile.set_preference("security.insecure_field_warning.contextual.enabled", False)
        profile.set_preference("devtools.console.stdout.content", True)  # log
        return profile

    def get_firefox_with_head(self, headless=False):
        retries = 0
        max_retries = 6
        driver_dir = '/tmp/UI7/webdrivers'
        driver_path = os.path.join(driver_dir, 'geckodriver')
        log_path = os.path.join(driver_dir, 'geckodriver.log')
        source_driver = os.environ["PYTHON_COMMON_HOME"]+'/modules/UI7/webdrivers/centos/geckodriver'

        while retries < max_retries:
            try:
                logger.debug2("Starting Firefox Browser...")
                logger.info('killing existing Firefox process...')
                os.system("pkill firefox")

                # mkdir for webdriver
                os.makedirs(driver_dir, exist_ok=True)

                # copy geckodriver
                if not os.path.exists("/tmp/UI7/webdrivers/geckodriver"):
                    shutil.copy2(source_driver, driver_path)
                    logger.info(f"Copied geckodriver to {driver_path}")
                    time.sleep(2)
                    os.chmod(driver_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # mode:777

                # touch file for log
                if not os.path.exists(log_path):
                    os.mknod(log_path)

                # Firefox Options
                firefox_options = Options()
                firefox_options.add_argument('--ignore-certificate-errors')
                if headless:
                    firefox_options.add_argument('--headless')

                # profile
                profile = self._get_firefox_profile()

                # Capabilities
                caps = DesiredCapabilities.FIREFOX.copy()
                caps["marionette"] = True
                caps['acceptSslCerts'] = True

                # launch browser...
                self.browser = webdriver.Firefox(executable_path=driver_path,
                                                 firefox_profile=profile,
                                                 options=firefox_options,
                                                 capabilities=caps,
                                                 service_log_path=log_path)
                logger.info("Firefox Browser started successfully")
                break
            except Exception as err:
                logger.error(f"Exception occurred during Firefox startup: {err}")
                logger.error(traceback.format_exc())
                logger.info("Browser startup failed")
                logger.info("Print geckodriver log")
                log_content = os.popen(f"cat {log_path}").read()
                logger.info("Geckodriver log output:\n" + log_content)

                retries += 1
                if retries < max_retries:
                    logger.info(f"Retrying... Attempt {retries}/{max_retries}")
                    time.sleep(10)
                else:
                    logger.error("Failed to start Firefox browser after all retries")

    def get_chrome_with_head(self, headless=False):
        try:
            logger.debug2("Starting Chrome Browser")
            logger.info('killing existing Chrome process...')
            os.system("pkill chrome")
            time.sleep(2)

            webdriver_src = os.environ["PYTHON_COMMON_HOME"] + '/tools/webdriver/chromedriver'
            webdriver_dst_dir = "/tmp/UI7/webdrivers"
            webdriver_dst = os.path.join(webdriver_dst_dir, "chromedriver")
            os.makedirs(webdriver_dst_dir, exist_ok=True)

            if not os.path.exists(webdriver_dst):
                shutil.copy2(webdriver_src, webdriver_dst)
                logger.info(f"Copied chromedriver to {webdriver_dst_dir}")

            os.chmod(webdriver_dst, 0o777)

            logger.info("Configuring Chrome options...")
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('ignore-certificate-errors')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.binary_location = '/usr/bin/google-chrome'
            chrome_options.add_argument("window-size=1920,1080")

            if headless:
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--disable-gpu')

            logger.info('Starting Chrome browser..')
            self.browser = webdriver.Chrome(executable_path=webdriver_dst, chrome_options=chrome_options)

            logger.info("Browser Chrome started successfully")
        except Exception as err:
            logger.error("Exception occurred during Chrome startup:\n" + traceback.format_exc())
            print("Browser startup failed")

    def get_browser(self):
        retries = 0
        max_retries = 6
        while retries < max_retries:
            try:
                logger.debug2("Starting Browser")
                if not os.path.exists("/tmp/UI7/webdrivers/"):
                    os.makedirs("/tmp/UI7/webdrivers/")
                    self.launch_temporary_firefox()
                if not os.path.exists("/tmp/UI7/webdrivers/geckodriver.log"):
                    os.mknod("/tmp/UI7/webdrivers/geckodriver.log")
                if not os.path.exists("/tmp/UI7/webdrivers/geckodriver"):
                    if 'ubuntu' in platform.version().lower():
                        os.system('cp /SWIFT4.0/TESTS/python_SonicOS/common_lib/modules/UI7/webdrivers/ubuntu/geckodriver /tmp/UI7/webdrivers/geckodriver')
                    else:
                        os.system('cp /SWIFT4.0/TESTS/python_SonicOS/common_lib/modules/UI7/webdrivers/centos/geckodriver /tmp/UI7/webdrivers/geckodriver')
                    time.sleep(2)
                    os.chmod("/tmp/UI7/webdrivers/geckodriver", stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO) # mode:777
                logger.info("Initialing firefox...")
                if 'ubuntu' in platform.version().lower() and '3.12' in subprocess.getstatusoutput('python3 --version')[1]:
                    firefox_options = Options()
                    
                    firefox_options.set_preference("browser.download.folderList", 2)
                    firefox_options.set_preference("browser.download.dir", "/root/Downloads")
                    firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", 
                                                "application/x-tar,application/gzip,application/x-gzip,application/octet-stream,application/x-gtar,application/tar,application/x-tgz,text/csv,application/pdf")
                    firefox_options.set_preference("pdfjs.disabled", True)
                    firefox_options.set_preference("security.insecure_field_warning.contextual.enabled", False)
                    firefox_options.set_preference("devtools.console.stdout.content", True)
                    firefox_options.set_preference("acceptInsecureCerts", True)  # 重要：接受不安全的证书
                    
                    firefox_options.add_argument('--headless')
                    firefox_options.add_argument('--ignore-certificate-errors')
                    firefox_options.add_argument('--disable-dev-shm-usage')
                    firefox_options.add_argument('--disable-gpu')
                    firefox_options.add_argument('--no-sandbox')
                    firefox_options.add_argument('--disable-web-security')
                    firefox_options.add_argument('--allow-running-insecure-content')
                    
                    firefox_options.accept_insecure_certs = True
                    
                    logger.info("Creating Firefox Service...")
                    service = Service(
                        executable_path="/tmp/UI7/webdrivers/geckodriver",
                        log_path="/tmp/UI7/webdrivers/geckodriver.log"
                    )
                    
                    service.start_timeout = 30
                    
                    logger.info("Starting Firefox driver...")
                    self.browser = webdriver.Firefox(
                        service=service,
                        options=firefox_options
                    )
                    
                    self.browser.implicitly_wait(10)
                    self.browser.set_page_load_timeout(30)
                    logger.info(f"Browser started successfully. Current URL: {self.browser.current_url}")
                    logger.info(f"Browser title: {self.browser.title}")
                    logger.info(f"Browser session_id: {self.browser.session_id}")
                    break
                else:
                    firefox_options = webdriver.FirefoxOptions()
                    profile = webdriver.FirefoxProfile()
                    profile.set_preference("browser.download.folderList", 2)  # Use custom download directory
                    download_directory = '/root/Downloads'
                    profile.set_preference("browser.download.dir", download_directory)
                    profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                        "application/x-tar,application/gzip,application/x-gzip,application/octet-stream,application/x-gtar,application/tar,application/x-tgz,text/csv,application/pdf")  # MIME types
                    profile.set_preference("pdfjs.disabled", True)  # To disable the PDF viewer
                    firefox_options.add_argument('--headless')
                    caps = DesiredCapabilities.FIREFOX
                    caps["marionette"] = True
                    caps['acceptSslCerts'] = True
                    #binary = FirefoxBinary('/usr/lib/firefox/firefox')
                    #self.browser = webdriver.Firefox(executable_path=r""+webdriver_directory + "\geckodriver.exe")
                    self.browser = webdriver.Firefox(executable_path=r"/tmp/UI7/webdrivers/geckodriver", firefox_profile=profile, options=firefox_options, capabilities=caps, service_log_path="/tmp/UI7/webdrivers/geckodriver.log")
                    logger.info("Browser started successfully")
                    break
                # return self.browser
            except Exception as err:
                logger.info("Browser startup failed")
                logger.info("Print geckodriver log")
                out = os.popen('cat /tmp/UI7/webdrivers/geckodriver.log').read()
                logger.info(out)
                logger.error("Now Exception is \t: " + str(err))
                retries += 1
                if retries < max_retries:
                    logger.info(f"Retrying... Attempt {retries}")
                    time.sleep(10)  
                    continue
                else:
                    logger.error("Failed to start browser after retries")
            
    def get_browser_2(self,browser_type = 'firefox'):
        try:
            logger.debug2("Starting Browser")
            if browser_type == 'firefox':
                if not os.path.exists("/tmp/UI7/webdrivers/"):
                    os.makedirs("/tmp/UI7/webdrivers/")
                    self.launch_temporary_firefox()
                if not os.path.exists("/tmp/UI7/webdrivers/geckodriver.log"):
                    os.mknod("/tmp/UI7/webdrivers/geckodriver.log")
                if not os.path.exists("/tmp/UI7/webdrivers/geckodriver"):     
                    os.system('cp /SWIFT4.0/TESTS/python_SonicOS/common_lib/modules/UI7/webdrivers/centos/geckodriver /tmp/UI7/webdrivers/geckodriver')
                    time.sleep(2)
                    os.chmod("/tmp/UI7/webdrivers/geckodriver", stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO) # mode:777
                logger.info("Initialing firefox...")
                logger.info('config firefox options....')
                firefox_options = webdriver.FirefoxOptions() 
                firefox_options.add_argument('--headless')
                profile = webdriver.FirefoxProfile()
                profile.accept_untrusted_certs = True
                profile.assume_untrusted_cert_issuer = True
                logger.info('config capabilities')
                caps = DesiredCapabilities.FIREFOX.copy()
                caps["marionette"] = True
                caps['acceptSslCerts'] = True
                caps['acceptInsecureCerts'] = True
                logger.info('start firefox')
                self.browser = webdriver.Firefox(executable_path=r"/tmp/UI7/webdrivers/geckodriver", options=firefox_options, capabilities=caps, firefox_profile=profile,service_log_path="/tmp/UI7/webdrivers/geckodriver.log")
            elif browser_type == 'chrome':
                logger.info('pkill chrome')
                os.system("pkill chrome")
                webdriver_path = '/SWIFT4.0/TESTS/python_SonicOS/common_lib/tools/webdriver/chromedriver'
                new_path = "/tmp/UI7/webdrivers/chromedriver"
                
                if not os.path.exists(new_path):
                    os.makedirs(os.path.dirname(new_path), exist_ok=True)
                    os.system(f'cp {webdriver_path} {new_path}')
                    time.sleep(2)
                    os.chmod(new_path, 0o777)
                else:
                    os.chmod(new_path, 0o777)

                logger.info('config chrome options...')
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument('ignore-certificate-errors')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--headless')
                logger.info('start chrome')
                self.browser = webdriver.Chrome(new_path,options=chrome_options)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            print("Browser startup failed")

    def launch_temporary_firefox(self, timeout=10):
        #try:
        logger.info("Launch Temporary Firefox")
        p = subprocess.Popen('firefox', stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
        t_beginning = time.time()
        seconds_passed = 0
        while True:  
            if p.poll() is not None:  
                break  
            seconds_passed = time.time() - t_beginning  
            if seconds_passed > timeout:  
                p.terminate()  
            time.sleep(0.1)  
        #return p.stdout.read()
            #os.system('firefox')
        #except Exception as err:
        #    logger.error("Exception \t: " + str(err))
        #    Assertion.fail("Launching Temporary Firefox Failed")

    # go to a url
    def go_to_url(self, url):
        try:
            logger.info("Opening URL on Browser :" + url)
            self.browser.get(url)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("URL Access failed")
    
    def scroll_mouse(self, pixcel):
        try:
            actions = ActionChains(self.browser)
            actions.move_by_offset(0, pixcel)
            actions.perform()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Scrolling mouse failed")
     

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
            Assertion.fail("Invalid selenium selector")

    # waits for the element visibility until given period of time.
    def wait_for_element_to_be_visible(self, attrib, attrib_val, wait_time=180):
        try:
            logger.debug2("Waiting for the element to be visible")
            selector = self.get_selenium_selector(attrib)
            logger.debug2("Selenium selector attribute \t: [" + attrib + "]")
            logger.debug2("Selenium selector value \t: [" + attrib_val + "]")
            return WebDriverWait(self.browser, wait_time).until(
                EC.visibility_of_element_located((selector, attrib_val)))
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Expected Condition : Element not visible")

    def wait_for_element_to_be_clickable(self, attrib, attrib_val, wait_time=180):
        try:
            logger.debug2("Waiting for the element to be clickable")
            selector = self.get_selenium_selector(attrib)
            logger.debug2("Selenium selector attribute \t: [" + attrib + "]")
            logger.debug2("Selenium selector value \t: [" + attrib_val + "]")
            return WebDriverWait(self.browser, wait_time).until(
                EC.element_to_be_clickable((selector, attrib_val)))
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Expected Condition : Element not clickable")

    # return an html element object.
    def get_element(self, attrib, attrib_val, visibility=True):
        try:
            logger.debug2("Getting element")
            if visibility:
                self.wait_for_element_to_be_visible(attrib, attrib_val)
            selector = self.get_selenium_selector(attrib)
            obj = self.browser.find_element(selector, attrib_val)
            return obj
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Element : Unable to get element")
    
    def get_span_element(self,attrib,attrib_val):
        element = self.get_element(attrib, attrib_val)
        element_text = element.text
        print("Element text:", element_text)
        return element_text

    # return an html element object.
    def get_invisible_element(self, attrib, attrib_val):
        try:
            logger.debug2("Getting invisible element")
            selector = self.get_selenium_selector(attrib)
            logger.debug2("Selenium selector value \t: [" + attrib_val + "]")
            obj = self.browser.find_element(selector, attrib_val)
            return obj
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Element : Unable to get invisible element")
            
    def get_invisible_elements(self, attrib, attrib_val):
        try:
            logger.debug2("Getting all matching elements")
            selector = self.get_selenium_selector(attrib)
            obj = self.browser.find_elements(selector, attrib_val)
            return obj
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Elements : Unable to get matching elements")

    # return an html element object.
    def get_elements(self, attrib, attrib_val):
        try:
            logger.debug2("Getting all matching elements")
            self.wait_for_element_to_be_visible(attrib, attrib_val)
            selector = self.get_selenium_selector(attrib)
            obj = self.browser.find_elements(selector, attrib_val)
            return obj
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Elements : Unable to get matching elements")

    # return any given html attribute value
    def get_attribute_value(self, attrib_to_identify, attrib_val, attrib_to_get_val, visibility=True):
        try:
            logger.debug2("Getting attribute value for \t: " + str(attrib_to_get_val))
            if visibility:
                self.wait_for_element_to_be_visible(attrib_to_identify, attrib_val)
            selector = self.get_selenium_selector(attrib_to_identify)
            obj = self.browser.find_element(selector, attrib_val)
            return obj.get_attribute(attrib_to_get_val)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Element : Unable to get attribute value of the element")

    # FUNCTIONALITY     : It clears a checkbox or a radio button
    # INPUT             : attrib : Attribute can be name,id,class,xpath,css,link_text,partial_link_text,tag_name
    #                     attrib_val : Attribute value
    #                     field_val : Value that has to be set
    # RETURNS           : Clears the field
    def clear_element(self, attrib, attrib_val):
        try:
            logger.debug2("Clearing Element")
            self.wait_for_element_to_be_visible(attrib, attrib_val)
            selector = self.get_selenium_selector(attrib)
            obj = self.browser.find_element(selector, attrib_val)
            if self.is_element_selected:
                logger.debug2("Element is selected, clicking to deselect")
                obj.click()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Action - Unable clear element")


    # FUNCTIONALITY     : It clears text field
    # INPUT             : attrib : Attribute can be name,id,class,xpath,css,link_text,partial_link_text,tag_name
    #                     attrib_val : Attribute value
    #                     field_val : Value that has to be set
    # RETURNS           : Clears the field
    def clear_text_field(self, attrib, attrib_val):
        try:
            logger.debug2("Clearing text field")
            self.wait_for_element_to_be_visible(attrib, attrib_val)
            selector = self.get_selenium_selector(attrib)
            obj = self.browser.find_element(selector, attrib_val)
            if self.is_element_selected:
                obj.send_keys(Keys.CONTROL, "a")
                obj.send_keys(Keys.BACKSPACE)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Action - Unable to clear test field")

    def clear_text_field_1(self, locator):
        try:
            element = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, locator)))
            element.click()
            element.send_keys(Keys.CONTROL, "a")
            element.send_keys(Keys.DELETE)
            logger.info(f"Cleared field: {locator}")
        except Exception as err:
            logger.error(f"Failed to clear field {locator}: {err}")
            Assertion.fail(f"Clearing text field failed for {locator}")

    # FUNCTIONALITY     : Setting a text field
    # INPUT             : attrib : Attribute can be name,id,class,xpath,css,link_text,partial_link_text,tag_name
    #                     attrib_val : Attribute value
    #                     field_val : Value that has to be set
    # RETURNS           : Sets the text field
    def set_text_field(self, attrib, attrib_val, field_val):
        try:
            logger.debug2("Setting text field with value \t: "+ str(field_val))
            self.wait_for_element_to_be_visible(attrib, attrib_val)
            self.click_element(attrib, attrib_val)
            self.clear_text_field(attrib,attrib_val)
            selector = self.get_selenium_selector(attrib)
            obj = self.browser.find_element(selector, attrib_val)
            for key in field_val:
                obj.send_keys(key)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Action - Unable to set text field")
    
    def set_text_field_2(self,  field_val):
        try:
            logger.debug2("Setting text field with value \t: "+ str(field_val))
            self.wait_for_element_to_be_visible(attrib, attrib_val)
            self.click_element(attrib, attrib_val)
            self.clear_text_field(attrib,attrib_val)
            selector = self.get_selenium_selector(attrib)
            obj = self.browser.find_element(selector, attrib_val)
            for key in field_val:
                obj.send_keys(key)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Action - Unable to set text field")

    def set_input_text_field(self, attrib, attrib_val, field_val):
        try:
            logger.debug2("Setting text field with value \t: " + str(field_val))
            selector = self.get_selenium_selector(attrib)
            obj = self.browser.find_element(selector, attrib_val)
            obj.click()
            obj.clear()
            # Enter the string character by character
            for char in str(field_val):
                ActionChains(self.browser).move_to_element(obj).send_keys(char).perform()
                time.sleep(0.1)
            print(obj.get_attribute('value'))
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Action - Unable to set text field")

    # FUNCTIONALITY     : Selects the required element
    # INPUT             : attrib : Attribute can be name,id,class,xpath,css,link_text,partial_link_text,tag_name
    #                     attrib_val : Attribute value
    #                     field_val : Value that has to be selected from the drop down
    # RETURNS           : Element is selected
    def select_element(self, attrib, attrib_val):
        try:
            logger.debug2("Selecting element")
            self.wait_for_element_to_be_clickable(attrib, attrib_val)
            selector = self.get_selenium_selector(attrib)
            obj = self.browser.find_element(selector, attrib_val)
            obj.send_keys(Keys.ENTER)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Action - Unable to select element")


    # FUNCTIONALITY     : Clicking a clickable element
    # INPUT             : attrib : Attribute can be name,id,class,xpath,css,link_text,partial_link_text,tag_name
    #                     attrib_val : Attribute value
    # RETURNS           : Clicks the required value
    def click_element(self, attrib, attrib_val):
        retries = 0
        while retries < 10:
            retries = retries + 1
            try:
                self.wait_for_element_to_be_clickable(attrib, attrib_val)
                obj = self.get_element(attrib, attrib_val)
                obj.click()
                return True
            except Exception as err:
                logger.debug2("Exception \t: " + str(err))
                logger.debug2("Click Exception : Retrying action")
                time.sleep(2)
                retries = retries + 1
                if retries < 10:
                    continue
                else:
                    logger.info("Exception \t: " + str(err))
                    Assertion.fail("Action - Unable to click element")

    # check whether a radio button or a checkbox is set or not.
    def is_element_set(self, attrib, attrib_val):
        try:
            logger.debug2("Checking if element is set")
            self.wait_for_element_to_be_visible(attrib, attrib_val)
            selector = self.get_selenium_selector(attrib)
            obj = self.browser.find_element(selector, attrib_val)
            if obj.is_selected():
                return True
            else:
                return False
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Element State : Unable to check if element is set")

    # to set radio button in UI7
    def set_radio_button(self, attrib, attrib_val):
        try:
            class_value = self.get_attribute_value(attrib, attrib_val, 'class')
            element_status = False
            if "sw-radio__fake-radio-button--checked" in class_value:
                element_status = True
            if element_status is not True:
                logger.debug("Action - setting radio button")
                self.click_element(attrib, attrib_val)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Action - Unable to set radio button")

    # FUNCTIONALITY     : Checks whether the given html element exist or not
    # INPUT             : attrib : Attribute can be name,id,class,xpath,css,link_text,partial_link_text,tag_name
    #                     attrib_val : Attribute value
    # RETURNS           : True if the element exists
    def does_element_exist(self, attrib, attrib_val):
        try:
            self.wait_for_element_to_be_visible(attrib, attrib_val)
            try:
                selector = self.get_selenium_selector(attrib)
                self.browser.find_element(selector, attrib_val)
            except NoSuchElementException:
                return False
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Element State : Unable to check if element exist")

    # check whether the given html element exist or not.
    def does_element_exist_now(self, attrib, attrib_val):
        time.sleep(2)
        try:
            try:
                selector = self.get_selenium_selector(attrib)
                self.browser.find_element(selector, attrib_val)
            except NoSuchElementException:
                return False
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            print("Element State : Unable to check for element existance")

    # check whether the element is enabled
    def is_element_enabled(self, attrib, attrib_val):
        try:
            logger.debug2("Checking if element is enabled")
            self.wait_for_element_to_be_visible(attrib, attrib_val)
            selector = self.get_selenium_selector(attrib)
            obj = self.browser.find_element(selector, attrib_val)
            if obj.is_enabled():
                return True
            else:
                return False
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Element State : Unable to check if element is enabled")

    # by JLian
    # check whether the invisible element is enabled
    def is_invisible_element_enabled(self, attrib, attrib_val):
        try:
            logger.debug2("Checking if element is enabled")
            selector = self.get_selenium_selector(attrib)
            obj = self.browser.find_element(selector, attrib_val)
            if obj.is_enabled():
                return True
            else:
                return False
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Element State : Unable to check if invisible element is enabled")

    # check whether the element is selected
    def is_element_selected(self, attrib, attrib_val):
        try:
            logger.debug2("Checking if element is selected")
            self.wait_for_element_to_be_visible(attrib, attrib_val)
            selector = self.get_selenium_selector(attrib)
            obj = self.browser.find_element(selector, attrib_val)
            if obj.is_selected():
                return True
            else:
                return False
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Element State : Unable to check if element is selected")

    # check whether the element is displayed
    def is_element_displayed(self, attrib, attrib_val):
        try:
            logger.debug2("Checking if element is displayed")
            self.wait_for_element_to_be_visible(attrib, attrib_val)
            selector = self.get_selenium_selector(attrib)
            obj = self.browser.find_element(selector, attrib_val)
            if obj.is_displayed():
                logger.debug2("Element is displayed")
                return True
            else:
                logger.debug2("Element is not displayed")
                return False
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Element State : Unable to check if element is visible")

    # waits for the element loading until given period of time.
    def wait_for_element_to_load(self, attrib, attrib_val, wait_time=180):
        try:
            logger.debug2("Waiting for element to load")
            selector = self.get_selenium_selector(attrib)
            logger.debug2("Selenium selector value \t: [" + attrib_val + "]")
            return WebDriverWait(self.browser, wait_time).until(
                EC.presence_of_element_located((selector, attrib_val)))
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Element State : Unable to check if element is loaded")

    # Wait for the text to appear for a fixed time
    def wait_for_text(self, text, wait_time=60):
        logger.debug2("Waiting for text \t: " + str(text))
        i = 0
        try:
            while i <= wait_time and not self.does_page_have_text(text):
                # Sleep while waiting for text to appear
                time.sleep(1)
                logger.debug2('Timeout: ' + str(i) + ' seconds elapsed waiting for "' + text + '"')
                i += 1
            assert i < wait_time, 'ERR: ' + str(wait_time) + ' seconds elapsed waiting for "' + text + '" to appear'
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Page State : Unable to wait for text")

    # check whether the given string is present in web pag ot not.
    def does_page_have_text(self, text_to_search):
        logger.debug2("Checking if {} page is loaded.".format(self.browser.current_url))
        # page_state = self.browser.execute_script('return document.readyState;')
        page_state = None
        for attempt in range(5):
            try:
                i = 0
                while page_state != 'complete' and i < 10:
                    page_state = self.browser.execute_script('return document.readyState;')
                    logger.debug2("page state is :" + page_state + "...")
                    i += 1
            except JavascriptException:
                logger.info("Caught JavascriptException exception. Retrying to get page load status...")
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

    # get the current browser url
    def get_current_browser_url(self):
        return self.browser.current_url

    # it maximizes the current web browser window
    def maximize_window(self):
        self.browser.maximize_window()

    # it refreshes the browser.
    def refresh_browser(self):
        self.browser.refresh()

    # it allows to click an element using javascript.
    def click_element_using_js(self, attrib_val):
        self.browser.execute_script(attrib_val)

    # used to kill any running {browser}.exe
    def kill_browser_sessions(self):
        if self.browser_name is "chrome":
            if self.kill_process('chrome.exe'):
                logger.info('Killing chrome.exe forcefully')
        if self.browser_name is "firefox":
            logger.info('Killing Firefox.exe forcefully')
            self.kill_process('firefox.exe')

    # delete all browsing history of the browser
    def delete_browser_history(self):
        if self.browser_name is "iexplorer":
            cmd = 'RunDll32.exe InetCpl.cpl,ClearMyTracksByProcess 4351 2>&1'
            logger.info('Deleting all history ofbrowser')
            result = os.system(cmd)
        elif self.browser_name is "chrome":
            # The clear history button is not working from chrome 71.x , replaced with default driver function
            self.browser.delete_all_cookies()
            # self.go_to_url('chrome://settings/clearBrowserData')
            # time.sleep(3)
            # self.click_element('css', '* /deep/ #clearBrowsingDataConfirm')
        else:
            logger.info("Invalid Browser type")
            return False

    # open a link and verify new page gets opened in new tab
    def click_link_and_check_page_opens_in_new_tab(self, attrib, attrib_val, new_url_text):
        self.click_element(attrib, attrib_val)
        handle = self.browser.window_handles
        self.browser.switch_to.window(handle[1])
        opened_url = self.browser.current_url
        self.browser.close()
        self.browser.switch_to.window(handle[0])
        if new_url_text in opened_url:
            return True
        else:
            return False

    # open a link and verify new page gets opened in same tab
    def click_link_and_check_page_opens_in_same_tab(self, attrib, attrib_val, new_url_text):
        opened_url1 = self.get_current_browser_url()
        self.click_element(attrib, attrib_val)
        # time.sleep(4)
        opened_url2 = self.get_current_browser_url()
        while opened_url1 == opened_url2:
            logger.info("waiting for link page to open ...")
            time.sleep(1)
            opened_url2 = self.get_current_browser_url()

        if new_url_text in opened_url2:
            return True
        else:
            return False

    # it retrieves entire html page source and returns the same
    def get_page_source(self):
        return self.browser.page_source

    # switches from one window to another
    def switch_window(self):
        for handle in self.browser.window_handles:
            self.browser.switch_to.window(handle)

    # Get browser handles
    def get_browser_all_handles(self):
        all_handles = self.browser.window_handles
        logger.info(all_handles)
        return all_handles

    # closes browser.
    def close_browser(self):
        self.browser.close()

    def kill_process(self, process_name):
        try:
            # Checks whether process is running or not
            result = self.is_process_running(process_name)
            if result:
                killed = os.system('taskkill /F /IM ' + process_name)
                self.wait_for_process_to_stop(process_name)
                assert not self.is_process_running(
                    process_name), 'ERR: Process: ' + process_name + 'is not killed successfully'
                logger.info('Process: ' + process_name + 'is killed successfully')
                return True
            else:
                return True
        except Exception as e:
            logger.info("ERR: Exception Occurred")
            logger.info(e)

    def get_select_list_values(self, attrib, attrib_val):
        self.wait_for_element_to_be_visible(attrib, attrib_val)
        self.switch_to_setting_frame()
        selector = self.get_selenium_selector(attrib)
        obj = self.browser.find_element(selector, attrib_val)
        obj1 = Select(obj)
        all_values = [values.get_attribute('value') for values in obj1.options]
        return all_values

    def if_value_exists_in_list(self, values, text):
        for value in values:
            if value == text:
                return True
        return False

    def quit(self):
        return self.browser.quit()

    # Kill process in Windows
    def kill_process(self, process_name):
        try:
            # Checks whether process is running or not
            result = self.is_process_running(process_name)
            if result:
                killed = subprocess.check_output('taskkill /F /IM ' + process_name, shell=True)
                self.wait_for_process_to_stop(process_name)
                assert not self.is_process_running(process_name), 'ERR: Process: ' + process_name + ' termination failed'
                logger.debug2('Process: ' + process_name + ' has been terminated successfully')
            else:
                logger.debug2('Process: ' + process_name + ' not running')
        except Exception as e:
            logger.error("ERR: Exception Occurred")
            logger.error(e)

    # Checks whether process is running or not
    def is_process_running(self, process_name):
        try:
            cmd = 'tasklist | findstr ' + process_name
            output = subprocess.check_output(cmd, shell=True)
            # Return True or False
            if output is not '':
                return True
        except subprocess.CalledProcessError as e:
            return False

    # Wait for a process to stop
    def wait_for_process_to_stop(self, process_name, wait_time=10):
        i = 0
        try:
            while i <= wait_time and self.is_process_running(process_name):
                # Sleep while waiting for process to stop
                time.sleep(1)
                logger.info('Timeout: ' + str(i) + ' seconds elapsed waiting for "' + process_name + '" to stop.')
                i += 1
            assert i < wait_time, 'ERR: ' + str(
                wait_time) + ' seconds elapsed waiting for "' + process_name + '" to stop'
        except Exception as e:
            logger.info("ERR: Exception Occurred")
            logger.info(e)
            raise

    def get_table_rows(self, attrib, attrib_val):
        time.sleep(1)
        self.wait_for_element_to_be_visible(attrib, attrib_val)
        obj = None
        rows = None
        selector = self.get_selenium_selector(attrib)
        obj = self.browser.find_element(selector, attrib_val)
        rows = obj.find_elements(By.TAG_NAME, "tr")
        return rows

    # Wait for the text to appear for a fixed time
    def wait_for_upgrade(self, text, task, wait_time=60):
        i = 0
        try:
            while i <= wait_time and not self.does_page_have_text(text):
                # Sleep 5seconds while waiting for text to appear
                time.sleep(5)
                i += 1
            assert i < wait_time, 'ERR: ' + str(wait_time) + ' seconds elapsed waiting for "' + text + '" to appear'
            logger.info("Time taken for " + task + " : " + str(i * 5) + " seconds...")
        except Exception as e:
            logger.info("ERR: Exception Occurred")
            logger.info(e)
            raise

    def does_relative_element_exist(self, element, attrib, attrib_val):
        try:
            selector = self.get_selenium_selector(attrib)
            element.find_element(selector, attrib_val)
        except NoSuchElementException:
            return False
        return True

    def click_relative_element(self, element, attrib, attrib_val):
        retries = 0
        self.wait_for_element_to_be_clickable(attrib, attrib_val)
        while retries < 5:
            retries = retries + 1
            try:
                selector = self.get_selenium_selector(attrib)
                obj = element.find_element(selector, attrib_val)
                obj.click()
            except Exception as e:
                logger.info("Click Exception : Retrying action")
                time.sleep(1)
                retries = retries + 1
                if retries < 5:
                    continue
                else:
                    logger.info("Click Exception : " + str(e))
                    return False
            return True
    
    def get_relative_element(self, element, attrib, attrib_val):
        selector = self.get_selenium_selector(attrib)
        obj = element.find_element(selector, attrib_val)
        return obj

    def wait_for_element_to_be_invisible(self, attrib, attrib_val, wait_time=180):
        selector = self.get_selenium_selector(attrib)
        element_status = EC.invisibility_of_element_located((selector, attrib_val))
        WebDriverWait(self.browser, wait_time).until(element_status)

    def is_element_displayed_now(self, attrib, attrib_val):
        # self.wait_for_element_to_be_visible(attrib, attrib_val, 2)
        selector = self.get_selenium_selector(attrib)
        obj = self.browser.find_element(selector, attrib_val)

        if obj.is_displayed():
            return True
        else:
            return False

    def wait_for_animation(self, selector):
        is_animation_in_progress = self.is_element_animated(selector)
        while is_animation_in_progress is True:
            time.sleep(1)
            is_animation_in_progress = self.is_element_animated(selector)

    def is_element_animated(self, selector):
        return self._driver.execute_script("return jQuery('" + selector + "').is(':animated');")

    def switchToWindow(self, title):
        try:
            logger.debug2("Switching to Window \t: " + title)
            handles = self.browser.window_handles
            size = len(handles)
            for x in range(size):
                self.browser.switch_to.window(handles[x])
                aTitle = self.browser.title
                if (aTitle == title):
                    break
                else:
                    continue

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Page State : Unable to switch window")

    def switchToDefaultWindow(self):
        try:
            handles = self.browser.window_handles
            self.browser.switch_to.window(handles[0])
        except Exception as e:
            logger.info("Window Switching failed.: " + str(e))
            raise e

    def switchToNewWindow(self):
        try:
            handles = self.browser.window_handles
            new_window_handle = handles[-1]
            self.browser.switch_to.window(new_window_handle)
            logger.info("switch succesfull")
        except Exception as e:
            logger.info("Window Switching failed.: " + str(e))
            raise e

    def bookmark_ssh_telnet_login(self, username, password):
        logger.info("logging into ssh telnet")
        try:
            action = ActionChains(self.browser)
            webdriver.ActionChains(self.browser).send_keys(username, Keys.ENTER).perform()
            time.sleep(5)
            logger.info("Username")
            webdriver.ActionChains(self.browser).send_keys(password, Keys.ENTER).perform()
            logger.info("password")
        except Exception as e:
            logger.info("Login failed.: " + str(e))
            raise e

    def click_button_using_action_chains(self, xpath_value):
        try:
            element = self.browser.find_element(By.XPATH, xpath_value)
            action = ActionChains(self.browser)
            action.click(element).perform()
        except Exception as e:
            logger.info("Button click failed.: " + str(e))
            raise e

    def get_browser_screen_mode(self):
        try:
            is_full_screen = self.browser.execute_script(
                "return window.innerHeight == screen.height && window.innerWidth == screen.width;")
            if is_full_screen:
                return "Full Screen Mode"
            else:
                return "Non Full Screen Mode"
        except Exception as e:
            logger.info("Getting Screen mode failed.: " + str(e))
            raise e

    def move_to_the_element(self, attrib, attrib_val, visible=True):
        logger.info("Moving to the element")
        if visible:
            element = self.get_element(attrib, attrib_val)
            ActionChains(self.browser).move_to_element(element).perform()
            return element
        else:
            element = self.get_invisible_element(attrib, attrib_val)
            ActionChains(self.browser).move_to_element(element).perform()
            return element

    #UI7 specify, looks for toggle value before changing the state
    def toggle_button(self, attrib, attrib_val, enabled):
        element_status = True
        if attrib_val.isdigit() != True:
            class_value = self.get_attribute_value(attrib, attrib_val, 'class')
            if "sw-toggle--off" in class_value:
                element_status = False
            if element_status != enabled:
                logger.debug("Action - Toggling Element")
                self.click_element(attrib, attrib_val)
        else:
            attrib_val = int(attrib_val)
            selector = self.get_selenium_selector(attrib)
            obj = self.browser.find_elements(selector, 'sw-toggle')[attrib_val]
            class_value = obj.get_attribute("outerHTML")
            if "sw-toggle--off" in class_value:
                element_status = False
            if element_status != enabled:
                logger.debug("Action - Toggling Element")
                self.browser.find_elements(selector, 'sw-toggle')[attrib_val].click()

    # Click on grid view
    def click_on_grid_view(self, attrib, attrib_value):
        self.click_element(attrib, attrib_value)

    # To set checkbox button in UI7
    def checkbox_button(self, attrib, attrib_val, enable):
        try:
            class_value = self.get_attribute_value(attrib, attrib_val, 'class', visibility=False)
            element_status = True
            if "sw-checkbox__box__mark--no" in class_value:
                element_status = False
            if element_status != enable:
                logger.debug("Action - Setting Checkbox Button")
                self.click_invisible_element(attrib, attrib_val)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Action - Unable to set Checkbox button")    
    
    # FUNCTIONALITY     : Clicking a invisiible element
    # INPUT             : attrib : Attribute can be name,id,class,xpath,css,link_text,partial_link_text,tag_name
    #                     attrib_val : Attribute value
    # RETURNS           : Clicks the required value
    def click_invisible_element(self, attrib, attrib_val):
        logger.debug2("Clicking on  \t: " + str(attrib_val))
        retries = 0
        while retries < 10:
            retries = retries + 1
            try:
                obj = self.get_invisible_element(attrib, attrib_val)
                obj.click()
                return True
            except Exception as err:
                logger.debug2("Exception \t: " + str(err))
                logger.debug2("Click Exception : Retrying action")
                time.sleep(2)
                retries = retries + 1
                if retries < 10:
                    continue
                else:
                    logger.info("Exception \t: " + str(err))
                    Assertion.fail("Action - Unable to click element")

    # FUNCTIONALITY     : Clicks on confirm alert button
    # INPUT             : None
    # RETURNS           : None
    def accept_alert(self):
        try:
            logger.debug("Action - Clicking on Confirm button")
            self.click_element('xpath', '//div[contains(@class, "sw-confirm-modal__footer")]/div/div/button'
                                                   '[text()="Submit" or text()="OK" or text()="Ok" or text()="Confirm"]')
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            print("Failed to accept the alert")
    def accept_ssh_alert(self):
        WebDriverWait(self.browser, 60).until(EC.alert_is_present())
        self.browser.switch_to.alert.accept()

    def is_ssh_alert_available(self):
        try:
            WebDriverWait(self.browser, 20).until(EC.alert_is_present())
            self.browser.switch_to.alert.accept()
            return 'Alert Available'
        except Exception as err:
            return 'Alert Not Available'
            
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

                self.move_to_the_element('xpath',
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
                self.move_to_the_element('xpath',
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
            self.wait_for_page_data_to_be_rendered()
            logger.debug2("Clicked on edit button for the entry:" + row_identifier)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            print("Unable to click edit icon")

    # Added by Celia
    # FUNCTIONALITY     : Clicks on edit icon after hovering on the desired entry
    # INPUT             : the name of row entry(row identifier)
    # RETURNS           : None
    def click_on_edit_element_after_hovering_new(self, row_identifier, modal=False, strict=True):
        try:
            text = f"text()='{row_identifier}'" if strict else f"contains(text(), '{row_identifier}')"
            logger.debug2(text)
            row_identifier_xpath_list = [
                f"//td/div[{text}]",
                f"//td/div/div[{text}]",
                f"//div[{text} and contains(@class, 'sw-table-row__cell__wrapper')]",
                f"//div[{text} and contains(@class, 'sw-table-row')]",
                f"//div[contains(@class, 'sw-table-row')]/following::*[{text}]"
            ]
            pencil_icon = "/following::*[contains(@class, 'sw-table-row-float-actions') and not (contains(@class, 'sw-table-row-float-actions--invisible'))]/descendant::*[contains(@class, 'icon-pencil')]"
            modal_xpath = "//div[contains(@class, 'sw-modal__main-body')]//following::"
            if not modal:
                logger.debug2('|'.join(row_identifier_xpath_list))
                self.move_to_the_element('xpath','|'.join(row_identifier_xpath_list))
                pencil_xpath = '|'.join((r_xpath + pencil_icon for r_xpath in row_identifier_xpath_list))
                logger.debug2(pencil_xpath)
                self.click_element('xpath', pencil_xpath)
            else:
                modal_row_identifier_list = [modal_xpath + r_xpath for r_xpath in row_identifier_xpath_list]
                self.move_to_the_element('xpath','|'.join(modal_row_identifier_list))
                pencil_xpath = '|'.join((r_xpath + pencil_icon for r_xpath in modal_row_identifier_list))
                self.click_element('xpath', pencil_xpath)
            self.wait_for_page_data_to_be_rendered()
            logger.debug2("Clicked on edit button for the entry:" + row_identifier)
        except Exception as err:
            logger.error(f"Exception \t: {err}")
            print("Unable to click edit icon")

    # FUNCTIONALITY     : Waits for all buffer to disappear
    # INPUT             : None
    # RETURNS           : None
    def wait_for_page_data_to_be_rendered(self):
        logger.info("Waiting for page data to be rendered completely!")
        self.wait_for_element_to_be_invisible('xpath', '//div[contains(@class, "sw-blocking-progress")]')

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
            element = self.move_to_the_element('xpath',  "//span[contains(text(), '"+select_identifier+"')]"
                                                                    "/following::div[contains(@class, 'sw-dropdown')]/"
                                                                    "span[text()='"+ select_value+"']", False)
            element.click()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Action - Unable to select from drop down list")

    # FUNCTIONALITY     : Configures text field
    # INPUT             : UI Label of the text field
    # RETURNS           : None
    def configure_text_field(self, text_box_label, text_value1,text_value2 =None):
        try:
            logger.debug("Configure - Text field "+text_box_label+" with value  \t: "+ str(text_value1))
            self.set_text_field('xpath', '//div[contains(@class,"label") and text()="'+text_box_label+'"]/'
                                                    'following::input[@type="text" or @type="password"]|'
                                                    '//div[contains(@class, "label")]/span[text()="'+text_box_label+'"]/'
                                                    'following::input[@type="text" or @type="password"]|'
                                                    '//div[contains(@class, "label")]/span[contains(text(), "'+text_box_label+'")]/'
                                                    'following::input[@type="text" or @type="password"]|'
                                                    '//div[contains(@class, "label") and contains(text(),"'+text_box_label+'")]/'
                                                    'following::input[@type="text" or @type="password"]', text_value1)
            if text_value2:
                self.send
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Configure - Unable to set text field")

    def verify_error_message_alert(self, errorMsg):
        try:
            self.compare_error_message(errorMsg)
            self.accept_alert()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Accept Error Message failed")

    # FUNCTIONALITY     : Gets the error message on the UI and compares it with the error message sent
    # INPUT             : Expected error message
    # RETURNS           : None
    def compare_error_message(self, errorMsg):
        try:
            errorMessage = self.get_element('class', "sw-status-info__text__message")
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

    # Added by Celia
    def compare_message_new(self, targetMsg, attrib='', attrib_val=''):
        for _ in range(3):
            try:
                if attrib and attrib_val:
                    message = self.get_element(attrib, attrib_val)
                else:
                    message = self.get_element('class', "sw-status-info__text__message")
                if message:
                    msg = str(message.text)
                    logger.debug2(f"Actual Error text\t:{msg}")
                    logger.debug2("Expected Error text\t: " + str(targetMsg))
                    if isinstance(targetMsg, list) and msg.lstrip().rstrip() in targetMsg:
                        logger.debug(msg)
                        return True
                    if isinstance(targetMsg, str) and msg.lower().lstrip().rstrip() == targetMsg.lower().lstrip().rstrip():
                        logger.debug(msg)
                        return True
                    logger.error(f"Message mismatch\t:{msg}")
                raise NoSuchElementException
            except Exception as err:
                logger.error(f"Exception \t: {err}")
                if 'the element is no longer attached to the DOM' in str(err):
                    continue
                Assertion.fail("Message verification failed")

    # Added by Celia
    def verify_message_alert(self, targetMsg):
        try:
            self.compare_message_new(targetMsg)
            self.accept_alert()
        except Exception as err:
            logger.error(f"Exception \t: {err}")
            Assertion.fail("Accept Error Message failed")

    # Added by Celia ----- part3
    def compare_alert_message(self, targetMsg, attrib='', attrib_val=''):
        for _ in range(3):
            try:
                if attrib and attrib_val:
                    message = self.get_element(attrib, attrib_val)
                else:
                    message = self.get_element('class', "sw-status-info__text__message")
                if message:
                    msg = str(message.text)
                    logger.debug2(f"Actual text\t:{msg}")
                    logger.debug2(f"Expected text\t:{str(targetMsg)}")
                    if isinstance(targetMsg, list):
                        msg_list = [x.lower() for x in targetMsg]
                        if msg.lower().lstrip().rstrip() in msg_list:
                            logger.debug(msg)
                            return True
                    if isinstance(targetMsg, str) and msg.lower().lstrip().rstrip() == targetMsg.lower().lstrip().rstrip():
                        logger.debug(msg)
                        return True
                    logger.error(f"Message mismatch\t:{msg}")
                    logger.error(f"Target Message\t:{str(targetMsg)}")
                raise NoSuchElementException
            except Exception as err:
                logger.error(f"Exception \t: {err}")
                if 'the element is no longer attached to the DOM' in str(err):
                    continue
                Assertion.fail("Message verification failed")

    def accept_alert_new(self):
        try:
            logger.debug("Action - Clicking on Confirm button")
            self.click_element('xpath', '//div[contains(@class, "sw-confirm-modal__footer")]/descendant::button'
                                                   '[text()="Submit" or text()="OK" or text()="Ok" or text()="Confirm"]')
        except Exception as err:
            logger.error(f"Exception \t: {err}")
            print("Failed to accept the alert")

    def verify_alert_message(self, targetMsg):
        try:
            self.compare_alert_message(targetMsg)
            self.accept_alert_new()
        except Exception as err:
            logger.error(f"Exception \t: {err}")
            Assertion.fail("Verify alert message failed")
    #  ----- part3

    def did_page_load_successfully(self):
        page_state = None
        for attempt in range(5):
            try:
                i = 0
                while page_state != 'complete' and i < 10:
                    page_state = self.browser.execute_script('return document.readyState;')
                    time.sleep(2)
                    return True
                    i += 1
            except JavascriptException:
                logger.info("Caught JavascriptException exception. Retrying to get page load status...")
                continue
            if attempt == 5:
                return False

    # Added by Celia
    # FUNCTIONALITY     : Scroll view to target element
    # INPUT             : Element Path Attribute and Attribute Value
    # RETURNS           : None
    def scroll_view_to_element(self, attrib, attrib_val):
        try:
            target = self.get_invisible_element(attrib=attrib, attrib_val=attrib_val)
            self.browser.execute_script("arguments[0].scrollIntoView();", target)
        except Exception as err:
            logger.error(f'Cannot scroll into element!! Exception \t: {err}')


    def get_specific_element_xpath(self, attrib_val_list):
        for attrib_val in attrib_val_list:
            try:
                logger.debug2("Getting element from_xpath_list")
                selector = self.get_selenium_selector('xpath')
                self.browser.find_element(selector, attrib_val)
                return attrib_val
            except Exception:
                logger.debug2('Cannot find this element')
        logger.error('Cannot find element from the path list !')
        return ''

    # add by JLian
    def set_radio_button_by_label(self, radio_button_lable):
        try:
            radio_button_xpath = f"//span[text()='{radio_button_lable}']/preceding-sibling::span[contains(@class,'sw-radio__fake-radio-button')]"
            class_value = self.get_attribute_value('xpath', radio_button_xpath, 'class')
            if "radio-button--checked" in class_value:
                logger.debug('radio button has already been checked')
                return True
            logger.debug("Action - setting radio button")
            self.click_element('xpath', radio_button_xpath)
            new_class_value = self.get_attribute_value('xpath', radio_button_xpath, 'class')
            if "radio-button--checked" in new_class_value:
                return True
            else:
                logger.warning(f'Failed to set radio button')
                return False
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Action - Unable to set radio button")

    # add by JLian
    def is_radio_button_checked(self, radio_button_label):
        try:
            logger.debug("Get -  Radio button value \t: " + str(radio_button_label))
            class_value = self.get_attribute_value('xpath',
                                                   f"//span[text()='{radio_button_label}']/preceding-sibling::span[contains(@class,'sw-radio__fake-radio-button')]",
                                                   'class')
            logger.info(f'radio button class value is:{class_value}')
            if 'radio-button--checked' in class_value:
                return True
            else:
                return False
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Unable to get radio button")

    # add by JLian
    def is_toggle_button_checked(self, toggle_button_label):
        try:
            logger.debug("Get -  Radio button value \t: " + str(toggle_button_label))

            class_value = self.get_attribute_value('xpath',
                                                   f'//div[text()="{toggle_button_label}"]/following::*[contains(@class,"sw-toggle")]',
                                                   'class')
            logger.info(f'toggle button class value is:{class_value}')
            if 'sw-toggle--off' not in class_value:
                return True
            else:
                return False
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Unable to get toggle button")

    # add by JLian
    def is_element_grey(self, attrib, attrib_val):
        try:
            logger.debug2("Checking if element is enabled")
            self.browser.implicitly_wait(5)
            selector = self.get_selenium_selector(attrib)
            radio_element = self.browser.find_element(selector, attrib_val)
            background_color = radio_element.value_of_css_property('background-color')
            logger.info(f'background_color is {background_color}')
            if background_color:
                match = re.match(r'rgb\((\d+), (\d+), (\d+)\)', background_color)
                if match:
                    r, g, b = map(int, match.groups())
                    is_grey = (abs(r - g) < 10 and abs(r - b) < 10 and abs(g - b) < 10)
                    is_not_black_or_white = (r > 10 and r < 245)
                    logger.info(f"Is grey: {is_grey}, Not black/white: {is_not_black_or_white}")
                    return is_grey and is_not_black_or_white
            return False
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Element State : Unable to check if element is grey")

    #  add by JLian
    def click_close_icon_by_window_title(self, window_title):
        close_window_xpath = f"//span[contains(text(),'{window_title}')]/following-sibling::span//span[contains(@class,'icon-close-thin')]"
        logger.info(f'close window xpth is:{close_window_xpath}')
        try:
            logger.debug("Action - Clicking Close")
            self.wait_for_page_data_to_be_rendered()
            self.wait_for_element_to_load('css', 'div.fw-app-main__content')
            obj = self.browser.find_element('xpath', close_window_xpath)
            location_dict = obj.location
            logger.info(f'location_dict is:{location_dict}')
            obj.click()
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            return False

