import re
import sys
import argparse
import sys
import os
from optparse import OptionParser

sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib/modules/ui/')
from networkdevice import Host

# sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
print(sys.path)
from runner.settings import logger
from modules.ui.ui_wrapper import Browser
from modules.ui.ui_helper import UIHelper
import time


class FWPage(Browser, UIHelper):
    def __init__(self, url, appurl, user, pwd):
        self.url = url
        self.appurl = appurl
        self.user = user
        self.password = pwd

    def login_fw_ui(self):
        try:
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("start logging...")
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
            logger.info("Action - Clicked Login")
            self.click_element('class', 'sw-login__trigger')
            logger.info('wait 10s to make sure login success.')
            time.sleep(10)
            logger.info(f"Login fw successful.")
            return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")
            return False

    def navigate_to_nat_rules_page(self):
        res = False
        try:
            self.go_to_url(self.appurl)
            res = True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            self.close_browser()
            logger.info("Firewall login failed")
        logger.info(f'go to nat rules page: {res}')
        return res

    def click_the_add_net_button(self):
        logger.info('wait 10s to load nat policy page')
        time.sleep(10)
        res = False
        try:
            logger.debug("Action - Clicking on Add icon...")
            res = self.click_element('class', "icon-add")
            if not res:
                logger.info('click add icon using class failed, start use xpath...')
                res = self.click_element('xpath',
                                         "//span[contains(@class, 'icon-add')]/following::span[contains(text(), '" + label + "')]")
        except Exception as err:
            logger.error("Exception \t: " + str(err))
        return res

    def select_drop_down_value(self, select_identifier, select_value, modal=False, ptype='ipv4', item_number=1, form_table='original'):
        try:
            logger.debug2("Selecting drop down value \t: " + str(select_value))
            if modal is True:
                self.click_element('xpath', "//div[contains(@class, 'sw-modal__main-body')]"
                                            f"//following::*[contains(text(), '{select_identifier}')]"
                                            "/following::*[contains(@class, 'sw-select__icon')]")
            # else:
            #     #if not duplicate elements, use it.
            #     self.click_element('xpath',
            #                        f"//span[contains(text(), '{select_identifier}')]"
            #                        f"/following::*[contains(@class, 'sw-select__icon')]")
            if ptype == 'ipv6':
                select_ipv6_radio = "//div[@class='sw-app sw-app--light sw-app--mode-app sw-typo-default sw-flexbox sw-flexbox--column fw-app-main']" \
                                    "//div/label[2]/span[@class='sw-radio__fake-radio-button sw-flexbox__flex-none']"
                output = self.click_element('xpath', select_ipv6_radio)
                logger.info(f'select ipv6 radio result: {output}')
            # only xpath the add net policy page.
            # select_icon_xpath = f"//div[@class='sw-flexbox__flex sw-flexbox sw-flexbox--column']/div/div/div" \
            #                     f"/div[@class='sw-form-row'][{item_number}]/div/div/span/div" \
            #                     f"/div[@class='sw-select__icon sw-flexbox sw-flexbox--center-items sw-flexbox--center-justify']"
            if form_table == 'translated':
                select_icon_xpath = f"//div[@class='sw-flexbox__flex sw-flexbox sw-flexbox--column']//div[@class='sw-form-row'][{item_number}]//div[@class='sw-select__icon sw-flexbox sw-flexbox--center-items sw-flexbox--center-justify']"
            else:
                select_icon_xpath = f"//div[@class='nat-policy-form__translated sw-flexbox__flex sw-flexbox sw-flexbox--column']//div[@class='sw-form-row'][{item_number}]//span/div/div/span/span"
            output = self.click_element('xpath', select_icon_xpath)
            logger.info(f'click drop down result: {output}')
            element = self.move_to_the_element('xpath',
                                               f"//span[contains(text(), '{select_identifier}')]"
                                               "/following::div[contains(@class, 'sw-dropdown')]/"
                                               f"span[text()='{select_value}']",
                                               False)
            element.click()
            logger.info(f'check value {select_value} in drop down result: True')
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.error("Action - Unable to select from drop down list")
            return False

    def get_drop_down_value(self, select_identifier):
        try:
            logger.debug2("Getting drop down value \t: " + str(select_identifier))
            ele = self.get_element('xpath',
                                   "//span[contains(text(), '" + select_identifier + "')]"
                                                                                     "/following::*[contains(@class, 'sw-select__label-text')]")
            value = ele.text
            return value
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.error("Action - Unable to select from drop down list")

    def click_original_translated_option(self):
        # logger.info('wait for 10s to check add net page...')
        # time.sleep(10)
        res_list = {}
        self.configure_text_field('Name', 'test111')
        res = self.does_page_have_text('Adding NAT Rule')
        logger.info(f'get page title: {res}')
        output = self.select_drop_down_value(
            select_identifier='Source',
            select_value='A.dns.baidu.com',
            form_table='original',
            item_number=1)
        res_list['tc1_res'] = output
        logger.info(f'tc1_res---select drop down value: {output}')
        output = self.select_drop_down_value(
            select_identifier='Source',
            select_value='A.pc2.baidu.com',
            form_table='original',
            item_number=1)
        res_list['tc11_res'] = output
        logger.info(f'tc11_res---select drop down value: {output}')
        output = self.select_drop_down_value(
            select_identifier='Destination',
            select_value='A.dns.baidu.com',
            form_table='translated',
            item_number=1)
        res_list['tc3_res'] = output
        logger.info(f'tc3_res---select drop down value: {output}')
        output = self.select_drop_down_value(
            select_identifier='Source',
            select_value='A.pc2.baidu.com',
            form_table='original',
            item_number=2)
        res_list['tc2_res'] = output
        logger.info(f'tc2_res---select drop down value: {output}')
        output = self.select_drop_down_value(
            select_identifier='Destination',
            select_value='A.dns.baidu.com',
            form_table='translated',
            item_number=2)
        res_list['tc4_res'] = output
        logger.info(f'tc4_res---select drop down value: {output}')

        # res = self.get_drop_down_value('Source')
        # logger.info(f'get source drop down: {res}')
        return res_list

    def click_original_translated_option_v6(self):
        res_list = {}
        # self.configure_text_field('Name', 'test111')
        res = self.does_page_have_text('Adding NAT Rule')
        logger.info(f'get page title: {res}')
        output = self.select_drop_down_value(
            select_identifier='Source',
            select_value='A.dns.baidu.com',
            form_table='original',
            ptype='ipv6',
            item_number=1)
        res_list['tc1v6_res'] = output
        logger.info(f'tc1v6_res---select drop down value: {output}')
        output = self.select_drop_down_value(
            select_identifier='Source',
            select_value='A.ipv6.baidu.com',
            form_table='original',
            # ptype='ipv6',
            item_number=1)
        res_list['tc11v6_res'] = output
        logger.info(f'tc11v6_res---select drop down value: {output}')
        output = self.select_drop_down_value(
            select_identifier='Destination',
            select_value='A.dns.baidu.com',
            form_table='translated',
            # ptype='ipv6',
            item_number=1)
        res_list['tc3v6_res'] = output
        logger.info(f'tc3v6_res---select drop down value: {output}')
        output = self.select_drop_down_value(
            select_identifier='Source',
            select_value='A.dns.baidu.com',
            form_table='original',
            # ptype='ipv6',
            item_number=2)
        res_list['tc2v6_res'] = output
        logger.info(f'tc2v6_res---select drop down value: {output}')
        output = self.select_drop_down_value(
            select_identifier='Destination',
            select_value='A.dns.baidu.com',
            form_table='translated',
            # ptype='ipv6',
            item_number=2)
        res_list['tc4v6_res'] = output
        logger.info(f'tc4v6_res---select drop down value: {output}')
        return res_list

    def get_a_page_source(self):
        self.get_browser()
        self.go_to_url(self.appurl)
        logger.info("Logging in to wan server via ui")
        return self.get_page_source()

    def close_browser(self):
        self.browser.close()


# uiobj = FWPage('https://12.12.1.50', 'test', 'test')
# rc = uiobj.login_external_auth_server()
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Login guest service by UI')
#     parser.add_argument('-url', type=str, dest='url', required=True, help='fw https login url')
#     parser.add_argument('-appurl', type=str, dest='appurl', required=True, help='fw https login url')
#     parser.add_argument('-user', type=str, dest='user', required=True, help='user to login guest service')
#     parser.add_argument('-pwd', type=str, dest='pwd', required=True, help='pwd to login guest service')
#     args = parser.parse_args()
#     print(args.url, args.appurl, args.user, args.pwd)
#     ui_obj = FWPage(args.url, args.appurl, args.user, args.pwd)
#     res = ui_obj.login_fw_ui()
#     print(f'login fw result is {res}')
#     if res:
#         # output = ui_obj.get_a_page_source()
#         logger.info('start go to nat rules page...')
#         output = ui_obj.navigate_to_nat_rules_page()
#         logger.info(f'start go to nat rules page: {output}')
#         logger.info('click Add net button...')
#         output = ui_obj.click_the_add_net_button()
#         logger.info(f'click add net button: {output}')
#         logger.info('start click original source option...')
#         output = ui_obj.click_original_source_option()
#         logger.info(f'click original source option: {output}')
#
#         ui_obj.close_browser()

