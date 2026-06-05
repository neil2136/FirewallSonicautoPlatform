import pyautogui

from libs.common_lib import *
from pytest_resources.common_require import *


class GlobalVPNClient:
    def __init__(self, hostname, username, password):
        # Define the VPN parameters
        self.hostname = hostname
        self.username = username
        self.password = password

    # Install Global VPN Client
    def install_gvc_client(self):
        if os.path.exists(gvc_client_path + "\\SWGVC.exe"):
            logger.info("Global VPN Client already installed, skipping installation....")
            return True
        else:
            pyautogui.hotkey("win", "d")
            logger.info("Copying the installer file locally...")
            copy_cmd = 'powershell cp ' + gvc_client_installer_path + gvc_client_filename + ' ' + gvc_download_path
            logger.info(copy_cmd)
            copy_output = os.system(copy_cmd)
            logger.info("Installing Global VPN Client...")
            install_cmd = gvc_download_path + "\\" + gvc_client_filename
            logger.info(install_cmd)
            os.startfile(install_cmd)
            time.sleep(10)
            pyautogui.press("enter")
            time.sleep(2)
            pyautogui.press("tab")
            time.sleep(2)
            pyautogui.press("right")
            time.sleep(2)
            pyautogui.press("enter")
            time.sleep(2)
            pyautogui.press("enter")
            time.sleep(2)
            pyautogui.press("enter")
            time.sleep(30)
            pyautogui.press("enter")
            time.sleep(10)
            pyautogui.moveTo(300, 190)
            pyautogui.click()
            pyautogui.press("enter")
            time.sleep(2)
            pyautogui.write(fw_eth1_ip)
            time.sleep(2)
            pyautogui.press("enter")
            time.sleep(2)
            pyautogui.press("enter")
            time.sleep(4)
            os.chdir(gvc_client_path)
            enable_cmd = 'SWGVC /E ' + self.hostname + ' /U ' + self.username + ' /P ' + self.password
            logger.info(enable_cmd)
            os.system(enable_cmd)
            time.sleep(2)
            pyautogui.write(gvc_preshared_secret_key)
            time.sleep(2)
            pyautogui.press("tab")
            time.sleep(2)
            pyautogui.press("tab")
            time.sleep(2)
            pyautogui.press("enter")
            time.sleep(4)
            pyautogui.write(self.username)
            time.sleep(2)
            pyautogui.press("tab")
            time.sleep(2)
            pyautogui.write(self.password)
            time.sleep(2)
            pyautogui.press("tab")
            time.sleep(2)
            pyautogui.press("enter")
            time.sleep(10)
            self.disable_gvc_connection()
            pyautogui.hotkey("win", "d")
            return True

    # Enable Global VPN Client
    def enable_gvc_connection(self):
        os.chdir(gvc_client_path)
        enable_cmd = 'SWGVC /E ' + self.hostname + ' /U ' + self.username + ' /P ' + self.password
        logger.info(enable_cmd)
        try:
            process = subprocess.check_output(enable_cmd, timeout=30)
            logger.info(process)
        except:
            pass

    # Disable Global VPN Client
    def disable_gvc_connection(self):
        os.chdir(gvc_client_path)
        disable_cmd = 'SWGVC /D ' + self.hostname
        logger.info(disable_cmd)
        try:
            process = subprocess.check_output(disable_cmd, timeout=10)
            logger.info(process)
        except:
            pass

    # Export and read client logs for authentication status
    def export_gvc_logs(self):
        com_obj = CommonLib()
        com_obj.kill_process(process_name='SWGVC.exe')
        log_file_name = os.path.join(mount_gvc_logs, "GVCAuto.log")
        logger.info("Opening " + log_file_name + " file for writing test case results")
        open(log_file_name, 'w', newline='')
        os.chdir(gvc_client_path)
        export_cmd = 'SWGVC /A ' + log_file_name
        logger.info(export_cmd)
        try:
            process = subprocess.check_output(export_cmd, timeout=10)
            logger.info(process)
        except:
            pass

    # Read exported logs and verify the expected log message in the log file
    def read_exported_gvc_logs(self, expected_log_message, expected_log_message2=None):
        log_file_name = os.path.join(mount_gvc_logs, "GVCAuto.log")
        data = open(log_file_name, 'rb').read()
        content = data.decode('utf-16')
        logger.info(content)
        if expected_log_message2:
            if expected_log_message in content or expected_log_message2 in content:
                logger.info("The text '" + expected_log_message + "' or '" + expected_log_message2 +
                            "' found in GVC Logs...")
                return True
            else:
                logger.info("The text '" + expected_log_message + "' or '" + expected_log_message2 +
                            "' not found in GVC Logs...")
                return False
        else:
            if expected_log_message in content:
                logger.info("The text '" + expected_log_message + "' found in GVC Logs...")
                return True
            else:
                logger.info("The text '" + expected_log_message + "' not found in GVC Logs...")
                return False

    # Clear exported GVC Logs
    def clear_gvc_logs(self):
        os.chdir(results_dir_path)
        log_file_name = os.path.join(mount_gvc_logs, "GVCAuto.log")
        with open(log_file_name, 'r+') as file:
            file.truncate(0)
        logger.info("Cleared GVC logs successfully....")

    # Global VPN Client login
    def gvc_login(self, expected_failure=False):
        self.enable_gvc_connection()
        if expected_failure:
            response = self.read_exported_gvc_logs(expected_log_message="User authentication has failed.",
                                                   expected_log_message2="Failed to decrypt buffer.")
            logger.info(response)
            if response is True:
                logger.info("GVC login failed as expected...")
            else:
                logger.info("GVC Login didn't fail as expected...")
        else:
            response = self.read_exported_gvc_logs(expected_log_message="User authentication has succeeded.")
            logger.info(response)
            if response is True:
                logger.info("GVC login is successful..")
            else:
                logger.info("GVC login failed for valid credentials...")
        self.clear_gvc_logs()
        self.disable_gvc_connection()
        return response

    # Uninstall Global VPN Client
    # def uninstall_gvc_client(self):
    #     pyautogui.hotkey("win", "d")
    #     logger.info("Uninstalling Global VPN Client...")
    #     uninstall_cmd = gvc_client_installer_path + gvc_client_filename
    #     logger.info(uninstall_cmd)
    #     os.startfile(uninstall_cmd)
    #     time.sleep(10)
    #     pyautogui.press("tab")
    #     time.sleep(2)
    #     pyautogui.press("down")
    #     time.sleep(2)
    #     pyautogui.press("enter")
    #     time.sleep(25)
    #     pyautogui.moveTo(750, 300)
    #     pyautogui.click()
    #     time.sleep(2)
    #     pyautogui.press("space")
    #     time.sleep(2)
    #     pyautogui.press("enter")
    #     time.sleep(60)
    #     pyautogui.press("enter")
    #     time.sleep(5)
    #     pyautogui.press("tab")
    #     time.sleep(2)
    #     pyautogui.press("enter")
    #     time.sleep(10)

