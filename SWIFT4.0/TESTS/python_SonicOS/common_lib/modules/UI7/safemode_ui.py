import os
import sys
import time
from pymouse import *
from pykeyboard import PyKeyboard
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from modules.UI7.common_require import *
from utm import Firewall
from runner.settings import Params, logger
from runner.utils.assertion import Assertion


class UISafemode:
    safemode_ip1 = '192.168.168.168'
    safemode_ip2 = '192.168.1.254'
    file_path = Params.build
    pykey = PyKeyboard()
    # Gen7 MaintenanceKey
    MaintenanceKey = [
        'b7bc583b1c2','2b6229f0a1a','6703a72fed7','81d120c52ab','7571c9699f6','510dc59e216','8a6752503e0','afbacc84ea7','018ce0f2201',
        'd5ddca90257','fc73e484795','798ebd007ec','9c9f2d83f2c','18891349079','c30a53cc84e','0b067df69c4','a2ab8a524a5','74b8f6fd679',
        'a2ae80ae777','18a3e0c0cee','09293ec3e37','aaf0672b453','05b9db121ec','ba36caf5898','a8b7df21e1b','e7b83beb316','7854e9e79f8',
        'cc44e51f647','3450ab0f956','11ce5031989','7ad84803af5','465894f098a','4c473eb5da6','2afbd14d954','2ba166f9c77','2e9fe0221a1',
        '0b64ad66161','63e667ad545','369c315253e','cd866bd2533','94dbd17c243','af110e9c74e','de5335c5231','da8d9f5eb19','8ed12fdd33d',
        '533ac38ddeb','ef370cc15e4','a375ab0516d','414ca2bd3ce','a8a9d6f6f4f','afe622f0ea8','e7b50cb4c66','07d55758035','3ee74d2d576',
        '7efce54c8f3','e9da1e39de4','cdb80b277c2','64599883fd6','c097df0e625','7375d70f68f','6e771ec8cca','9e3aca5d147','4314b5b45a9',
        '7bb078a8c1b','a2c80c649f2','8c8f4ed6002','82087ae8d62','cc04a4ef0f5','fb2400b05ad','6ef318edd02','cfaeee48f40','7bb98c5e2ce',
        '8e3761aa31b','09ad56f00dc','b677bbad978','8cc8b6e0e94','33ac2a56a23','ce46f3bb729','38489682ac5','17a3611b279','fa601f49af9',
        '28321437527','80b1ee8b050','e0d72aa9879','948910a75d5','972fd481076','ebfb5232a9c','07d55758035','3ee74d2d576','3a72e7b5a24',
        '878b8a0689d','5223773848c','eca63074b72','034e11bdf10','7a8f61d4cb6','19843ec22ff','d8ad8168eb4','790f366c484','32e47b78f97',
        '6169cb867fa','4314b5b45a9','638387825dc','29750812171','8c18c8cb4b1','0f7a8e0e92f','ae4ad0d1c8e','ade89533d8a','42b7cf7d7b5',
        'ab61cb3ae4e','45902f4a350'
    ]
    # Gen8 MaintenanceKey
    MaintenanceKey_gen8 = [
        'f06acd2fbad','c7a96e91ae1','062f2caa8ee','12161c40c2d','2833d562018','31bbb56b2c6','0d3c20102a5','1d426e3e1bd','0073a7db0fe',
        '259b76626c1','525b1379868','288841d3320','0635493df78','aba9e42aaa0','0635493df78','fd7d501e6fc','a5a3f0982d4','5675b682383',
        '4e7ea402e58','a02e40d43df','9b81fb92f10','ca48d962229','a79061bd47d','4d07ea587f9','5a9d6dbada5','72fca50ea20','62cbf28bec2',
        '7e404d3d2d9','245df0124ca','fadd9e653c1','3671ab0470b','74ab11b2cbb','45678186fa5','2dca61ea433','5a01a1f80f8','c80f6d41e3f',
        '4cae2e53ca0','22890229b34','1fe3873098c','7ecac69b7ec','9cc24a8459c','22890229b34','947d6fd9558','29e75e404d0','fad36c815e4',
        '33724241642','bd8ff6e5e48','e24e75596ce','705ed7a2445','30a5ce2f550','aad3d97ad4d','05a39146a9e','db8d844a888','519c187bf00',
        '15ba2ae61b0','4b69cf901ff','6169cb867fa','8ba8b28616c','e07b1976d01','cbb5632550e','eee3e2befba','39d347be7b2','79f0c1227af',
        '7dd821817a6','e080d633436','a73d731f5c2','fd4fb155253',
        ]

    def login_fw_from_safemode_ui(self):
        try:
            logger.info("Check safmode status first")
            retries = 1
            while retries < 8:
                try:
                    logger.info('Sleep 30s for firewall enter safemode')
                    time.sleep(30)
                    self.ui_wrapper.get_browser()
                    rc1 = os.popen('ping {} -c 2'.format(self.safemode_ip1)).read()
                    logger.info(rc1)
                    if '100% packet loss' not in str(rc1):
                        logger.info('ping {} successfully'.format(self.safemode_ip1))
                        logger.info("Start login with {}".format(self.safemode_ip1))
                        self.ui_wrapper.go_to_url('https://{}/'.format(self.safemode_ip1))
                        time.sleep(5)
                        current_url = self.ui_wrapper.browser.current_url
                        logger.info("Current URL : " + str(current_url))
                        if 'login' in current_url:
                            break
                        else:
                            logger.info("Can ping {}, but cannot login via https.".format(self.safemode_ip1))
                            Assertion.fail("Can ping {}, but cannot login via https.".format(self.safemode_ip1))
                    else:
                        rc2 = os.popen('ping {} -c 2'.format(self.safemode_ip2)).read()
                        logger.info(rc2)
                        if '100% packet loss' not in str(rc2):
                            logger.info('ping {} successfully'.format(self.safemode_ip2))
                            logger.info("Start login with {}".format(self.safemode_ip2))
                            self.ui_wrapper.go_to_url('https://{}/'.format(self.safemode_ip2))
                            time.sleep(5)
                            current_url = self.ui_wrapper.browser.current_url
                            logger.info("Current URL : " + str(current_url))
                            if 'login' in current_url:
                                break
                            else:
                                logger.info("Can ping {}, but cannot login via https.".format(self.safemode_ip1))
                                Assertion.fail("Can ping {}, but cannot login via https.".format(self.safemode_ip1))
                except Exception as err:
                    retries += 1
                    if retries < 8:
                        logger.info("Safemode status is not ready.")
                        continue
                    else:
                        logger.info("Check safemode status with maximum retries")
                        Assertion.fail("Cannot access to FW VS MGMT port,Need to check it.")
            time.sleep(10)
            logger.info("Login fw in safemode from UI")
            logger.info("Enter Maintenance Key")
            try:
                for Key in self.MaintenanceKey:
                    self.ui_wrapper.set_text_field('xpath', "//input[@type='password' and @name='emailInput']", Key)
                    time.sleep(2)
                    logger.info("Click LOGIN")
                    self.ui_wrapper.click_element('xpath', '//div[contains(text(), "LOGIN")]')
                    time.sleep(3)
                    current_url = self.browser.current_url
                    logger.info(current_url)
                    logger.info(Key)
                    if 'login' not in current_url:
                        break
                    else:
                        logger.info("Cannot login safemode UI via this  Maintenance Key, Try another one...")
                logger.info('Login fw in safemode from UI successfully.')
                time.sleep(5) 
            except Exception as err:
                logger.error("Exception \t: " + str(err))
                Assertion.fail("No Maintenance Key for this dut, pls check again.") 
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Login fw in safemode from UI failed")
    
    def upload_fw_from_safemode_ui(self, restore_default=True):
        check_tag = False
        logger.info("Upload new build from safemode UI... ... ...")
        try:
            upload_path = '//span[contains(text(), "Upload Firmware")]'
            for i in range(10):
                logger.info(f'times {i+1} to click Upload Firmware...')
                logger.info("wait for 30s to make sure the browser is loading completely...")
                time.sleep(30)
                logger.info(f"Click Upload Image using path :{upload_path}")
                if self.ui_wrapper.does_element_exist_now('xpath', upload_path):
                    logger.info("Upload Firmware button is visible")
                    self.ui_wrapper.click_element('xpath', upload_path)
                    time.sleep(3)
                    check_tag = True
                    break
                else:
                    logger.info("Upload Firmware button is not visible")
            else:
                logger.info("Cannot find Upload Firmware button after 10 times.")

            if check_tag:
                logger.info("Check - if Browse button is visible")  
                browse_path = '//span/button[contains(text(),"Browse")]'
                logger.info(f"Browse button using path :{browse_path}")
                if self.ui_wrapper.does_element_exist_now('xpath', browse_path):
                    logger.info("Browse button is visible")
                    logger.info("Click - Browse")
                    try:
                        self.ui_wrapper.click_element('xpath',browse_path)
                    except Exception as err:
                        logger.error("Exception \t: " + str(err))
                        Assertion.fail("Click Browse button failed")
                    logger.info("The file that you want to upload is:" + self.file_path)
                    time.sleep(3)
                    self.pykey.type_string(self.file_path)
                    time.sleep(5)
                    self.pykey.tap_key(self.pykey.enter_key)
                    time.sleep(5)
                    logger.info("Click - Upload")
                    upload_path = '//div/button[contains(text(),"Upload")]'
                    logger.info(f"Upload button using path :{upload_path}")
                    self.ui_wrapper.click_element('xpath',upload_path)
                    time.sleep(5)
                    logger.info("Sleep 220s wait for the page reload.")
                    time.sleep(220)
                    logger.info("Check - if new firmware is loaded from UI")
                    if self.ui_wrapper.does_element_exist_now('xpath', '//span[contains(text(),"This is the uploaded firmware")]'):
                        logger.info("New firmware is loaded from UI successfully.")
                        logger.info("Prepare booting uploaded fw.")   
                        icon_reboot_path = '//div[contains(., "This is the uploaded firmware")]/ancestor::div[contains(@class, "sw-table-row")]//span[contains(@class, "icon-reboot")]'
                        logger.info(f"Reboot icon button using path :{icon_reboot_path}")  
                        self.ui_wrapper.click_element('xpath',icon_reboot_path)
                        logger.info('Click Boot firmware with Current Configuration.')
                        time.sleep(2)
                        if restore_default:
                            Default_config_path = '//*[contains(text(),"with Default Configuration")]'
                            logger.info(f"Default Configuration button using path :{Default_config_path}")
                            self.ui_wrapper.click_element('xpath', Default_config_path)
                        else:
                            current_config_path = '//*[contains(text(),"with Current Configuration")]'
                            logger.info(f"Current Configuration button using path :{current_config_path}")
                            self.ui_wrapper.click_element('xpath', current_config_path)
                        logger.info('Click OK.')
                        time.sleep(2)
                        self.ui_helper.submit_page()
                        logger.info('Sleep 600s wait for fw up.')
                        time.sleep(600)
                        logger.info('Close browser')
                        os.system('pkill firefox')
                        time.sleep(5)
                        retries = 1
                        while retries < 20:
                            try:
                                logger.info('Sleep 60s wait for fw up.')
                                time.sleep(60)
                                out = os.popen('ping {} -c 30'.format(self.safemode_ip1)).read()
                                logger.info(out)
                                if '30 received' in out:
                                    break
                            except Exception as err:
                                retries += 1
                                if retries < 20:
                                    logger.info("Firewall is not up after reboot, retrying")
                                    continue
                                else:
                                    Assertion.fail("Firewall is not up after reboot with maximum retries")
                        logger.info('Firewall is up')
                    else:
                        logger.info('The page is invisible after load new build.')
                else:
                    logger.info('Cannot find Browser button.')
            else:
                logger.info("Cannot find Upload Firmware button.")
                Assertion.fail("Cannot find Upload Firmware button in safemode UI")
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Load firmware in safemode failed")

    def login_fw_from_safemode_ui_gen8(self):
        try:
            logger.info("Check safmode status first")
            retries = 1
            while retries < 8:
                try:
                    logger.info('Sleep 30s for firewall enter safemode')
                    time.sleep(30)
                    self.ui_wrapper.get_browser()
                    rc1 = os.popen('ping {} -c 2'.format(self.safemode_ip1)).read()
                    logger.info(rc1)
                    if '100% packet loss' not in str(rc1):
                        logger.info('ping {} successfully'.format(self.safemode_ip1))
                        logger.info("Start login with {}".format(self.safemode_ip1))
                        self.ui_wrapper.go_to_url('https://{}/'.format(self.safemode_ip1))
                        time.sleep(5)
                        current_url = self.ui_wrapper.browser.current_url
                        logger.info("Current URL : " + str(current_url))
                        if 'login' in current_url:
                            break
                        else:
                            logger.info("Can ping {}, but cannot login via https.".format(self.safemode_ip1))
                            Assertion.fail("Can ping {}, but cannot login via https.".format(self.safemode_ip1))
                    else:
                        rc2 = os.popen('ping {} -c 2'.format(self.safemode_ip2)).read()
                        logger.info(rc2)
                        if '100% packet loss' not in str(rc2):
                            logger.info('ping {} successfully'.format(self.safemode_ip2))
                            logger.info("Start login with {}".format(self.safemode_ip2))
                            self.ui_wrapper.go_to_url('https://{}/'.format(self.safemode_ip2))
                            time.sleep(5)
                            current_url = self.ui_wrapper.browser.current_url
                            logger.info("Current URL : " + str(current_url))
                            if 'login' in current_url:
                                break
                            else:
                                logger.info("Can ping {}, but cannot login via https.".format(self.safemode_ip1))
                                Assertion.fail("Can ping {}, but cannot login via https.".format(self.safemode_ip1))
                except Exception as err:
                    retries += 1
                    if retries < 8:
                        logger.info("Safemode status is not ready.")
                        continue
                    else:
                        logger.info("Check safemode status with maximum retries")
                        Assertion.fail("Cannot access to FW VS MGMT port,Need to check it.")
            time.sleep(10)
            logger.info("Login fw in safemode from UI")
            logger.info("Enter Maintenance Key")
            try:
                for Key in self.MaintenanceKey_gen8:
                    logger.info(f"Trying Maintenance Key: {Key}")
                    self.ui_wrapper.set_text_field('xpath', "//input[@type='password' or @name='emailInput']", Key)
                    time.sleep(2)
                    logger.info("Click LOGIN")
                    self.ui_wrapper.click_element('xpath', '//div[contains(text(), "LOGIN")]')
                    time.sleep(3)
                    current_url = self.browser.current_url
                    logger.info(current_url)
                    logger.info(Key)
                    if 'login' not in current_url:
                        break
                    else:
                        logger.info("Cannot login safemode UI via this  Maintenance Key, Try another one...")
                logger.info('Login fw in safemode from UI successfully.')
                time.sleep(5) 
            except Exception as err:
                logger.error("Exception \t: " + str(err))
                Assertion.fail("No Maintenance Key for this dut, pls check again.") 
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Login fw in safemode from UI failed")

    def upload_fw_from_safemode_ui_gen8(self, restore_default=True):
        check_tag = False
        logger.info("Upload new build from safemode UI... ... ...")
        try:
            upload_path = '//span[text()="Upload Firmware"]'
            for i in range(10):
                logger.info(f'times {i+1} to click Upload Firmware...')
                logger.info("wait for 30s to make sure the browser is loading completely...")
                time.sleep(30)
                logger.info(f"Click Upload Image using path :{upload_path}")
                if self.ui_wrapper.does_element_exist_now('xpath', upload_path):
                    logger.info("Upload Firmware button is visible")
                    self.ui_wrapper.click_element('xpath', upload_path)
                    time.sleep(3)
                    check_tag = True
                    break
                else:
                    logger.info("Upload Firmware button is not visible")
            else:
                logger.info("Cannot find Upload Firmware button after 10 times.")

            if check_tag:
                logger.info("Check - if Browse button is visible")  
                browse_path = '//button[@type="button" and text()="Browse"]'
                logger.info(f"Browse button using path :{browse_path}")
                if self.ui_wrapper.does_element_exist_now('xpath', browse_path):
                    logger.info("Browse button is visible")
                    logger.info("Click - Browse")
                    try:
                        self.ui_wrapper.click_element('xpath',browse_path)
                    except Exception as err:
                        logger.error("Exception \t: " + str(err))
                        Assertion.fail("Click Browse button failed")
                    logger.info("The file that you want to upload is:" + self.file_path)
                    time.sleep(3)
                    self.pykey.type_string(self.file_path)
                    time.sleep(5)
                    self.pykey.tap_key(self.pykey.enter_key)
                    time.sleep(5)
                    logger.info("Click - Upload")
                    upload_path = '//div/button[@type="button" and text()="Upload"]'
                    logger.info(f"Upload button using path :{upload_path}")
                    self.ui_wrapper.click_element('xpath',upload_path)
                    time.sleep(5)
                    logger.info("Sleep 220s wait for the page reload.")
                    time.sleep(220)
                    logger.info("Check - if new firmware is loaded from UI")
                    if self.ui_wrapper.does_element_exist_now('xpath', '//span[contains(text(),"This is the uploaded firmware")]'):
                        logger.info("New firmware is loaded from UI successfully.")
                        logger.info("Prepare booting uploaded fw.")   
                        icon_reboot_path = '//div[contains(., "This is the uploaded firmware")]/ancestor::div[contains(@class, "sw-table-row")]//span[contains(@class, "icon-reboot")]'
                        logger.info(f"Reboot icon button using path :{icon_reboot_path}")                           
                        self.ui_wrapper.click_element('xpath',icon_reboot_path)
                        logger.info('Click Boot firmware with Current Configuration.')
                        time.sleep(10)
                        res = self.ui_wrapper.does_element_exist_now('xpath', '//div[contains(@class, "sw-dropdown-unit") and contains(., "with Default Configuration")]')
                        logger.info(res)
                        if restore_default:
                            Default_config_path = '//div[contains(@class, "sw-dropdown-unit") and contains(., "with Default Configuration")]'
                            logger.info(f"Default Configuration button using path :{Default_config_path}")
                            self.ui_wrapper.click_element('xpath', Default_config_path)
                        else:
                            current_config_path = '//div[contains(@class, "sw-dropdown-unit") and contains(., "with Current Configuration")]'
                            logger.info(f"Current Configuration button using path :{current_config_path}")
                            self.ui_wrapper.click_element('xpath', current_config_path)
                        logger.info('Click OK.')
                        time.sleep(2)
                        self.ui_helper.submit_page()
                        logger.info('Sleep 600s wait for fw up.')
                        time.sleep(600)
                        logger.info('Close browser')
                        os.system('pkill firefox')
                        time.sleep(5)
                        retries = 1
                        while retries < 20:
                            try:
                                logger.info('Sleep 60s wait for fw up.')
                                time.sleep(60)
                                out = os.popen('ping {} -c 30'.format(self.safemode_ip1)).read()
                                logger.info(out)
                                if '30 received' in out:
                                    break
                            except Exception as err:
                                retries += 1
                                if retries < 20:
                                    logger.info("Firewall is not up after reboot, retrying")
                                    continue
                                else:
                                    Assertion.fail("Firewall is not up after reboot with maximum retries")
                        logger.info('Firewall is up')
                    else:
                        logger.info('The page is invisible after load new build.')
                else:
                    logger.info('Cannot find Browser button.')
            else:
                logger.info("Cannot find Upload Firmware button.")
                Assertion.fail("Cannot find Upload Firmware button in safemode UI")
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Load firmware in safemode failed")

