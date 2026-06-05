#!/usr/bin/env python3
import sys
import os
import subprocess
import shutil
import re
import time
import xml.etree.ElementTree as ET
import requests
from runner.settings import logger
from util.openstack import Openstack
from utm import Firewall
from modules.UI7.rompack_ui_wrapper import Browser

def ensure_python_package(pkg_name, import_name=None):
    module_name = import_name
    try:
        __import__(module_name)
    except ModuleNotFoundError:
        logger.info(f"[INFO] Installing Python package {pkg_name}…")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg_name])
        __import__(module_name)

ensure_python_package("PyUserInput", "pykeyboard")
ensure_python_package("pyvirtualdisplay", "pyvirtualdisplay")

from pymouse import PyMouse
from pykeyboard import PyKeyboard
from pyvirtualdisplay import Display

def detect_linux_family():
    """
    Read /etc/os-release to distinguish 'debian' vs 'rhel' families.
    Returns 'debian', 'rhel', or None.
    """
    try:
        with open("/etc/os-release") as f:
            data = f.read().lower()
        if "id_like" in data and "rhel" in data:
            return "rhel"
        if "id_like" in data and "debian" in data:
            return "debian"
        # fallback by ID
        if "centos" in data or "rhel" in data or "fedora" in data:
            return "rhel"
        if "ubuntu" in data or "debian" in data:
            return "debian"
    except FileNotFoundError:
        pass
    return None

def ensure_system_package(binary_name, pkg_name=None):
    """
    If `binary_name` is missing, install `pkg_name` (or binary_name) via the
    distro's package manager (apt-get or yum).
    """
    if shutil.which(binary_name):
        return

    family = detect_linux_family()
    pkg = pkg_name or binary_name
    if family == "debian":
        installer = ["sudo", "apt-get", "update"], ["sudo", "apt-get", "install", "-y", pkg]
    elif family == "rhel":
        # on CentOS7 use yum; on newer RHEL/Fedora you could switch to dnf
        installer = ["sudo", "yum", "install", "-y", pkg],
    else:
        raise RuntimeError(f"Cannot detect package manager for installing {pkg}")

    logger.info(f"[INFO] Installing system package {pkg} with { 'yum' if family=='rhel' else 'apt-get' }…")
    # run each command in sequence
    for cmd in installer:
        subprocess.check_call(cmd)

ensure_system_package("Xvfb", "xorg-x11-server-Xvfb")

display = Display(visible=0, size=(1920, 1080), backend='xvfb')
display.start()
os.environ["DISPLAY"] = f":{display.display}"
logger.info(f"Virtual display started on DISPLAY={os.environ['DISPLAY']}")

safemode_ip1 = '192.168.168.168'
safemode_ip2 = '192.168.1.254'
pykey = PyKeyboard()


class UploadRompack():
    def __init__(self, rompack_version, test_bed):
        self.rom_url = rompack_version
        self.version = rompack_version.split('/')[-2]
        self.test_bed = test_bed
        self.console_ip = ''
        self.console_port = ''
        self.maintenance_key = ''
        self.ui_wrapper = Browser()
        self.os_host = 'osservices-sj.eng.sonicwall.com'
        self.topologies_json= 'http://' + self.os_host + '/topologies/' + self.test_bed + '.xml'
        self.rom_file_dir = '/tmp'
        self.rom_save_path = ''
        self.get_console_info()
        self.fw_console = Firewall('192.168.168.168', console_ip=self.console_ip, console_port=self.console_port,
                              user='admin', password='password', supported_config_mode='cli-console')

    def get_console_info(self):
        logger.info('Get console ip and port.')
        if self.test_bed:
            logger.info('---- This is ' + self.test_bed + ' -----')
            ostack = Openstack(self.test_bed)
            console_info = ostack.get_console_info()
            if console_info and len(console_info) >= 2:
                self.console_ip = console_info[0]
                self.console_port = console_info[1]
            else:
                logger.error('console_info is invalid.')
        else:
            out = os.popen('hostname').read()
            hostname = out.split('-')[0]
            if hostname:
                logger.info('------------ ' + hostname + '------------')
                ostack = Openstack(hostname)
                console_info = ostack.get_console_info()
                if console_info and len(console_info) >= 2:
                    self.console_ip = console_info[0]
                    self.console_port = console_info[1]
                else:
                    logger.error('console_info is invalid.')
            else:
                logger.error('hostname is empty.')
        logger.info('The console server is : ' + str(self.console_ip))
        logger.info('The console port is :   ' + str(self.console_port))

    def enable_ssh(self):
        logger.info('enable SSH on X0 interface.')
        commands = ['configure', 'interface x0', 'management ssh', 'commit', 'end', 'exit']
        (rc,output) = self.fw_console.do_cli_commands(commands,1)
        time.sleep(5)
        return rc, output

    def enter_safe_mode(self):
        commands = ['safemode']
        (rc, output) = self.fw_console.do_cli_commands(commands, 1)
        time.sleep(30)
        return rc, output
    
    def is_safemode(self):
        commands = [' ']
        (rc, output) = self.fw_console.do_cli_commands(commands, 1)
        if 'Restart SonicWall' in output:
            logger.info('Firewall is in safemode.')
            return True
        else:
            logger.info('Firewall is not in safemode.')
            return False

    def compare_ver(self):
        fw_cli = Firewall('192.168.168.168', user='admin', password='password',
                          supported_config_mode='cli-ssh')
        commands = ['show status']
        rc, status = fw_cli.do_cli_commands(commands, 1)
        pattern = re.compile(r'ROM Version.*?(\d+\.\d+\.\d+\.\d+)', re.I)
        match = pattern.search(status)
        if match:
            rom_ver = match.group(1)
            if rom_ver == self.version:
                logger.info('Rompack has the same version as uploaded. omit uploading.')
                return False
            else:
                logger.info('Rompack has different version with uploaded. Prepare uploading.')
                return True

    def get_maintenance_key(self):
        url = self.topologies_json
        ostack = Openstack(self.test_bed)
        response = ostack.get_url(url)
        if not response:
            logger.error(f'Fail to get {url} topo info.')
            return
        try:
            root = ET.fromstring(response)
            serial_elem = root.find(".//serial-number")
            if serial_elem is not None and serial_elem.text:
                serial_number = serial_elem.text
                if '-' in serial_number:
                    self.maintenance_key = serial_number.split('-')[1]
                elif '_' in serial_number:
                    self.maintenance_key = serial_number.split('_')[1]
                logger.info('The maintenance key is: ' + self.maintenance_key)
            else:
                logger.error('serial-number not found in XML.')
        except Exception as e:
            logger.error(f'Fail to get maintenance key. error:{e}')

    def get_rom_sig_file(self, rom_url):
        response = requests.get(rom_url, stream=True)
        pattern = r'(?<=//)[^/]+(/.*)'
        match = re.search(pattern, rom_url)
        try:
            if not match:
                logger.error(f"URL pattern not matched: {rom_url}")
                return
            extracted_path = match.group(1)
            rom_save_path = self.rom_file_dir + extracted_path
            dir_name = os.path.dirname(rom_save_path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            if response.status_code == 200:
                with open(rom_save_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                self.rom_save_path = rom_save_path
                logger.info(f"rom sig has been downloaded in: {rom_save_path}")
            else:
                logger.error(f"Download failed: {response.status_code}")
        except Exception as e:
            logger.error(f"Download failed. error:{e}")

    def login_safemode_from_ui_linux(self):
        try:
            logger.info("Check safemode status first")
            retries = 1
            while retries < 8:
                try:
                    logger.info('Sleep 30s for firewall enter safemode')
                    time.sleep(30)
                    self.ui_wrapper.get_browser()
                    rc1 = os.popen('ping {} -c 2'.format(safemode_ip1)).read()
                    logger.info(rc1)
                    if '100% packet loss' not in str(rc1):
                        logger.info('ping {} successfully'.format(safemode_ip1))
                        logger.info("Start login with {}".format(safemode_ip1))
                        self.ui_wrapper.go_to_url('https://{}/'.format(safemode_ip1))
                        time.sleep(5)
                        current_url = self.ui_wrapper.browser.current_url
                        logger.info("Current URL : " + str(current_url))
                        if 'login' in current_url:
                            break
                        else:
                            logger.info("Can ping {}, but cannot login via https.".format(safemode_ip1))
                    else:
                        rc2 = os.popen('ping {} -c 2'.format(safemode_ip2)).read()
                        logger.info(rc2)
                        if '100% packet loss' not in str(rc2):
                            logger.info('ping {} successfully'.format(safemode_ip2))
                            logger.info("Start login with {}".format(safemode_ip2))
                            self.ui_wrapper.go_to_url('https://{}/'.format(safemode_ip2))
                            time.sleep(5)
                            current_url = self.ui_wrapper.browser.current_url
                            logger.info("Current URL : " + str(current_url))
                            if 'login' in current_url:
                                break
                            else:
                                logger.info("Can ping {}, but cannot login via https.".format(safemode_ip2))
                except Exception as err:
                    retries += 1
                    if retries < 8:
                        logger.info("Safemode status is not ready.")
                        continue
                    else:
                        logger.info("Check safemode status with maximum retries")
            time.sleep(10)
            logger.info("Login fw in safemode from UI")
            logger.info("Enter Maintenance Key")
            self.get_maintenance_key()
            try:
                self.ui_wrapper.set_text_field('xpath',
                "//input[@type='password' and @name='identifier' and @placeholder='Enter Maintenance Key...']",
                                               self.maintenance_key)
                time.sleep(2)
                logger.info("Click LOGIN")
                self.ui_wrapper.click_element('xpath', '//div[contains(text(), "LOGIN")]')
                time.sleep(3)
                current_url = self.ui_wrapper.browser.current_url
                logger.info(current_url)
                if 'webfront/scx/firmware' in current_url:
                    logger.info('Login fw in safemode from UI successfully.')
                    time.sleep(5)
                else:
                    logger.info("Cannot login safemode UI via this  Maintenance Key, Try another one...")
            except Exception as err:
                logger.error("Exception \t: " + str(err))
        except Exception as err:
            logger.error("Exception \t: " + str(err))

    def upgrade_rom(self):
        try:
            out = os.popen('ping 192.168.168.168 -c 2').read()
            if '100% packet loss' not in out:
                logger.info("Fw is up for test")
                ssh_status = self.enable_ssh()
                if not ssh_status[0]:
                    return False, "Enable SSH failed: " + ssh_status[1]
                logger.info("SSH is enabled successfully.")
                if self.is_safemode():
                    logger.info("Firewall is in safemode, restart")

                if self.compare_ver():
                    safemode_status = self.enter_safe_mode()[0]
                    if not safemode_status:
                        return False, "Enter safemode failed."
                    self.login_safemode_from_ui_linux()
                    time.sleep(35)
                    logger.info("Click Boot ROM")
                    self.ui_wrapper.click_element('xpath', '//span[contains(text(), "Boot ROM")]')
                    time.sleep(4)
                    logger.info("Click Upload ROMpack")
                    self.ui_wrapper.wait_for_element_and_click('xpath','//span[contains(@class, "icon-upload")]')
                    time.sleep(4)
                    logger.info("upload rompack sig file")
                    self.get_rom_sig_file(self.rom_url)
                    logger.info("The file that you want to upload is:" + self.rom_save_path)
                    self.ui_wrapper.wait_for_element_and_click('xpath',
                                                               "//button[@class='sw-button sw-button--light' and text()='Browse']")
                    time.sleep(3)
                    pykey.type_string(self.rom_save_path)
                    time.sleep(5)
                    pykey.tap_key(pykey.enter_key)
                    time.sleep(5)
                    logger.info("Click - Upload")
                    self.ui_wrapper.wait_for_element_and_click('xpath',"//button[contains(@class, 'sw-button') and text()='Upload']")
                    time.sleep(5)
                    logger.info("Sleep 30s wait for the page reload.")
                    time.sleep(80)
                    logger.info("Check - if new ROMpack is loaded from UI")
                    if self.ui_wrapper.does_element_exist_now('xpath',
                                                              '//p[text()="Uploaded Boot ROM Version"]/following-sibling::span'):
                        logger.info("New firmware is loaded from UI successfully.")
                        logger.info("Prepare booting uploaded fw.")
                        boot_button = self.ui_wrapper.browser.find_elements('xpath', '//span[contains(@class, "icon-reboot")]')
                        logger.info(len(boot_button))
                        time.sleep(2)
                        boot_button[-1].click()
                        time.sleep(2)
                        logger.info('Click OK.')
                        self.ui_wrapper.click_element('xpath', '//button[text()="OK"]')
                        time.sleep(30)
                        logger.info('Click Reboot Now.')
                        self.ui_wrapper.wait_for_element_and_click('xpath',
                                                                   "//button[contains(@class, 'sw-button sw-button--light') and text()='Reboot Now']")
                        logger.info('Sleep 240s wait for fw up.')
                        time.sleep(240)
                        logger.info('Close ui_wrapper')
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
                                    logger.info("Firewall is not up after reboot, retrying")
                                    continue
                                else:
                                    return False, "Firewall is not up after factory reboot with maximum retries"
                        logger.info('Firewall is up')
                        logger.info("After booting in safemode, the new version is:" + self.version)
                        return True, "Load ROM in safemode successfully"
                    else:
                        return False, "ROM sig upload failed."
                else:
                    return True, "ROM version is same, skip."
            else:
                return False, "At first, it can't ping 192.168.168.168."
        except Exception as err:
                logger.error("Exception \t: " + str(err))
                return False, "Load ROM in safemode failed"
        finally:
            try:
                display.stop()
                logger.info("Virtual display stopped.")
                if self.is_safemode():
                    logger.info("Firewall is in safemode, restart it.")
            except Exception as e:
                logger.error(f"Error stopping virtual display: {e}")

if __name__ == "__main__":
    rompack_version = 'http://10.200.0.100/rompack/gen8/TZ280/Rompack/7.1.0.13/7.1.0.13-dev-rompack.sig'
    test_bed = 'VTB519'
    ul = UploadRompack(rompack_version, test_bed)
    ul.upgrade_rom()