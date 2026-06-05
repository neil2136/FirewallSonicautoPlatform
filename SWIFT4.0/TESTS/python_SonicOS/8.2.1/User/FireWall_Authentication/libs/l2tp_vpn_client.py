import subprocess
from pytest_resources.common_require import *
from inputs.constants import *


class L2TPVPNClient:
    def __init__(self, hostname, username, password):
        # Define the VPN parameters
        self.hostname = hostname
        self.username = username
        self.password = password
        self.vpn_name = "MyL2TPVPN"
        self.pre_shared_key = gvc_preshared_secret_key
        self.l2tp_vpn_success_text = "Successfully connected to MyL2TPVPN."
        self.l2tp_vpn_failure_text = "The remote connection was denied because the user name and password combination" \
                                     " you provided is not recognized, or the selected authentication protocol is not" \
                                     " permitted on the remote access server."
        self.l2tp_vpn_failure_text2 = "The connection was terminated because the remote computer did not respond" \
                                      " in a timely manner."

    # Function to run a PowerShell command
    def run_powershell_command(self, command):
        output = subprocess.run(["powershell.exe", "-Command", command], capture_output=True, text=True)
        logger.info(output)
        command_output = str(output)
        return command_output

    # Add the L2TP VPN connection
    def add_l2tp_vpn_connection(self):
        logger.info("Adding L2TP VPN connection....")
        add_vpn_command = "Add-VpnConnection -Name " + self.vpn_name + " -ServerAddress " + self.hostname + \
                          " -TunnelType L2TP -L2tpPsk " + self.pre_shared_key + \
                          " -AuthenticationMethod Pap -EncryptionLevel Optional -PassThru -Force"
        logger.info(add_vpn_command)
        # Run the command to add the VPN connection
        self.run_powershell_command(command=add_vpn_command)
        logger.info("Added L2TP VPN connection successfully....")

    # Connect to the L2TP VPN Connection
    def connect_l2tp_vpn_connection(self, expected_failure=False):
        connect_vpn_command = "rasdial " + self.vpn_name + " " + self.username + " " + self.password
        logger.info(connect_vpn_command)
        # Run the command to connect to the VPN
        connection_status = self.run_powershell_command(command=connect_vpn_command)
        if expected_failure:
            if self.l2tp_vpn_failure_text in connection_status or self.l2tp_vpn_failure_text2 in connection_status:
                logger.info("L2TP VPN connection failed as expected...")
                return True
            else:
                logger.info("L2TP VPN connection succeeded with invalid credentials or expected output not found...")
                return False
        else:
            if self.l2tp_vpn_success_text in connection_status:
                logger.info("L2TP VPN connection is successful...")
                return True
            else:
                logger.info("L2TP VPN connection failed even with valid credentials...")
                return False

    # Connect to the L2TP VPN Connection
    def disconnect_l2tp_vpn_connection(self):
        disconnect_vpn_command = "rasdial " + self.vpn_name + " /DISCONNECT"
        logger.info(disconnect_vpn_command)
        # Run the command to disconnect the VPN
        self.run_powershell_command(command=disconnect_vpn_command)
        logger.info("Disconnected L2TP VPN connection...")

    # Remove the L2TP VPN Connection
    def remove_l2tp_vpn_connection(self):
        logger.info("Removing L2TP VPN connection....")
        remove_vpn_command = "Remove-VpnConnection -Name " + self.vpn_name + " -Force"
        logger.info(remove_vpn_command)
        # Run the command to remove the VPN connection
        self.run_powershell_command(command=remove_vpn_command)
        logger.info("Removed L2TP VPN connection successfully...")

