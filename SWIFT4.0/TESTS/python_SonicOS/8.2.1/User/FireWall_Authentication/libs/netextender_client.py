
from inputs.constants import *
from pytest_resources.common_require import *


class SSLVPNNetExtenderCLI:
    def __init__(self, hostname, username, password):
        # Define the VPN parameters
        self.hostname = hostname
        self.username = username
        self.password = password
        self.domain = sslvpn_login_domain

    # Install NetExtender client
    def install_nx_client(self):
        # Check if client is already installed and uninstall it
        if os.path.exists(nx_client_path + "\\NECLI.exe"):
            self.uninstall_nx_client()
        logger.info("Copying the installer file locally...")
        copy_cmd = 'powershell cp ' + nx_client_installer_path + nx_client_filename + ' ' + nx_download_path
        logger.info(copy_cmd)
        copy_output = os.system(copy_cmd)
        logger.info("Installing NetExtender Client...")
        install_cmd = nx_download_path + "\\" + nx_client_filename + " /S"
        logger.info(install_cmd)
        cmd_output = os.system(install_cmd)
        logger.info(cmd_output)
        time.sleep(30)
        if cmd_output == 0 and os.path.exists(nx_client_path + "\\NECLI.exe"):
            logger.info("NetExtender client installed successfully...")
            return True
        else:
            logger.info("NetExtender client installation failed...")
            return False

    # NextExtender client valid login
    def nx_valid_login(self):
        # Check if client is connected and disconnect if connected
        nx_status = self.nx_show_status()
        if nx_connection_status in nx_status:
            self.nx_disconnect()
        logger.info("Connecting to NetExtender client...")
        os.chdir(nx_client_path)
        logger.info(os.getcwd())
        logger.info(self.hostname)
        logger.info(self.username)
        logger.info(self.password)
        logger.info(self.domain)
        server = self.hostname + ':' + sslvpn_port
        cmd = 'NECLI connect -s ' + server + ' -u ' + self.username + ' -p ' + self.password + ' -d ' + self.domain
        logger.info(cmd)
        cmd_output = "Connected successfully."
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # accepting ssl certificate and checking status
        try:
            if process.stdin.writable():
                process.stdin.write(("Y" + '\n').encode(encoding='utf-8'))
                process.stdin.flush()

            if process.stdout.readable():
                response = process.stdout.read()
                response = response.decode(encoding='utf-8')
                logger.info(response)
                nx_status = self.nx_show_status()
                logger.info(nx_status)
                if (cmd_output in response) and (nx_connection_status in nx_status):
                    logger.info("NetExtender client login succeeded...")
                    return True
                else:
                    return False
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.error("NetExtender client login failed...")
            return False

    # NextExtender client invalid login
    def nx_invalid_login(self):
        # Check if client is connected and disconnect if connected
        nx_status = self.nx_show_status()
        if nx_connection_status in nx_status:
            self.nx_disconnect()
        logger.info("Connecting to NetExtender client...")
        os.chdir(nx_client_path)
        logger.info(os.getcwd())
        logger.info(self.hostname)
        logger.info(self.username)
        logger.info(self.password)
        logger.info(self.domain)
        server = self.hostname + ':' + sslvpn_port
        cmd = 'NECLI connect -s ' + server + ' -u ' + self.username + ' -p ' + self.password + ' -d ' + self.domain
        logger.info(cmd)
        error_message1 = "Error: Login failed - Incorrect username/password"
        error_message2 = "Error: authentication failed!"
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # accepting ssl certificate and checking status
        try:
            if process.stdin.writable():
                process.stdin.write(("Y" + '\n').encode(encoding='utf-8'))
                process.stdin.flush()

            if process.stdout.readable():
                response = process.stdout.read()
                response = response.decode(encoding='utf-8')
                logger.info(response)
                nx_status = self.nx_show_status()
                logger.info(nx_status)
                if (error_message1 in response or error_message2 in response) and (nx_disconnection_status in nx_status):
                    logger.info("NetExtender client login failed as expected...")
                    return True
                else:
                    return False
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.error("NetExtender login succeeded with invalid credentials...")
            return False

    # NextExtender client check connection/disconnection status
    def nx_show_status(self):
        os.chdir(nx_client_path)
        cmd = 'NECLI showstatus'
        logger.info(cmd)
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Read and return the output
        try:
            process.stdout.readable()
            output = process.stdout.read()
            output = output.decode(encoding='utf-8')
            logger.info(output)
            return output
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.error("Getting NetExtender client status failed...")
            return False

    # NextExtender client disconnection
    def nx_disconnect(self):
        os.chdir(nx_client_path)
        cmd = 'NECLI disconnect 10'
        logger.info(cmd)
        cmd_output = "Disconnected successfully."
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Verifying disconnection status
        try:
            if process.stdout.readable():
                response = process.stdout.read()
                response = response.decode(encoding='utf-8')
                logger.info(response)
                nx_status = self.nx_show_status()
                logger.info(nx_status)
                if (cmd_output in response) and (nx_disconnection_status in nx_status):
                    logger.info("NetExtender client disconnection succeeded...")
                    return True
                else:
                    return False
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.error("NetExtender client disconnection failed...")
            return False

    # Uninstall NetExtender client
    def uninstall_nx_client(self):
        logger.info("Uninstalling NetExtender client...")
        os.chdir(nx_client_path)
        uninstall_cmd = 'uninst.exe /S'
        logger.info(uninstall_cmd)
        cmd_output = os.system(uninstall_cmd)
        logger.info(cmd_output)
        time.sleep(30)
        if cmd_output == 0 and not(os.path.exists(nx_client_path + "\\NECLI.exe")):
            logger.info("NetExtender client uninstalled successfully...")
            return True
        else:
            logger.info("NetExtender client uninstallation failed...")
            return False

