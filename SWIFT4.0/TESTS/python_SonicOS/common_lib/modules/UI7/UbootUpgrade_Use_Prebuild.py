from asyncio.log import logger
from cmath import log
import os
import re
import sys
import string
import telnetlib
import argparse
import json
import time
import base64
from runner.unittest.suite import UnittestSuite
from runner.unittest.setup import Test, skip_if_dts, repeat_method
import unittest
from collections import OrderedDict
from pymouse import *
from pykeyboard import PyKeyboard
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from modules.UI7.common_require import *
from utm import * 
from util.openstack import Openstack
from util.ssdh import SSDH
from lib.modules.CLI.system import SettingCli,AdminCli,StatusCli
from lib.modules.CLI.network import InterfaceCli
from lib.modules.API.network import InterfaceIPv4Api
from pyvirtualdisplay import Display
from lib.modules.API import system

display = Display(visible=0, size=(1920,1200), backend='xvfb')    

fw_cli = Firewall('192.168.168.168', user='admin', password='password', supported_config_mode='cli-ssh')
fw_api = Firewall('192.168.168.168', user='admin', password='password', supported_config_mode='api')


ssdh_build = SSDH(Params.build)
tsr = system.DiagnosticApi(fw_api)
setting_obj = system.SettingApi(fw_api)
setting_cli = SettingCli(fw_cli)


pykey = PyKeyboard()
system_ver = StatusCli(fw_cli)

safemode_ip1 = '192.168.168.168'
safemode_ip2 = '192.168.1.254'

# build_file_unresolved = os.popen('ls /logs/Dont_Delete_Uboot_Upgrade_Release_Build/{}/{}'.format(Params.sonicos_ver,Params.product)).read()
# logger.info('Build file is ' + build_file_unresolved)
# build_pattern = re.compile(r'sw.*', re.I)
# build_file_resolved = build_pattern.findall(build_file_unresolved)[0]
# logger.info(build_file_resolved)
# webpost_file_path= '/logs/Dont_Delete_Uboot_Upgrade_Release_Build/' + str(Params.sonicos_ver) + '/' + str(Params.product) + '/' + str(build_file_resolved)

class Uboot_Upgrade:

    def upgrade_fw_in_safemode_from_linux(self, boot_type, build_type):
        try:
            out = os.popen('ping 192.168.168.168 -c 2').read()
            if '100% packet loss' not in out:
                logger.debug("Fw is up for test")
                if boot_type == 'factory_default':
                    self.login_safemode_from_ui_linux()
                    time.sleep(35)
                    logger.debug("Click Upload Image")
                    self.ui_wrapper.click_element('xpath', '//span[contains(text(), "Upload Firmware")]')
                    time.sleep(4)
                    logger.debug("Click - Browse")
                    self.ui_wrapper.click_element('xpath','//span/button[contains(text(),"Browse")]')
                    if build_type == 'prebuild':
                        file_path = Params.prebuild
                    elif build_type == 'newbuild':
                        file_path = Params.build
                    elif build_type == 'webpost':                        
                        file_path = webpost_file_path.replace("\n","")
                    logger.debug("The file that you want to upload is:" + file_path)
                    time.sleep(3)
                    pykey.type_string(file_path)
                    time.sleep(5)
                    pykey.tap_key(pykey.enter_key)
                    time.sleep(5)
                    logger.debug("Click - Upload")
                    self.ui_wrapper.click_element('xpath','//div/button[contains(text(),"Upload")]')
                    time.sleep(5)
                    logger.debug("Sleep 30s wait for the page reload.")
                    time.sleep(80)
                    logger.debug("Check - if new firmware is loaded from UI")
                    if self.ui_wrapper.does_element_exist_now('xpath', '//span[contains(text(),"This is the uploaded firmware")]'):
                        logger.debug("New firmware is loaded from UI successfully.")
                        logger.debug("Prepare booting uploaded fw.")                                
                        boot_button = self.browser.find_elements('xpath', '//span[contains(@class, "icon-reboot")]')
                        logger.debug(len(boot_button))
                        time.sleep(2)
                        boot_button[-1].click()
                        logger.debug('Click Boot firmware with Factory Default Configuration.')
                        time.sleep(2)
                        self.ui_wrapper.click_element('xpath', '//*[contains(text(),"Factory Default Configuration")]')
                        logger.debug('Click OK.')
                        time.sleep(2)
                        self.ui_helper.submit_page()
                        logger.info('Sleep 180s wait for fw up.')
                        time.sleep(240)
                        logger.debug('Close browser')
                        os.system('pkill firefox')
                        time.sleep(5)
                        retries = 1
                        while retries < 20:
                            try:
                                logger.info('Sleep 30s wait for fw up.')
                                time.sleep(30)
                                out = os.popen('ping {} -c 2'.format(safemode_ip1)).read()
                                logger.info(out)
                                if '100% packet loss' not in out:
                                    break
                            except Exception as err:
                                retries += 1
                                if retries < 20:
                                    logger.info("Firewall is not up after factory reboot, retrying")
                                    continue
                                else:
                                    Assertion.fail("Firewall is not up after factory reboot with maximum retries")
                        logger.info('Firewall is up')         
                        self.get_version_use_cli()
                        logger.debug("After booting with factory default in safemode, the new version is:" + str(version))

                        if build_type == 'prebuild':
                            if Params.prebuild:
                                ssdh_prebuild = SSDH(Params.prebuild)
                                ssdh_prebuild.is_build_sig()
                                ssdh_prebuild_version = ssdh_prebuild.get_version_total_string()
                                logger.info('The version get via ssdh is:' + ssdh_prebuild_version)
                                if version == ssdh_prebuild_version:
                                    logger.debug("Boot fw successfully after upgrade to prebuild version in safemode from UI")                            
                                else:
                                    Assertion.fail('Boot fw failed after upgrade to prebuild version in safemode from UI.')
                                # display.stop()
                        elif build_type == 'newbuild':
                            if version == Params.scmlabel:
                                logger.debug('Boot fw successfully after upgrade to newbuild version in safemode from UI.')
                                # display.stop()
                            else:
                                Assertion.fail("Boot fw failed after upgrade to newbuild version in safemode from UI")
                        elif build_type == 'webpost':
                            file_path_webpost = webpost_file_path.replace("\n","")
                            logger.info(file_path_webpost)
                            release_build = SSDH(file_path_webpost)
                            release_build.is_build_sig()
                            release_build_version = release_build.get_version_total_string()
                            logger.info('The webpost version get via ssdh is:' + release_build_version)
                            if version == release_build_version:
                                logger.debug('Boot fw successfully after upgrade to webpost version in safemode from UI.')
                            else:
                                Assertion.fail("Boot fw failed after upgrade to webpost version in safemode from UI")

                    else:
                        Assertion.fail("New firmware is loaded from UI failed.")
                else:
                    self.login_safemode_from_ui_linux()
                    time.sleep(40)
                    self.ui_wrapper.click_element('xpath', '//span[contains(@class, "icon-reboot")]')
                    logger.debug('Click Boot firmware with current Configuration.')
                    time.sleep(6)
                    self.ui_wrapper.click_element('xpath', '//*[contains(text(),"with Current Configuration")]')
                    time.sleep(5)
                    logger.debug('Click OK.')
                    self.ui_helper.submit_page()
                    logger.debug('Waiting 180s for boot fw')   
                    time.sleep(180)
                    logger.debug('Close browser')  
                    os.system('pkill firefox')
                    time.sleep(5)
                    retries = 1
                    while retries < 20:
                        try:
                            logger.info('Sleep 30s wait for fw up.')
                            time.sleep(30)
                            out = os.popen('ping {} -c 2'.format(safemode_ip1)).read()
                            logger.info(out)
                            if '100% packet loss' not in out:
                                break
                        except Exception as err:
                            retries += 1
                            if retries < 20:
                                logger.info("Firewall is not up after current reboot, retrying")
                                continue
                            else:
                                Assertion.fail("Firewall is not up after current reboot with maximum retries")
                    logger.info('Firewall is up')    
                    # display.stop()        
                    self.check_settings_after_import_prefs_current_boot_use_api()
            else:
                Assertion.fail("Fw is not up now, skip the case.")  
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Load firmware in safemode failed")
    
    def enable_api(self):
        admin = AdminCli(fw_cli)
        api_dict = {
           'sonicos-api': True,
           'basic': True,
        }
        result = admin.sonicos_api(**api_dict)
        Assertion.assert_equal(result, True, "ERR: Enable api failed.")

    def config_interface_x1_cli(self):
        x1_config = InterfaceCli(fw_cli)
        x1_static = {
            'if': 'x1',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': '172.17.1.168',
            'gateway': '172.17.1.1',
            'dns1': '10.190.202.200',
        }
        rc = x1_config.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 failed")

    def check_settings_after_import_prefs_current_boot_use_api(self):
        self.enable_api()
        x1_api = InterfaceIPv4Api(fw_api)
        data = x1_api.get_interface_status('X1')
        try:
            if data['interfaces'][0]['ipv4']['ip_assignment']['mode']['static']['ip'] == '172.17.1.168':
                logger.debug('WAN IP is right after importing prefs or current boot.')
            if data['interfaces'][0]['ipv4']['ip_assignment']['mode']['static']['gateway'] == '172.17.1.1':
                logger.debug('WAN gateway is right after importing prefs or current boot.')
            if data['interfaces'][0]['ipv4']['ip_assignment']['mode']['static']['dns']['primary'] == '10.190.202.200':
                logger.debug('WAN dns is right after importing prefs or current boot.')
        
        except Exception as err:
            logger.error(str(err))
            Assertion.fail("Check settings failed after importing prefs from UI")

    def login_safemode_from_ui_linux(self):
        try:
            self.enter_safemode_cli()
            logger.debug("Check safmode status first")
            retries = 1
            while retries < 8:
                try:
                    logger.debug('Sleep 30s for firewall enter safemode')
                    time.sleep(30)
                    self.ui_wrapper.get_browser()
                    rc1 = os.popen('ping {} -c 2'.format(safemode_ip1)).read()
                    logger.info(rc1)
                    if '100% packet loss' not in str(rc1):
                        logger.debug('ping {} successfully'.format(safemode_ip1))
                        logger.debug("Start login with {}".format(safemode_ip1))
                        self.ui_wrapper.go_to_url('https://{}/'.format(safemode_ip1))
                        time.sleep(5)
                        current_url = self.ui_wrapper.browser.current_url
                        logger.debug("Current URL : " + str(current_url))
                        if 'login' in current_url:
                            break
                        else:
                            logger.debug("Can ping {}, but cannot login via https.".format(safemode_ip1))
                            Assertion.fail("Can ping {}, but cannot login via https.".format(safemode_ip1))
                    else:
                        rc2 = os.popen('ping {} -c 2'.format(safemode_ip2)).read()
                        logger.info(rc2)
                        if '100% packet loss' not in str(rc2):
                            logger.debug('ping {} successfully'.format(safemode_ip2))
                            logger.debug("Start login with {}".format(safemode_ip2))
                            self.ui_wrapper.go_to_url('https://{}/'.format(safemode_ip2))
                            time.sleep(5)
                            current_url = self.ui_wrapper.browser.current_url
                            logger.debug("Current URL : " + str(current_url))
                            if 'login' in current_url:
                               break
                            else:
                                logger.debug("Can ping {}, but cannot login via https.".format(safemode_ip1))
                                Assertion.fail("Can ping {}, but cannot login via https.".format(safemode_ip2))
                except Exception as err:
                    retries += 1
                    if retries < 8:
                        logger.debug("Safemode status is not ready.")
                        continue
                    else:
                        logger.debug("Check safemode status with maximum retries")
                        Assertion.fail("Cannot access to FW VS MGMT port,Need to check it.")
            time.sleep(10)
            logger.debug("Login fw in safemode from UI")
            logger.debug("Enter Maintenance Key")
            MaintenanceKey = ['2b6229f0a1a','6703a72fed7','81d120c52ab','7571c9699f6','510dc59e216','8a6752503e0','afbacc84ea7','018ce0f2201','d5ddca90257',
            'fc73e484795','798ebd007ec','9c9f2d83f2c','18891349079','c30a53cc84e','0b067df69c4','a2ab8a524a5','74b8f6fd679','a2ae80ae777','18a3e0c0cee',
            '09293ec3e37','aaf0672b453','05b9db121ec','ba36caf5898','a8b7df21e1b','e7b83beb316','7854e9e79f8','cc44e51f647','3450ab0f956','11ce5031989',
            '7ad84803af5','465894f098a','4c473eb5da6','2afbd14d954','2ba166f9c77','2e9fe0221a1','0b64ad66161','63e667ad545','369c315253e','cd866bd2533',
            '94dbd17c243','af110e9c74e','de5335c5231','da8d9f5eb19','8ed12fdd33d','533ac38ddeb','ef370cc15e4','a375ab0516d','414ca2bd3ce','a8a9d6f6f4f',
            'afe622f0ea8','e7b50cb4c66','07d55758035','3ee74d2d576','7efce54c8f3','e9da1e39de4','cdb80b277c2','64599883fd6','c097df0e625','7375d70f68f',
            '6e771ec8cca','9e3aca5d147','4314b5b45a9','7bb078a8c1b','a2c80c649f2','8c8f4ed6002','82087ae8d62','cc04a4ef0f5','fb2400b05ad','6ef318edd02',
            'cfaeee48f40','7bb98c5e2ce','8e3761aa31b','09ad56f00dc','b677bbad978','8cc8b6e0e94','33ac2a56a23','ce46f3bb729','38489682ac5','17a3611b279',
            'fa601f49af9','b7bc583b1c2','28321437527','80b1ee8b050','e0d72aa9879','948910a75d5','972fd481076','ebfb5232a9c','07d55758035','3ee74d2d576',
            '3a72e7b5a24','878b8a0689d','5223773848c','eca63074b72','034e11bdf10','7a8f61d4cb6','9cc24a8459c','947d6fd9558',
            'fad36c815e4','bd8ff6e5e48','ade89533d8a','45902f4a350','705ed7a2445','e24e75596ce','05a39146a9e','aad3d97ad4d',
            '30a5ce2f550','790f366c484','b846c63d39e','95bcead2b0e','af39326c2f0','d209de40f73','bce7fe86806','1b3eb9bb926'
            ]
            try:
                for Key in MaintenanceKey:
                    self.ui_wrapper.set_text_field('xpath', "//input[@type='password' and @name='emailInput']", Key)
                    time.sleep(2)
                    logger.debug("Click LOGIN")
                    self.ui_wrapper.click_element('xpath', '//div[contains(text(), "LOGIN")]')
                    time.sleep(3)
                    current_url = self.browser.current_url
                    logger.info(current_url)
                    if 'login' not in current_url:
                        break
                    else:
                        logger.debug("Cannot login safemode UI via this  Maintenance Key, Try another one...")
                logger.info('Login fw in safemode from UI successfully.')
                time.sleep(5) 
            except Exception as err:
                logger.error("Exception \t: " + str(err))
                Assertion.fail("No Maintenance Key for this dut, pls check again.") 

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Login fw in safemode from UI failed")

    def enable_interface_X0_ssh(self):
        logger.info('Enable management ssh')
        fw_console = Firewall('192.168.168.168', console_ip=consvr, console_port=conport,user='admin', password='password', supported_config_mode='cli-console')
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

    def get_version_use_cli(self):
        global version
        self.get_console_info()
        time.sleep(20)
        retries = 1
        while retries < 20:
            try:
                ssh_return = self.enable_interface_X0_ssh()
                if not ssh_return:
                    break
            except Exception as err:
                retries += 1
                if retries < 20:
                    logger.info("Enable ssh failed, retrying")
                    continue
                else:
                    Assertion.fail("Enable ssh failed with maximum retries")
        logger.info('Start to get fw version.')
        
        telnet_connect = telnetlib.Telnet()
        telnet_connect.open(consvr,conport)
        logger.debug("Input console server's user and password.")
        telnet_connect.read_until(b'login: ',timeout=10)
        telnet_connect.write('admin'.encode('ascii') + b'\n')
        telnet_connect.read_until(b'Password: ',timeout=10)
        telnet_connect.write('password'.encode('ascii') + b'\n')
        time.sleep(2)
        logger.debug("Input FW's user.")
        telnet_connect.read_until(b'User: ',timeout=10)
        telnet_connect.write('admin'.encode('ascii') + b'\n')
        telnet_connect.read_until(b'Password: ',timeout=10)
        logger.debug("Input password: password.")
        telnet_connect.write('password'.encode('ascii') + b'\n')
        time.sleep(5)
        logger.debug("Get info.")
        console_response1 = telnet_connect.read_very_eager()
        logger.info(console_response1)
        if 'Access denied' in str(console_response1):
            telnet_connect.write('admin'.encode('ascii') + b'\n')
            telnet_connect.read_until(b'Password: ',timeout=10)
            logger.debug(f"Input password:{G_PASSWORD_NEW}.")
            telnet_connect.write(f'G_PASSWORD_NEW'.encode('ascii') + b'\n')
            time.sleep(5)
            logger.debug("Get info.")
            console_response2 = telnet_connect.read_very_eager()
            logger.info(console_response2)
            if 'Access denied' in str(console_response2):
                telnet_connect.write('admin'.encode('ascii') + b'\n')
                telnet_connect.read_until(b'Password: ',timeout=10)
                logger.debug("Input password:Admin_1234.")
                telnet_connect.write('Admin_1234'.encode('ascii') + b'\n')
                time.sleep(3)
        telnet_connect.write('diag show build-info'.encode('ascii') + b'\n')
        logger.debug("Get version info.")
        time.sleep(2)
        console_response = telnet_connect.read_very_eager()
        version_no_resolved = str(console_response).split('Uname')[0]
        logger.info(version_no_resolved)
        pattern = re.compile(r'Firmware Version.*(\d+\.\d+\.\d+\S+)', re.I)
        ver = pattern.findall(version_no_resolved)
        logger.info(ver[0].split('\\'))
        version = str(ver[0].split('\\')[0])
        logger.debug('The current firmware version get from console is: ' + version)
        return version
    
    def get_console_info(self):
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

    def enter_safemode_cli(self):
        self.get_console_info()
        fw_console = Firewall('192.168.168.168', console_ip=consvr, console_port=conport,user='admin', password='password', supported_config_mode='cli-console')
        setting = SettingCli(fw_console)
        output = setting.enable_safemode()
        time.sleep(50)
    
    def export_and_check_TSR(self):
        logger.info("Exprot tsr...")
        rc = tsr.get_tsr_part('Network','Interfaces')
        logger.info(rc)
        logger.info("Check tsr...")
        if '172.17.1.168' in rc and '172.17.1.1' in rc and '10.190.202.200' in rc:
            logger.info('export_and_check_TSR successfully')
        else:
            Assertion.fail("export_and_check_TSR failed.")

    def export_and_check_Prefs(self):
        logger.info("Exprot Prefs...")
        setting_obj.export_setting_exp(filepath='/tmp/preference_test.exp')
        logger.info("Check Prefs...")
        rc = open('/tmp/preference_test.exp').read()
        prefs_content = base64.b64decode(rc).decode("utf-8")
        logger.info(prefs_content)
        if '172.17.1.168' in prefs_content and '172.17.1.1' in prefs_content and '10.190.202.200' in prefs_content:
            logger.info('export_and_check_Prefs successfully')
        else:
            Assertion.fail("export_and_check_Prefs failed.")

    def upgrade_fw_release(self, build_type):
        try:
            file_name = ''
            if build_type == 'releasebuild':
                file = os.popen('ls /logs/Dont_Delete_Uboot_Upgrade_Release_Build/{}/{}'.format(Params.sonicos_ver,Params.product)).read()
                file_name = os.path.basename(file)
                file_part= '/logs/Dont_Delete_Uboot_Upgrade_Release_Build/' + Params.sonicos_ver + '/' + Params.product + '/' + file_name
                file_path = file_part.replace("\n","")
                logger.info("The file that you want to upload is:" + file_path)
                release_build = SSDH(file_path)
                release_build.is_build_sig()
                release_build_version = release_build.get_version_total_string()
                logger.info(release_build_version)
            else:
                file_path = Params.build
            logger.debug("The file that you want to upload is:" + file_path)
            import_dict = {
                'protocol': 'scp',
                'passwd': 'password',
                'server': '192.168.168.200',
                'user': 'root',
                'file': file_path
            }
            rc = setting_cli.import_firmware(**import_dict)
            if not rc:
                Assertion.fail('Import firmware failed.')
            else:
                logger.info('Import firmware succeed,Prepare to boot firmware.')
            cmds = ['configure', 'boot uploaded factory-default', 'end', 'exit']
            fw_cli.do_cli_commands(cmds)
            self.get_version_use_cli()
            if build_type == 'releasebuild':
                if version == release_build_version:
                    logger.info('Boot firmware passed.')
                else:
                     Assertion.fail('Boot firmware failed.')
            else:
                if version == Params.scmlabel:
                    logger.info('Boot firmware passed.')
                else:
                     Assertion.fail('Boot firmware failed.')
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Login fw in safemode from UI failed")
