# This file contains all constants(or environment variables) that are used across.
import os
import json

# FireWall details
fw_eth0_ip = '192.168.168.168'
fw_eth1_ip = "10.5.67.180"
corp_dns = "10.50.129.148"
ip_pool_start = "192.168.0.10"
ip_pool_end = "192.168.0.50"
fw_url = 'https://' + fw_eth0_ip
fw_username = "admin"
fw_password = "sonicwall"
fw_unpw_login_failure_message = "Incorrect name/password"

# List of admin groups, login methods and authentication methods
fw_administrator_groups = ["SonicWALL Administrators", "Guest Administrators", "Limited Administrators",
                           "SonicWALL Read-Only Admins", "System Administrators", "Cryptographic Administrators",
                           "Audit Administrators"]
login_methods = ["FireWall_Administration", "L2TP_VPN_Client", "SSL-VPN_Portal", "NetExtender_Client",
                 "Global_VPN_Client", "ULA"]
authentication_methods = ["Local", "LDAP", "RADIUS", "TACACS", "LDAP-Local", "RADIUS-Local", "TACACS-Local"]

# ULA
wan_resource_url = "https://www.bbc.com"

# Mail Server details
sv_web_mail_server = "mail.sonicwall.com"
sender_email_id = "sshetty@sonicwall.com"
recipient_email_list = ["sshetty@sonicwall.com", "pagarwal@sonicwall.com", "nishas@sonicwall.com", "ajee@sonicwall.com",
                        "pguddadahalli@sonicwall.com", "kskarkera@sonicwall.com", "shkumar@sonicwall.com"]


# mounted drive 10.5.64.10\logs
mount_logs_username = "root"
mount_logs_password = "password"
mount_logs_path = "\\\\10.5.64.10\\logs"
mount_logs_auth_hardening_path = mount_logs_path + "\\sonicos_auth_hardening"
mount_logs_cmdline = mount_logs_auth_hardening_path + "\\cmdline\\"
mount_logs_results = mount_logs_auth_hardening_path + "\\results\\"
mount_mail_results = mount_logs_auth_hardening_path + "\\mail\\"
mount_gvc_logs = mount_logs_auth_hardening_path + "\\gvc\\"

root_dir = os.sep.join(str(__file__).split(os.sep)[0:-4]) + os.sep
inputs_base_path = root_dir + r"/User/FireWall_Authentication/inputs/"
config_jsons_base_path = inputs_base_path + "config_json"
power_run_base_path = inputs_base_path + "power_run/"

# SSL-VPN Portal and NetExtender Client details
sslvpn_port = '4433'
sslvpn_portal_url = 'https://' + fw_eth1_ip + ':' + sslvpn_port
sslvpn_login_domain = "LocalDomain"
nx_connection_status = "Status: Connected"
nx_disconnection_status = "Status: Disconnected"
nx_client_filename = "NXSetupU-x64-10.2.339.exe"
nx_client_path = r'C:\Program Files (x86)\Sonicwall\SSL-VPN\NetExtender'
nx_client_installer_path = root_dir + r"/User/FireWall_Authentication/inputs/installers/sslvpn_nx_win/"
nx_download_path = r'C:\Users\Admin\Downloads'

# Global VPN Client details
gvc_preshared_secret_key = "sonicwall"
gvc_client_filename = "184-011921-00_REV_A_GVCSetup64.exe"
gvc_client_path = r'C:\Program Files\SonicWall\Global VPN Client'
gvc_client_installer_path = root_dir + r"/User/FireWall_Authentication/inputs/installers/global_vpn_client_win/"
gvc_download_path = r'C:\Users\Admin\Downloads'

# Local User Details

# reading local_user.json
local_user_file = open(config_jsons_base_path + r"/local_user.json", "r")
local_user_details = json.load(local_user_file)
local_user_file.close()

local_user_name = local_user_details['user']['local']['user'][0]['name']
local_user_password = local_user_details['user']['local']['user'][0]['password']

# LDAP User Details

# reading ldap_user.json
ldap_user_file = open(config_jsons_base_path + r"/ldap_user.json", "r")
ldap_user_details = json.load(ldap_user_file)
ldap_user_file.close()

ldap_user_name = ldap_user_details['user']['local']['user'][0]['name']
ldap_user_password = ldap_user_details['user']['local']['user'][0]['password']
ldap_user_domain = ldap_user_details['user']['local']['user'][0]['domain']

# RADIUS User Details

# reading radius_user.json
radius_user_file = open(config_jsons_base_path + r"/radius_user.json", "r")
radius_user_details = json.load(radius_user_file)
radius_user_file.close()

radius_user_name = radius_user_details['user']['local']['user'][0]['name']
radius_user_password = radius_user_details['user']['local']['user'][0]['password']
radius_user_domain = radius_user_details['user']['local']['user'][0]['domain']

# TACACS+ User Details

# reading tacacs_user.json
tacacs_user_file = open(config_jsons_base_path + r"/tacacs_user.json", "r")
tacacs_user_details = json.load(tacacs_user_file)
tacacs_user_file.close()

tacacs_user_name = tacacs_user_details['user']['local']['user'][0]['name']
tacacs_user_password = tacacs_user_details['user']['local']['user'][0]['password']
tacacs_user_domain = tacacs_user_details['user']['local']['user'][0]['domain']


# SMTP Sevrer Details

# reading smtp_server.json
smtp_server_file = open(config_jsons_base_path + r"/smtp_server.json", "r")
smtp_server_details = json.load(smtp_server_file)
smtp_server_file.close()

smtp_server_ip = smtp_server_details['SMTP_server']['server_ip']
smtp_username = smtp_server_details['SMTP_server']['username']
smtp_password = smtp_server_details['SMTP_server']['password']
smtp_port = smtp_server_details['SMTP_server']['port']
email_id = smtp_server_details['SMTP_server']['email_id']

