from definition.settings import *


class nontc_config(Test):
    uuid = 'NonTC'
    
    def test_01_add_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'localuser',
            'userpassword': 'S0nic@uto'
        }
        user_local.local_user(**user_json)
        resp = user_local.show_local_users()
        Assertion.assert_regular(json.dumps(resp), '"name": "localuser"', 'ERR: Creation of local user failed')

    def test_02_configure_ftp_logging(self):
        ftp_log_config = {
            'ftp': {
                'server': '10.10.10.10',
                'login': 'ftp_admin',
                'password': 'ftp_password'
            }
        }
        packetmonitorapi.conf_packmon(**ftp_log_config)
        resp = packetmonitorapi.show_packmon_setting()
        Assertion.assert_regular(json.dumps(resp), '"server": "10.10.10.10"', 'ERR: Config FTP Logging server failed')

    def test_03_add_guest_account(self):
        guest_account_json = {
            'action': 'add',
            'accountname': 'localguestuser',
            'password': 'S0nic@uto'
        }
        guest_local.user_guest_account(**guest_account_json)
        resp = guest_local.show_user_guest_account()
        Assertion.assert_regular(json.dumps(resp), '"name": "localguestuser"', 'ERR: Creation of guest account failed')

    def test_04_configure_mail_server_advanced(self):
        mail_server_dict = {
            'smtp_authentication': True,
            'user_name': 'smtp_admin',
            'password': 'smtp_password'
        }
        resp = logautomationapi.cfg_mail_server(**mail_server_dict)
        Assertion.assert_equal(resp, True, "ERR: Config mail server advanced failed")

    def test_05_set_x2_pppoe(self):
        x2_pppoe = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'pppoe',
            'pppoe_user': 'pppoe_admin',
            'pppoe_passwd': 'pppoe_password',
            'pppoe_service': '',
            'pppoe_schedule': 'always_on',
            'pppoe_dynamic': True,
            'pppoe_inactivity': 0,
            'pppoe_lcp_echo_packets': False,
            'pppoe_reconnect': 0
        }
        rc = interface.config_interface(**x2_pppoe)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to PPPoE failed")

    def test_06_add_ddns_profile(self):
        ddns_dyn_profile = {
            'version': 'ipv4',
            'profile_name': 'DDNS Profile',
            'enable': True,
            'use_online': True,
            'provider': 'dyn',
            'user_name': 'ddns_admin',
            'password': 'ddns_password',
            'domain': 'ddnsprofile.com',
            'service_type': 'dynamic',
            'bound_to': {
                'any': True
            },
            'online_settings': {
                'detect': True
            },
            'offline_settings': {
                'do_nothing': True
            }
        }
        ddnsapi.add_ddns_profile(**ddns_dyn_profile)
        rc = ddnsapi.show_ddns_profiles_ipv4()
        Assertion.assert_regular(json.dumps(rc), '"profile_name": "DDNS Profile"', "ERR: Config DDNS Profile failed")


# def check_string_with_context(file_path, target_string, prev_string, next_string):
#     try:
#         with open(file_path, 'r') as file:
#             previous_line = None
#             current_line = None
#             next_line = None
#             for line in file:
#                 previous_line = current_line
#                 current_line = next_line
#                 next_line = line.strip()
#                 if current_line and target_string in current_line:
#                     logger.info(f"previous_line = {previous_line}")
#                     logger.info(f"current_line = {current_line}")
#                     logger.info(f"next_line = {next_line}")
#                     if previous_line == prev_string and next_line == next_string:
#                         return True
#         return False
#     except FileNotFoundError:
#         print(f"Error: The file '{file_path}' does not exist.")
#         return False

def check_string_with_context(file_path, target_string, prev_string, next_string):
    try:
        with open(file_path, 'r') as file:
            lines = [l.strip() for l in file.readlines()]
        for i, line in enumerate(lines):
            if target_string in line:
                prev_ok = True
                next_ok = True
                if prev_string:
                    prev_ok = (
                        (i-1 >= 0 and prev_string in lines[i-1]) or
                        (i-2 >= 0 and prev_string in lines[i-2]))
                if next_string:
                    next_ok = (
                        (i+1 < len(lines) and next_string in lines[i+1]) or
                        (i+2 < len(lines) and next_string in lines[i+2]))
                if prev_ok and next_ok:
                    logger.info("Found target with context:")
                    if i-2 >= 0:
                        logger.info(f"  [-2] {lines[i-2]}")
                    if i-1 >= 0:
                        logger.info(f"  [-1] {lines[i-1]}")
                    logger.info(f"  [ 0] {lines[i]}")
                    if i+1 < len(lines):
                        logger.info(f"  [+1] {lines[i+1]}")
                    if i+2 < len(lines):
                        logger.info(f"  [+2] {lines[i+2]}")
                    return True
        return False
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        return False

class Check_Encrypt_Local_Username_Present_TSR(Test):
    uuid = "SOSAIOT-TC-74977"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508947')

    def test_01_enable_encryption_username_tsr_options(self):
        tsr_options = {
                "user_name": False
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_encrypted(self):
        resp = diagnostic.download_tsr()
        local_user_uuid = user_local.get_local_user_uuid("localuser")
        file_path = '/tmp/techSupport'
        search_line = '1,  ******(user name is not displayed)'
        prev_line = 'Local Users:'
        next_line = f'UUID:                  {local_user_uuid}'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_Unencrypt_Local_Username_Present_TSR(Test):
    uuid = "SOSAIOT-TC-74978"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508948')

    def test_01_disable_encryption_username_tsr_options(self):
        tsr_options = {           
                "user_name": True
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_unencrypted(self):
        resp = diagnostic.download_tsr()
        local_user_uuid = user_local.get_local_user_uuid("localuser")
        file_path = '/tmp/techSupport'
        search_line = '1,  localuser'
        prev_line = 'Local Users:'
        next_line = f'UUID:                  {local_user_uuid}'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_FTP_Encrypt_Username_Encrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-74979"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508949')

    def test_01_enable_encryption_username_enable_encryption_sensistive_keys_tsr_options(self):
        tsr_options = {
                "user_name": False,
                "sensitive_keys": False
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_encrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'ftpServerIpAddress[10.10.10.10] backupFtpServerIpAddress[0.0.0.0] ftpLoginId[********]'
        prev_line = 'patchedHeader[0] numberBytesCapture[1520] exclude[0x0] inter[0]'
        next_line = 'ftpPassword[********] ftpDirectory[captures]'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_encrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'ftpPassword[********] ftpDirectory[captures]'
        prev_line = 'ftpServerIpAddress[10.10.10.10] backupFtpServerIpAddress[0.0.0.0] ftpLoginId[********]'
        next_line = 'mcast[0] iph[0] reass[0] frag[0] mirror[0] crypto[0]'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_FTP_Unencrypt_Username_Encrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-74980"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508950')

    def test_01_disable_encryption_username_enable_encryption_sensistive_keys_tsr_options(self):
        tsr_options = {
                "user_name": True,
                "sensitive_keys": False
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_unencrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'ftpServerIpAddress[10.10.10.10] backupFtpServerIpAddress[0.0.0.0] ftpLoginId[ftp_admin]'
        prev_line = 'patchedHeader[0] numberBytesCapture[1520] exclude[0x0] inter[0]'
        next_line = 'ftpPassword[********] ftpDirectory[captures]'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_encrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'ftpPassword[********] ftpDirectory[captures]'
        prev_line = 'ftpServerIpAddress[10.10.10.10] backupFtpServerIpAddress[0.0.0.0] ftpLoginId[ftp_admin]'
        next_line = 'mcast[0] iph[0] reass[0] frag[0] mirror[0] crypto[0]'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_FTP_Encrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-74981"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508951')

    def test_01_enable_encryption_username_disable_encryption_sensistive_keys_tsr_options(self):
        tsr_options = {
                "user_name": False,
                "sensitive_keys": True
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_encrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'ftpServerIpAddress[10.10.10.10] backupFtpServerIpAddress[0.0.0.0] ftpLoginId[********]'
        prev_line = 'patchedHeader[0] numberBytesCapture[1520] exclude[0x0] inter[0]'
        next_line = 'ftpPassword[ftp_password] ftpDirectory[captures]'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_unencrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'ftpPassword[ftp_password] ftpDirectory[captures]'
        prev_line = 'ftpServerIpAddress[10.10.10.10] backupFtpServerIpAddress[0.0.0.0] ftpLoginId[********]'
        next_line = 'mcast[0] iph[0] reass[0] frag[0] mirror[0] crypto[0]'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_FTP_Unencrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-74982"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508952')

    def test_01_disable_encryption_username_disable_encryption_sensistive_keys_tsr_options(self):
        tsr_options = {
                "user_name": True,
                "sensitive_keys": True
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_unencrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'ftpServerIpAddress[10.10.10.10] backupFtpServerIpAddress[0.0.0.0] ftpLoginId[ftp_admin]'
        prev_line = 'patchedHeader[0] numberBytesCapture[1520] exclude[0x0] inter[0]'
        next_line = 'ftpPassword[ftp_password] ftpDirectory[captures]'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_unencrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'ftpPassword[ftp_password] ftpDirectory[captures]'
        prev_line = 'ftpServerIpAddress[10.10.10.10] backupFtpServerIpAddress[0.0.0.0] ftpLoginId[ftp_admin]'
        next_line = 'mcast[0] iph[0] reass[0] frag[0] mirror[0] crypto[0]'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_Encrypt_Guest_Username_Present_TSR(Test):
    uuid = "SOSAIOT-TC-74983"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508953')

    def test_01_enable_encryption_username_tsr_options(self):
        tsr_options = {
                "user_name": False
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_encrypted(self):
        resp = diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = '1,   (guest name is not displayed)     Privileges:            0x408: Bypass-Filter=no, Admin: (Full=no, Ltd=no, Guest=no, Rd-Only=no)'
        prev_line = 'Guest Accounts:'
        next_line = '- Guest Properties:'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_Unencrypt_Guest_Username_Present_TSR(Test):
    uuid = "SOSAIOT-TC-74984"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508954')

    def test_01_disable_encryption_username_tsr_options(self):
        tsr_options = {
                "user_name": True
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_unencrypted(self):
        resp = diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = '1,  localguestuser'
        prev_line = 'Guest Accounts:'
        next_line = 'Privileges:            0x408: Bypass-Filter=no, Admin: (Full=no, Ltd=no, Guest=no, Rd-Only=no)'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_SMTP_Encrypt_Username_Encrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-74998"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508968')

    def test_01_enable_encryption_username_enable_encryption_sensistive_keys_tsr_options(self):
        tsr_options = {
                "user_name": False,
                "sensitive_keys": False
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_encrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'

        search_key = 'SMTP Auth User'
        prev_key = 'Enable SMTP Authentication'
        next_key = 'SMTP Auth Password'

        res = check_string_with_context(file_path, search_key, prev_key, next_key)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_encrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'SMTP Auth Password                : *******************'
        prev_line = 'SMTP Auth User                    : *******************'
        next_line = 'Log email:'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_SMTP_Encrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-74999"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508969')

    def test_01_enable_encryption_username_disable_encryption_sensistive_keys_tsr_options(self):
        tsr_options = {
                "user_name": False,
                "sensitive_keys": True
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_encrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'SMTP Auth User                    : *******************'
        prev_line = 'Enable SMTP Authentication        : Enabled'
        next_line = 'SMTP Auth Password                : smtp_password'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_unencrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'SMTP Auth Password                : smtp_password'
        prev_line = 'SMTP Auth User                    : *******************'
        next_line = 'Log email:'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_SMTP_Unencrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75000"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508970')

    def test_01_disable_encryption_username_disable_encryption_sensistive_keys_tsr_options(self):
        tsr_options = {
                "user_name": True,
                "sensitive_keys": True
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_unencrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'SMTP Auth User                    : smtp_admin'
        prev_line = 'Enable SMTP Authentication        : Enabled'
        next_line = 'SMTP Auth Password                : smtp_password'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_unencrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'SMTP Auth Password                : smtp_password'
        prev_line = 'SMTP Auth User                    : smtp_admin'
        next_line = 'Log email:'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_PPPoE_Encrypt_Username_Encrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75001"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508971')

    def test_01_enable_encryption_username_enable_encryption_sensistive_keys_tsr_options(self):
        tsr_options = {
                "user_name": False,
                "sensitive_keys": False
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_encrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'User Name                                       : *******************'
        prev_line = 'Schedule                                        : Always On (0)'
        next_line = 'Password                                        : *******************'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_encrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'Password                                        : *******************'
        prev_line = 'User Name                                       : *******************'
        next_line = 'Service Name:                                   :'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_PPPoE_Unencrypt_Username_Encrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75002"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508972')

    def test_01_disable_encryption_username_enable_encryption_sensistive_keys_tsr_options(self):
        tsr_options = {
                "user_name": True,
                "sensitive_keys": False
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_unencrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'User Name                                       : pppoe_admin'
        prev_line = 'Schedule                                        : Always On (0)'
        next_line = 'Password                                        : *******************'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_encrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'Password                                        : *******************'
        prev_line = 'User Name                                       : pppoe_admin'
        next_line = 'Service Name:                                   :'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_PPPoE_Encrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75003"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508973')

    def test_01_enable_encryption_username_disable_encryption_sensistive_keys_tsr_options(self):
        tsr_options = {
                "user_name": False,
                "sensitive_keys": True
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_encrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'User Name                                       : *******************'
        prev_line = 'Schedule                                        : Always On (0)'
        next_line = 'Password                                        : <Password exists>'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_unencrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'Password                                        : <Password exists>'
        prev_line = 'User Name                                       : *******************'
        next_line = 'Service Name:                                   :'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_PPPoE_Unencrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75004"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508974')

    def test_01_disable_encryption_username_disable_encryption_sensistive_keys_tsr_options(self):
        tsr_options = {
                "user_name": True,
                "sensitive_keys": True
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_unencrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'User Name                                       : pppoe_admin'
        prev_line = 'Schedule                                        : Always On (0)'
        next_line = 'Password                                        : <Password exists>'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_unencrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'Password                                        : <Password exists>'
        prev_line = 'User Name                                       : pppoe_admin'
        next_line = 'Service Name:                                   :'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_DDNS_Encrypt_Username_Encrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75022"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508995')

    def test_01_enable_encryption_username_enable_encryption_sensistive_keys_tsr_options(self):
        tsr_options = {
                "user_name": False,
                "sensitive_keys": False
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_encrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'User Name: *******'
        prev_line = 'Provider Name: dyn.com'
        next_line = 'IPversion is : IPV4'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_encrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'Password: has been set'
        prev_line = 'IPversion is : IPV4'
        next_line = 'Domain Name: ddnsprofile.com'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_DDNS_Unencrypt_Username_Encrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75023"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508996')

    def test_01_disable_encryption_username_enable_encryption_sensistive_keys_tsr_options(self):
        tsr_options = {
                "user_name": True,
                "sensitive_keys": False
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_unencrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'User Name: ddns_admin'
        prev_line = 'Provider Name: dyn.com'
        next_line = 'IPversion is : IPV4'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_encrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'Password: has been set'
        prev_line = 'IPversion is : IPV4'
        next_line = 'Domain Name: ddnsprofile.com'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_DDNS_Encrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75024"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508997')

    def test_01_enable_encryption_username_disable_encryption_sensistive_keys_tsr_options(self):
        tsr_options = {
                "user_name": False,
                "sensitive_keys": True
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_encrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'User Name: *******'
        prev_line = 'Provider Name: dyn.com'
        next_line = 'IPversion is : IPV4'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_unencrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'Password: has been set'
        prev_line = 'IPversion is : IPV4'
        next_line = 'Domain Name: ddnsprofile.com'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_DDNS_Unencrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75025"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508998')

    def test_01_disable_encryption_username_disable_encryption_sensistive_keys_tsr_options(self):
        tsr_options = {
                "user_name": True,
                "sensitive_keys": True
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_unencrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'User Name: ddns_admin'
        prev_line = 'Provider Name: dyn.com'
        next_line = 'IPversion is : IPV4'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_unencrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'Password: has been set'
        prev_line = 'IPversion is : IPV4'
        next_line = 'Domain Name: ddnsprofile.com'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")
