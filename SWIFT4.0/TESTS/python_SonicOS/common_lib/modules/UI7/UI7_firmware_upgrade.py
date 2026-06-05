import os
import re
import sys
import string
import argparse
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/UI7_Linux/UI7_Firmware_Upgrade')

from pymouse import *
from pykeyboard import PyKeyboard
from modules.UI7.common_require import *
from utm import Firewall
from utm import FirewallCGI

from runner.settings import logger
from modules.CLI import network
from runner.unittest.setup import Test
from runner.utils.assertion import Assertion
from test_cases.Initial_parameter import Parameter
from pprint import pprint
from util.openstack import Openstack
from modules.CLI.system import StatusCli
from modules.CLI.system import SettingCli
from modules.API.system import StatusApi
from modules.CLI.network import InterfaceCli
from runner.settings import Params
from utm import is_Firewall_up

ip = Parameter.FIREWALL
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
fw_cgi = Firewall(ip, user='admin', password='password', supported_config_mode='cgi')
fw_api = Firewall(ip, user='admin', password='password', supported_config_mode='api')


interface = network.InterfaceCli(fw_cli)
system = StatusCli(fw_cli)
system_api = StatusApi(fw_api)

pykey = PyKeyboard()


class Upgrade_firmware:

    def upgrade_firmware_from_UI(self):
        # Before upgrading, restore firewall firstly  # # #
        logger.info('------- Before upgrading, restore firewall firstly -----------')
        self.get_console_info() 
        fw_console = Firewall(ip, console_ip=consvr, console_port=conport,user='admin', password='password', supported_config_mode='cli-console')
        setting = SettingCli(fw_console)
        restore_fw = setting.restore(consvr, conport)
        #### Compare the versions: between uploaded and already existed  # # #
        logger.info('-------- Compare the versions: between uploaded and already existed --------')
        self.show_status_of_fw()
        logger.info("The current firewall version is: " + ver[0])
        logger.info("The uploaded firewall version is: " + Params.scmlabel)
        if ver and ver[0] == Params.scmlabel:
            logger.info('------- Firewall has the same version as uploaded firewall. Omit uploading --------')
        else:
            logger.info('------- Firewall has different build with uploaded. Prepare uploading new version --------')
            logger.info('In order to upgrade fw, to register the firewall.')
            self.config_interface_X1()
            self.register_fw()
            logger.info('Login fw.')
            self.login_ui()
            self.load_new_firmware()                      
    
    def load_new_firmware(self, upgrade_type=None):
        self.navigation.navigate_to_device_firmware_section()
        try:
            logger.info("Click - Upload Firmware from UI")
            time.sleep(2)
            self.ui_wrapper.click_element('xpath','//span[contains(text(),"Upload Firmware")]')
            logger.info("Click - OK")
            self.ui_helper.submit_page()
            time.sleep(2)
            logger.info("Click - Browse")
            self.ui_wrapper.click_element('xpath','//span/button[contains(text(),"Browse")]')
            time.sleep(2)
            if upgrade_type == 'upgrade_to_backup':
                logger.info("Upgrade to sprint42.")
                file_path = '/logs/backup/sw_tz_570_eng.7.0.0.0-P212.bin.sig'               
            else:
                file_path = Params.build
            logger.info("The file that you want to upload is:" + file_path)
            pykey.type_string(file_path)
            time.sleep(5)
            pykey.tap_key(pykey.enter_key)
            time.sleep(5)
            self.ui_wrapper.click_element('xpath','//div/button[contains(text(),"Upload")]')
            time.sleep(45)
            logger.info("Check - if new firmware is loaded from UI")
            if self.ui_wrapper.does_element_exist_now('xpath', '//span[contains(text(),"This is the uploaded firmware")]'):
                logger.info("New firmware is loaded from UI successfully.")
                logger.info("Prepare booting uploaded fw as factory default configuration.")
                if upgrade_type == 'upgrade_to_backup':
                    self.boot_uploaded_fw_factory_default(boot_type='current_boot')
                else:
                    self.boot_uploaded_fw_factory_default()
                                 
            else:
                logger.info("New firmware is loaded from UI failed.")
                self.logout_ui()
                Assertion.fail("Upload firmware failed from UI")

        except Exception as err:
            logger.error(str(err))
            Assertion.fail("Upgrade firmware failed from UI")

    def boot_uploaded_fw_factory_default(self, upgrade_type=None, boot_type=None):
        self.get_console_info()
        # # Boot fw after uploaded new version# # #
        logger.info('Now begin to boot uploaded fw as factory default configuration from UI7.')
        logger.info('Click Boot button.')
        time.sleep(2)
        boot_button = self.browser.find_elements('xpath', '//span[contains(@class, "icon-reboot")]')
        logger.info(len(boot_button))
        time.sleep(2)
        boot_button[1].click()
        if boot_type == 'current_boot':
            logger.info('Click Boot firmware with current Configuration.')
            time.sleep(2)
            self.ui_wrapper.click_element('xpath', '//*[contains(text(),"with current Configuration")]')
            logger.info('Click OK.')
            self.ui_helper.submit_page()
            logger.info('Waiting for boot fw')   
            time.sleep(360)
            self.ui_wrapper.close_browser()
            self.ui_wrapper.quit()
            self.check_settings_after_current_boot()
        else:
            logger.info('Click Boot firmware with Factory Default Configuration.')
            time.sleep(2)
            self.ui_wrapper.click_element('xpath', '//*[contains(text(),"Factory Default Configuration")]')
            logger.info('Click OK.')
            self.ui_helper.submit_page()
            logger.info('Waiting for boot fw')   
            time.sleep(360)
            self.ui_wrapper.close_browser()
            self.ui_wrapper.quit()
            self.enable_interface_X0_ssh()
            self.show_status_of_fw()
            logger.info('Now the fw version is: ' + ver[0])
            if upgrade_type == 'upgrade_to_backup':
                if ver and ver[0] == '7.0.0.0-64v-42-P212-e6c15a93':
                    logger.info('Upgrade to backup version successfully.')
            else:
                if ver and ver[0] == Params.scmlabel:
                    logger.info('Upgrade to newest version successfully.')
        
    def check_settings_after_current_boot():
        self.enable_interface_X0_ssh()
        logger.info('Check whether some configurations still exists.')
        output = interface.show_interface_status(interface='X1', version='ipv4')
        logger.info(output)
        if Parameter.X1_IP in output and Parameter.X1_GW in output \
            and Parameter.DNS1 in outout and Parameter.DNS2 in output:
            logger.info('some configurations still exists on fw, current boot successfully.')
        else:
            Assertion.fail("After current booting,some configurations doesn't exist, current boot failed.")

    def upgrade_from_UI_safemode(self):
        try:
            self.ui_wrapper.get_browser()
            self.ui_wrapper.go_to_url(self.common.URL)
            logger.info("Enter Authentication code")
            self.get_ver_and_auth_code()
            self.ui_wrapper.set_text_field('class', 'ivu-input', auth_code)
            logger.info("Click-Authenticate button")
            self.ui_helper.submit_page()
            time.sleep(2)
            self.ui_wrapper.click_element('xpath','//span[contains(text(),"Upload Firmware")]')
            logger.info("Click - OK")
            self.ui_helper.submit_page()
            time.sleep(2)
            logger.info("Click - Browse")
            self.ui_wrapper.click_element('xpath','//span/button[contains(text(),"Browse")]')
            time.sleep(2)
            if upgrade_type == 'upgrade_to_backup':
                logger.info("Upgrade to sprint42.")
                file_path = '/logs/backup/sw_tz_570_eng.7.0.0.0-P212.bin.sig'                
            else:
                file_path = Params.build
            logger.info("The file that you want to upload is:" + file_path)
            pykey.type_string(file_path)
            time.sleep(5)
            pykey.tap_key(pykey.enter_key)
            time.sleep(5)
            self.ui_wrapper.click_element('xpath','//div/button[contains(text(),"Upload")]')
            time.sleep(45)
            logger.info("Check - if new firmware is loaded from UI")
            if self.ui_wrapper.does_element_exist_now('xpath', '//span[contains(text(),"This is the uploaded firmware")]'):
                logger.info("New firmware is loaded from UI successfully.")
                logger.info("Prepare booting uploaded fw as factory default configuration.")
                if upgrade_type == 'upgrade_to_backup':
                    self.boot_uploaded_fw_factory_default(boot_type='current_boot')
                else:
                    self.boot_uploaded_fw_factory_default()
                                 
            else:
                logger.info("New firmware is loaded from UI failed.")
                self.logout_ui()
                Assertion.fail("Upload firmware failed from UI")

        except Exception as err:
            logger.error(str(err))
            Assertion.fail("Upgrade firmware failed from UI")


    def config_interface_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gw': Parameter.X1_GW,
            'dns1': Parameter.DNS2,
            'dns2': Parameter.DNS1,
        }
        output = interface.config_interface(**x1_static)
        logger.info(output)
        Assertion.assert_equal(output, True, "ERR: Config X1 to static failed")
            
    def register_fw(self):
        logger.info('Register fw.')
        output = fw_cgi.register()
        logger.info(output)
        Assertion.assert_equal(output, True, "ERR: Register fw failed")

    def get_console_info(self):
        # # # Get console information # # #
        global consvr, conport
        logger.info('Get console information.')
        if Params.testbed:
            logger.info('---- This is ' + Params.testbed + ' -----')
            ostack = Openstack(Params.testbed)
            console_info = ostack.get_console_info()
            if console_info:
                consvr = console_info[0]
                conport = console_info[1]
        else:
            out = os.popen('hostname').read()
            hostname = out.split('-')[0]
            if hostname:
                logger.info('------------ ' + hostname + '------------')
                ostack = Openstack(hostname)
                console_info = ostack.get_console_info()
                if console_info:
                    consvr = console_info[0]
                    conport = console_info[1]
        logger.info('The console server is : ' + consvr)
        logger.info('The console port is :   ' + conport)

    def enable_interface_X0_ssh(self):
        logger.info('Enable management ssh')
        fw_console = Firewall(ip, console_ip=consvr, console_port=conport,user='admin', password='password', supported_config_mode='cli-console')
        interface_console = InterfaceCli(fw_console)
        x0_dict = {
            'if': 'x0',
            'zone': 'LAN',
            'ip': '192.168.168.168',
            'mgmt-ssh': True,    
        }
        output = interface_console.config_interface(**x0_dict)
        logger.info(output)
        Assertion.assert_equal(output, True, "ERR: Enable ssh failed")

    def get_ver_and_auth_code(self):
        global ver, auth_code
        status = system.show_status()
        ver_pattern = re.compile(r'Firmware Version.*(\d+\.\d+\.\d+\.\d+\S+)', re.I)
        ver = ver_pattern.findall(status)
        auth_code_pattern = re.compile(r'Authentication Code.*(\S+\S+\S+\S+\S+\S+\S+\S+\S)', re.I)
        auth_code_str = auth_code_pattern.findall(status)
        auth_code = auth_code_str[0].replace('-', '')

    def enter_safemode(self):
        fw_console = Firewall(ip, console_ip=consvr, console_port=conport,user='admin', password='password', supported_config_mode='cli-console')
        setting = SettingCli(fw_console)
        output = setting.enable_safemode()
        logger.info(output)
        Assertion.assert_equal(output, True, "ERR: Enable safemode failed")


    




        
