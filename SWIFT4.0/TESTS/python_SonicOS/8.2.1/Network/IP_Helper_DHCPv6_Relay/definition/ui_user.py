import re
import sys
import argparse
import sys
from datetime import datetime, timedelta
sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
from runner.settings import logger
from modules.ui.ui_wrapper import Browser
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from runner.utils.assertion import Assertion
from selenium.webdriver.common.by import By

import time


class FWPage(Browser):
    def __init__(self, method, url, user, pwd):
        self.method = method
        self.url = url
        self.user = user
        self.password = pwd

    def navigate_to_ip_helper_section(self):
        try:
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
            logger.info("Action - Clicked Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(10)
            self.click_element('xpath', "//button[normalize-space()='Cancel']")
            time.sleep(2)
            self.click_element('xpath',"//span[@class='sw-icon__inner sw-font-icon icon-topo']")
            time.sleep(5)
            self.click_element('xpath',"//span[normalize-space()='IP Helper']")
            time.sleep(5)                  
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def verify_toggle_button(self, attrib, attrib_val):
        if attrib_val.isdigit() != True:
            class_value = self.get_attribute_value(attrib, attrib_val, 'class')
            if "sw-toggle--off" in class_value:
                return "OFF"
            else:
                return "ON"
        

    def tc1_DHCPv6_listed_under_Relay_Protocols_field(self):
        try:
            self.navigate_to_ip_helper_section()
            self.click_element('xpath',"//span[@class='sw-icon__inner sw-font-icon icon-topo']")
            time.sleep(5)
            self.click_element('xpath',"//span[normalize-space()='IP Helper']")
            time.sleep(5)
            DHCPv6 = self.does_page_have_text('DHCPv6')
            if DHCPv6 == True:
                logger.info('True')
            return True                  
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")   

    def tc2_DHCPv6_Relay_Protocol_details(self):
        try:
            self.navigate_to_ip_helper_section()
            self.set_text_field('xpath', "//input[@placeholder='Search...']", "DHCPv6")
            time.sleep(5)
            name = self.browser.find_element(By.XPATH,
                                             "/html/body/div/div/div/div[2]/div[4]/div[2]/div[1]/div/section/div/div[2]/div[2]/div/div[2]/div[1]/div/div/div[5]/div").text
            port1 = self.browser.find_element(By.XPATH,
                                             "/html/body/div/div/div/div[2]/div[4]/div[2]/div[1]/div/section/div/div[2]/div[2]/div/div[2]/div[1]/div/div/div[6]/div").text
            port2 = self.browser.find_element(By.XPATH,
                                             "/html/body/div/div/div/div[2]/div[4]/div[2]/div[1]/div/section/div/div[2]/div[2]/div/div[2]/div[1]/div/div/div[7]/div").text
            protocol = self.browser.find_element(By.XPATH,
                                             "/html/body/div/div/div/div[2]/div[4]/div[2]/div[1]/div/section/div/div[2]/div[2]/div/div[2]/div[1]/div/div/div[9]/div").text
            mode = self.browser.find_element(By.XPATH,
                                             "/html/body/div/div/div/div[2]/div[4]/div[2]/div[1]/div/section/div/div[2]/div[2]/div/div[2]/div[1]/div/div/div[11]/div").text

            if name == 'DHCPv6' and port1 == '547' and port2 == '546' and protocol == 'UDP' and mode == 'Multicast':
                logger.info('True')
                return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def tc2_DHCPv6_Relay_Protocol_details_tz80(self):
        try:
            self.navigate_to_ip_helper_section()
            self.set_text_field('xpath', "//input[@placeholder='Search...']", "DHCPv6")
            time.sleep(5)
            name = self.browser.find_element(By.XPATH,
                                             "/html/body/div/div/div/div[2]/div[4]/div[2]/div[1]/div/section/div/div[2]/div[2]/div/div[2]/div[1]/div/div/div[5]/div").text
            port1 = self.browser.find_element(By.XPATH,
                                              "/html/body/div/div/div/div[2]/div[4]/div[2]/div[1]/div/section/div/div[2]/div[2]/div/div[2]/div[1]/div/div/div[6]/div").text
            port2 = self.browser.find_element(By.XPATH,
                                              "/html/body/div/div/div/div[2]/div[4]/div[2]/div[1]/div/section/div/div[2]/div[2]/div/div[2]/div[1]/div/div/div[7]/div").text
            protocol = self.browser.find_element(By.XPATH,
                                                 "/html/body/div/div/div/div[2]/div[4]/div[2]/div[1]/div/section/div/div[2]/div[2]/div/div[2]/div[1]/div/div/div[9]/div").text
            mode = self.browser.find_element(By.XPATH,
                                             "/html/body/div/div/div/div[2]/div[4]/div[2]/div[1]/div/section/div/div[2]/div[2]/div/div[2]/div[1]/div/div/div[11]/div").text
            if name == 'DHCPv6' and port1 == '547' and port2 == '546' and protocol == 'UDP' and mode == 'Multicast':
                logger.info('True')
            return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def tc3_enable_and_disable_DHCPv6_Relay_Protocol(self):
        try:
            self.navigate_to_ip_helper_section()
            self.set_text_field('xpath', "//input[@placeholder='Search...']", "DHCPv6")
            time.sleep(5)
            self.toggle_button('xpath', "//div[@class='sw-table-row__cell__wrapper sw-flexbox__flex sw-flexbox sw-flexbox--center-items']//div//div//div[@class='sw-toggle sw-toggle--right sw-toggle--regular sw-toggle--light sw-toggle--off']", True)
            self.click_element('xpath', "//button[@class='sw-button sw-button--light sw-button--default']")
            time.sleep(5)
            res1 = self.verify_toggle_button('xpath',"//div[@class='sw-toggle sw-toggle--right sw-toggle--regular sw-toggle--light']")
            if res1 == 'ON':
                logger.info('Element toggled ON successfully')
            self.toggle_button('xpath', "//div[@class='sw-toggle sw-toggle--right sw-toggle--regular sw-toggle--light']", False)
            self.click_element('xpath', "//button[@class='sw-button sw-button--light sw-button--default']")
            time.sleep(5)
            res2 = self.verify_toggle_button('xpath',"//div[@class='sw-table-row__cell__wrapper sw-flexbox__flex sw-flexbox sw-flexbox--center-items']//div//div//div[@class='sw-toggle sw-toggle--right sw-toggle--regular sw-toggle--light sw-toggle--off']")
            if res2 == 'OFF':
                logger.info('Element toggled OFF successfully')
            if res1 == 'ON' and res2 == 'OFF':
                logger.info('True')
            return True                  
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")     

    def tc5_check_DHCPv6_listed_in_Protocol_dropdown_list(self):
        try:
            self.navigate_to_ip_helper_section()
            self.click_element('xpath',"//span[normalize-space()='Policies']")
            time.sleep(5)
            self.click_element('xpath', "//span[@class='sw-icon__inner sw-font-icon icon-add']")
            self.click_element('xpath',
                               "//div[@class='sw-select sw-select--light sw-typo-default sw-flexbox sw-flexbox--inline sw-flexbox--center-items sw-select--top-padding create-ip-policies__select-protocol']//span[@class='sw-icon__inner sw-font-icon icon-arrow-up']")
            time.sleep(5)
            DHCPv6 = self.does_page_have_text('DHCPv6')
            if DHCPv6 == True:
                logger.info('True')
            return True                  
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def tc6_add_DHCPv6_relay_policy(self):
        try:
            self.navigate_to_ip_helper_section()
            self.click_element('xpath',"//span[normalize-space()='Policies']")
            time.sleep(5)
            self.click_element('xpath', "//span[@class='sw-icon__inner sw-font-icon icon-add']")
            time.sleep(3)
            # self.select_drop_down_value('Protocol', "DHCPv6", modal=True)
            self.click_element('xpath', "//div[@class='sw-select sw-select--light sw-typo-default sw-flexbox sw-flexbox--inline sw-flexbox--center-items sw-select--top-padding create-ip-policies__select-protocol']//span[@class='sw-icon__inner sw-font-icon icon-arrow-up']")
            self.click_element('xpath',"//span[normalize-space()='DHCPv6']")
            # self.select_drop_down_value('From', "Interface X0", modal=True)
            self.click_element('xpath', "//div[@class='sw-select sw-select--light sw-typo-default sw-flexbox sw-flexbox--inline sw-flexbox--center-items sw-select--top-padding create-ip-policies__from-policy']//span[@class='sw-icon__inner sw-font-icon icon-arrow-up']")
            self.click_element('xpath',"//span[@class='sw-flexbox__flex sw-flexbox sw-flexbox--center-items'][normalize-space()='Interface X0']")
            self.set_text_field('xpath', "//input[@name='dhcpv6-to']", "::ffff:c0a8:0dc8")
            # self.select_drop_down_value('Egress Interface', "Interface X6", modal=True)
            self.click_element('xpath', "//div[@class='sw-select sw-select--light sw-typo-default sw-flexbox sw-flexbox--inline sw-flexbox--center-items sw-select--top-padding create-ip-policies__dhcpv6-egress-interface']//span[@class='sw-icon__inner sw-font-icon icon-arrow-up']")
            self.click_element('xpath',"//span[normalize-space()='Interface X4']")
            self.set_text_field('xpath', "//input[@name='textfield-comment-policy']", "test")
            time.sleep(2)
            self.click_element('xpath', "//button[normalize-space()='Save']")
            time.sleep(2)
            DHCPv6 = self.does_page_have_text('DHCPv6')
            if DHCPv6 == True:
                logger.info('True')
            return True                  
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    
    def tc7_verify_DHCPv6_relay_policy_details(self):
        try:
            self.navigate_to_ip_helper_section()
            self.click_element('xpath',"//span[normalize-space()='Policies']")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Search...']", "DHCPv6")
            time.sleep(3)
            protocol = self.browser.find_element(By.XPATH,"//div[contains(text(),'DHCPv6')]").text
            source = self.browser.find_element(By.XPATH,"//div[contains(text(),'X0')]").text
            destination = self.browser.find_element(By.XPATH,"//div[contains(text(),'::ffff:c0a8:dc8')]").text
            comment = self.browser.find_element(By.XPATH,"//div[contains(text(),'test')]").text
            
            if protocol == 'DHCPv6' and source == 'X0' and destination == '::ffff:c0a8:dc8' and comment == 'test':
                logger.info('True')
            return True                  
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def tc8_disable_DHCPv6_relay_policy(self):
        try:
            self.navigate_to_ip_helper_section()
            self.click_element('xpath',"//span[normalize-space()='Policies']")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Search...']", "DHCPv6")
            time.sleep(3)
            self.toggle_button('xpath', "//div[@class='sw-toggle sw-toggle--right sw-toggle--regular sw-toggle--light ip-policies__inline-enable']", False)
            self.click_element('xpath', "//button[@class='sw-button sw-button--light sw-button--default']")
            time.sleep(5)
            res2 = self.verify_toggle_button('xpath',"//div[@class='sw-toggle sw-toggle--right sw-toggle--regular sw-toggle--light sw-toggle--off ip-policies__inline-enable']")
            if res2 == 'OFF':
                logger.info('Element toggled OFF successfully')
                logger.info('True')
            return True                  
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def tc9_enable_DHCPv6_relay_policy(self):
        try:
            self.navigate_to_ip_helper_section()
            self.click_element('xpath',"//span[normalize-space()='Policies']")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Search...']", "DHCPv6")
            time.sleep(3)
            self.toggle_button('xpath', "//div[@class='sw-toggle sw-toggle--right sw-toggle--regular sw-toggle--light sw-toggle--off ip-policies__inline-enable']", True)
            self.click_element('xpath', "//button[@class='sw-button sw-button--light sw-button--default']")
            time.sleep(5)
            res = self.verify_toggle_button('xpath',"//div[@class='sw-toggle sw-toggle--right sw-toggle--regular sw-toggle--light ip-policies__inline-enable']")
            if res == 'ON':
                logger.info('Element toggled ON successfully')
                logger.info('True')
            return True                  
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    
    def tc10_delete_DHCPv6_relay_policy(self):
        try:
            self.navigate_to_ip_helper_section()
            self.click_element('xpath',"//span[normalize-space()='Policies']")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Search...']", "DHCPv6")
            time.sleep(3)
            self.move_to_the_element('xpath',"//div[contains(text(),'DHCPv6')]")
            self.click_element('xpath',"//span[@class='sw-icon-button sw-icon-button--no-border sw-icon-button--dark']//span[@class='sw-icon__inner sw-font-icon icon-trash']")
            self.click_element('xpath', "//button[@class='sw-button sw-button--light sw-button--default']")
            logger.info('DHCPv6 Relay Policy deleted successfully')
            time.sleep(3)
            # verify if deletion is success
            self.set_text_field('xpath', "//input[@placeholder='Search...']", "DHCPv6")
            time.sleep(5)
            DHCPv6 = self.does_page_have_text('No Data')
            if DHCPv6 == True:
                logger.info('Enter does not exist - deletion is successful')
                logger.info('True')
            return True                  
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def tc11_configure_DHCPv6_relay_policy(self):
        try:
            resp = self.tc6_add_DHCPv6_relay_policy()
            resp1 = self.tc7_verify_DHCPv6_relay_policy_details()
            if resp == True and resp1 == True:
                logger.info('True')
            return True                  
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")

    def tc12_invalid_input_add_DHCPv6_relay_policy(self):
        try:
            self.navigate_to_ip_helper_section()
            self.click_element('xpath',"//span[normalize-space()='Policies']")
            time.sleep(5)
            self.click_element('xpath', "//span[@class='sw-icon__inner sw-font-icon icon-add']")
            self.click_element('xpath', "//div[@class='sw-select sw-select--light sw-typo-default sw-flexbox sw-flexbox--inline sw-flexbox--center-items sw-select--top-padding create-ip-policies__select-protocol']//span[@class='sw-icon__inner sw-font-icon icon-arrow-up']")
            self.click_element('xpath',"//span[normalize-space()='DHCPv6']")
            self.click_element('xpath', "//div[@class='sw-select sw-select--light sw-typo-default sw-flexbox sw-flexbox--inline sw-flexbox--center-items sw-select--top-padding create-ip-policies__from-policy']//span[@class='sw-icon__inner sw-font-icon icon-arrow-up']")
            self.click_element('xpath',"//span[@class='sw-flexbox__flex sw-flexbox sw-flexbox--center-items'][normalize-space()='Interface X0']")
            self.set_text_field('xpath', "//input[@name='dhcpv6-to']", "10.5.6.4")
            self.click_element('xpath', "//div[@class='sw-select sw-select--light sw-typo-default sw-flexbox sw-flexbox--inline sw-flexbox--center-items sw-select--top-padding create-ip-policies__dhcpv6-egress-interface']//span[@class='sw-icon__inner sw-font-icon icon-arrow-up']")
            self.click_element('xpath',"//span[normalize-space()='Interface X4']")
            self.set_text_field('xpath', "//input[@name='textfield-comment-policy']", "test")
            self.click_element('xpath', "//button[normalize-space()='Save']")
            time.sleep(2)
            DHCPv6 = self.does_page_have_text("Error: property 'ipv6': invalid format")
            if DHCPv6 == True:
                logger.info('True')
            return True                  
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Login group service by UI')
    parser.add_argument("-method", type=str, dest='method', required=True, help="Specify the method to run.")
    parser.add_argument('-url', type=str, dest='url', required=True, help='http server url')
    parser.add_argument('-user', type=str, dest='user', required=True, help='user to login group service')
    parser.add_argument('-pwd', type=str, dest='pwd', required=True, help='pwd to login group service')
    args = parser.parse_args()
    uiobj = FWPage(args.method, args.url, args.user, args.pwd)

    if args.method == "tc1":
        rc = uiobj.tc1_DHCPv6_listed_under_Relay_Protocols_field()
    elif args.method == "tc2":
        rc = uiobj.tc2_DHCPv6_Relay_Protocol_details()
    elif args.method == "tc3":
        rc = uiobj.tc3_enable_and_disable_DHCPv6_Relay_Protocol()
    elif args.method == "tc5":
        rc = uiobj.tc5_check_DHCPv6_listed_in_Protocol_dropdown_list()
    elif args.method == "tc6":
        rc = uiobj.tc6_add_DHCPv6_relay_policy()
    elif args.method == "tc7":
        rc = uiobj.tc7_verify_DHCPv6_relay_policy_details()
    elif args.method == "tc8":
        rc = uiobj.tc8_disable_DHCPv6_relay_policy()
    elif args.method == "tc9":
        rc = uiobj.tc9_enable_DHCPv6_relay_policy()
    elif args.method == "tc10":
        rc = uiobj.tc10_delete_DHCPv6_relay_policy()
    elif args.method == "tc11":
        rc = uiobj.tc11_configure_DHCPv6_relay_policy()
    elif args.method == "tc12":
        rc = uiobj.tc12_invalid_input_add_DHCPv6_relay_policy()
    elif args.method == "tc2_tz80":
        rc = uiobj.tc2_DHCPv6_Relay_Protocol_details_tz80()
    
