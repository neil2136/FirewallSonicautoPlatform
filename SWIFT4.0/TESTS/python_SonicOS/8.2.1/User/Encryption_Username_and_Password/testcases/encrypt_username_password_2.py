from definition.settings import *


class nontc_config(Test):
    uuid = 'NonTC'
    
    def test_01_add_dynamic_group(self):
        add_dynamic_group = {
            "name": "ftpdynamicgroup",
            "periodic_download": "5-minutes",
            "protocol": "ftp",
            "fqdn": False,
            "server": "10.20.30.40",
            "login": "deag_admin",
            "password": "deag_password",
            "directory": "/var/ftp/ForEDAG",
            "filename": "ftpfile.txt"
        }
        res = edagapi.add_dynamic_group_by_build_json(**add_dynamic_group)
        Assertion.assert_equal(res, True, "ERR: Failed to add Dynamic Group")
    
    def test_02_add_ntp_server(self):
        resp = status_api.show_status()
        model = resp['model']

        if model == 'TZ 80':
            # Custom NTP not supported in TZ80 GEN8-3187
            logger.info("TZ 80 does not support this [GEN8-3187].")
            Assertion.assert_equal(True, True, "ERR: Failed.")
        else:
            ntp_dict = {
                "name": "192.168.168.171",
                "md5": {
                    "key_number": 1,
                    "password": "ntp_password",
                    "trust_key_no": 1
                }
            }
            res = time_api.add_ntp_server(**ntp_dict)
            Assertion.assert_equal(res, True, 'ERR: Failed to add NTP Server')
    
    def test_03_enable_rip_on_X0(self):
        rip_dict = {
            'interface': 'X0',
            'mode': 'send_and_receive',
            'receive': '2',
            'send': '2',
            'password': 'rip_password'
        }
        res = dyrouteapi.set_rip(**rip_dict)
        Assertion.assert_equal(res, True, "ERR: Failed To enable RIP on X0 interface")

    def test_04_enable_ospf_on_X0(self):
        ospf_dict = {
            'interface': 'X0',
            'mode': 'enable',
            'hello_interval': '5',
            'dead_interval': '20',
            'cost': 'on',
            'auth': 'simple password',
            'password': 'ospf_pas'
        }
        res = dyrouteapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(res, True, "ERR: Failed to enable OSPF on X0 interface")
    
    def test_05_add_vpn_policy(self):
        vpn = {
            'type': 'tunnel_interface',
            'name': 'vpn_interface',
            'enable': True,
            'auth_mode': 'shared_secret',
            'pri_gate': '101.1.1.101',
            'secret': 'ipsec_password',
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4'
        }
        rc = vpnObj.add_vpn_policy(**vpn)
        Assertion.assert_equal(rc, True, "ERR: Failed to add VPN Policy")
    
    def test_06_configure_ftp_logging(self):
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
    
    def test_07_add_object_encryptserver(self):
        address_object = {
            "name": 'encryptserver',
            "zone": 'LAN',
            "object_type": 'host',
            "value": '10.103.12.254'
        }
        ret = address_obj.config_addressobject(**address_object)
        Assertion.assert_equal(ret, True, "ERR: Failed to configure Address Object")

    def test_08_config_dmz_zone_external_guest_authentication(self):
        edit_zone_object = {
            "zones": [{
                "name": "DMZ",
                "guest_services": {
                    "enable": True,
                    "external_auth": {
                        "enable": True,
                        "client_redirect": "http",
                        "web_server_1": {
                            "name": "encryptserver",
                            "protocol": "http",
                            "port": 80
                        },
                        "auth_pages": {
                            "web_server_1": {
                                "login": "encrypt_json/default.aspx",
                                "expiration": "encrypt_json/default.aspx?rc=1",
                                "timeout": "encrypt_json/default.aspx?rc=2",
                                "max_sessions": "encrypt_json/default.aspx?rc=3",
                                "traffic_exceeded": "encrypt_json/default.aspx?rc=4"
                            },				
                        },
                        "message_auth": {
                            "enable": True,
                            "method": "sha1",
                            "shared_secret": "external_password",
                            "confirm_secret": "external_password"
                        }
                    }
                }
            }]
        }
        rc = zone_obj.edit_zone_object('DMZ',**edit_zone_object)
        Assertion.assert_equal(rc, True, "ERR: Failed to configure External Guest Authentication for DMZ Zone")


def check_string_with_context(file_path, target_string, prev_string, next_string):
    try:
        with open(file_path, 'r') as file:
            previous_line = None
            current_line = None
            next_line = None
            for line in file:
                previous_line = current_line
                current_line = next_line
                next_line = line.strip()
                if current_line and target_string in current_line:
                    logger.info(f"previous_line = {previous_line}")
                    logger.info(f"current_line = {current_line}")
                    logger.info(f"next_line = {next_line}")
                    if previous_line == prev_string and next_line == next_string:
                        return True
        return False
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        return False


def check_string_not_in_file(file_path, search_string):
    with open(file_path, 'r') as file:
        contents = file.read()
        if search_string not in contents:
            return True
        else:
            return False


class Check_GMSserver_Encrypt_Username_Encrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75012"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508982')

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
        search_line = 'GMSFlow Server fw name...................**************'
        prev_line = 'GMSFlow Server 2 max flows.................200000'
        next_line = 'GMSFlow Server passphrase................**************'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_encrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'GMSFlow Server passphrase................**************'
        prev_line = 'GMSFlow Server fw name...................**************'
        next_line = 'GMSFlow Server auto sync.................TRUE'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_GMSserver_Unencrypt_Username_Encrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75013"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508983')

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
        search_line = 'GMSFlow Server fw name...................My SonicWall'
        prev_line = 'GMSFlow Server 2 max flows.................200000'
        next_line = 'GMSFlow Server passphrase................**************'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_encrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'GMSFlow Server passphrase................**************'
        prev_line = 'GMSFlow Server fw name...................My SonicWall'
        next_line = 'GMSFlow Server auto sync.................TRUE'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_GMSserver_Encrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75014"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508984')

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
        search_line = 'GMSFlow Server fw name...................**************'
        prev_line = 'GMSFlow Server 2 max flows.................200000'
        next_line = 'GMSFlow Server passphrase................password'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_unencrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'GMSFlow Server passphrase................password'
        prev_line = 'GMSFlow Server fw name...................**************'
        next_line = 'GMSFlow Server auto sync.................TRUE'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_GMSserver_Unencrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75015"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508985')

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
        search_line = 'GMSFlow Server fw name...................My SonicWall'
        prev_line = 'GMSFlow Server 2 max flows.................200000'
        next_line = 'GMSFlow Server passphrase................password'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_unencrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'GMSFlow Server passphrase................password'
        prev_line = 'GMSFlow Server fw name...................My SonicWall'
        next_line = 'GMSFlow Server auto sync.................TRUE'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_Encrypt_External_Guest_Auth_Shared_Secret_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75016"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508989')

    def test_01_enable_encryption_password_tsr_options(self):
        tsr_options = {
                "sensitive_keys": False
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_password_encrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'Shared Secret = ******'
        prev_line = 'Type          = 1'
        next_line = 'External Web Server:'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_Unencrypt_External_Guest_Auth_Shared_Secret_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75017"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508990')

    def test_01_disable_encryption_password_tsr_options(self):
        tsr_options = {
                "sensitive_keys": True
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_password_unencrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'Shared Secret = external_password'
        prev_line = 'Type          = 1'
        next_line = 'External Web Server:'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_Dynamic_External_Objects_Encrypt_Username_Encrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75026"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508999')

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
        search_line = 'userName:********'
        prev_line = 'dirPath:/var/ftp/ForEDAG'
        next_line = 'password:********'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_encrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'password:********'
        prev_line = 'userName:********'
        next_line = 'httpUserName:'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_Dynamic_External_Objects_Unencrypt_Username_Encrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75027"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1509000')

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
        search_line = 'userName:deag_admin'
        prev_line = 'dirPath:/var/ftp/ForEDAG'
        next_line = 'password:********'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_encrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'password:********'
        prev_line = 'userName:deag_admin'
        next_line = 'httpUserName:'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_Dynamic_External_Objects_Encrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75028"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1509001')

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
        search_line = 'userName:********'
        prev_line = 'dirPath:/var/ftp/ForEDAG'
        next_line = 'password:deag_password'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_unencrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'password:deag_password'
        prev_line = 'userName:********'
        next_line = 'httpUserName:'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_Dynamic_External_Objects_Unencrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75029"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1509002')

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
        search_line = 'userName:deag_admin'
        prev_line = 'dirPath:/var/ftp/ForEDAG'
        next_line = 'password:deag_password'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_unencrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'password:deag_password'
        prev_line = 'userName:deag_admin'
        next_line = 'httpUserName:'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_Encrypt_NTP_Password_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75037"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1509010')

    def test_01_enable_encryption_password_tsr_options(self):
        tsr_options = {
                "sensitive_keys": False
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_password_encrypted(self):
        resp = status_api.show_status()
        model = resp['model']

        if model == 'TZ 80':
            # Custom NTP not supported in TZ80 GEN8-3187
            logger.info("TZ 80 does not support this testcase [GEN8-3187].")
            Assertion.assert_equal(True, True, "ERR: Failed.")
        else:
            diagnostic.download_tsr()
            file_path = '/tmp/techSupport'
            search_string = 'Password          : *******'
            # Since the next line after the "search_string" is not consistent, so using an alternative way to verify NTP Password is encrypted
            # Moreover, the occurrence of this "search_string" is only one time (only for NTP configuration), so this method verifies the requirement
            res = check_string_not_in_file(file_path, search_string)
            Assertion.assert_equal(res, False, "ERR: Unable to find required data")


class Check_Unencrypt_NTP_Password_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75038"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1509011')

    def test_01_disable_encryption_password_tsr_options(self):
        tsr_options = {
                "sensitive_keys": True
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_password_unencrypted(self):
        resp = status_api.show_status()
        model = resp['model']

        if model == 'TZ 80':
            # Custom NTP not supported in TZ80 GEN8-3187
            logger.info("TZ 80 does not support this testcase [GEN8-3187].")
            Assertion.assert_equal(True, True, "ERR: Failed.")
        else:
            diagnostic.download_tsr()
            file_path = '/tmp/techSupport'
            search_string = 'Password          : ntp_password'
            # Since the next line after the "search_string" is not consistent, so using an alternative way to verify NTP Password is unencrypted
            # Moreover, the occurrence of this "search_string" is only one time (only for NTP configuration), so this method verifies the requirement
            res = check_string_not_in_file(file_path, search_string)
            Assertion.assert_equal(res, False, "ERR: Unable to find required data")


class Check_Encrypt_RIP_Password_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75039"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1509012')

    def test_01_enable_encryption_password_tsr_options(self):
        tsr_options = {
                "sensitive_keys": False
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_password_encrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        # Since the passwords in RIP are never encrypted, hence we are storing plain password for RIP in TSR, even if Sensitive Keys are excluded
        # Reference JIRA: GEN7-50801
        search_line = 'Password                          : rip_password'
        prev_line = 'Use Password                        : on'
        next_line = ''
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_Unencrypt_RIP_Password_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75040"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1509013')

    def test_01_disable_encryption_password_tsr_options(self):
        tsr_options = {
                "sensitive_keys": True
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_password_unencrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'Password                          : rip_password'
        prev_line = 'Use Password                        : on'
        next_line = ''
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_Encrypt_OSPF_Password_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75041"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1509014')

    def test_01_enable_encryption_password_tsr_options(self):
        tsr_options = {
                "sensitive_keys": False
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_password_encrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'Password                          : ******'
        prev_line = 'Authentication                      : Simple Password'
        next_line = 'OSPF Area                           : 112'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_Unencrypt_OSPF_Password_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75042"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1509015')

    def test_01_disable_encryption_password_tsr_options(self):
        tsr_options = {
                "sensitive_keys": True
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_password_unencrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'Password                          : ospf_pas'
        prev_line = 'Authentication                      : Simple Password'
        next_line = 'OSPF Area                           : 112'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_Encrypt_VPN_Tunnel_Not_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75043"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1509016')

    def test_01_enable_encryption_password_tsr_options(self):
        tsr_options = {
                "sensitive_keys": False
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_password_encrypted_not_present(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_string = 'Pre-shared Key len    :'
        # If sensitive keys are excluded, the "Pre-shared Key len" field itself will not be there in TSR
        res = check_string_not_in_file(file_path, search_string)
        Assertion.assert_equal(res, True, "ERR: Found the 'Pre-shared Key len' even though Sensitive Keys are excluded")


class Check_Unencrypt_VPN_Tunnel_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75044"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1509017')

    def test_01_disable_encryption_password_tsr_options(self):
        tsr_options = {
                "sensitive_keys": True
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_password_unencrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'Pre-shared Key len    : 14, value=ipsec_password'
        prev_line = 'IPsec Secondary gw    : (0.0.0.0)'
        next_line = 'IKE Local Id          : ID_IPV4_ADDR'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_EXP_Contains_Encrypted_Username_Password(Test):
    uuid = "SOSAIOT-TC-75045"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1509018')

    def test_01_enable_encrypt_username_password_config_file(self):
        diag_json = {
            "stream": "encUsernamePassword=on"
        }
        response = diag.config_raw_api(**diag_json)
        Assertion.assert_equal(response, True, "ERR: Failed to enable Encrypt Username and Password of Confguration File")
    
    def test_02_export_config(self):
        logger.info('Exporting exp file')
        res = settingapi.export_setting_exp()
        Assertion.assert_equal(res, True, "ERR: export exp file failed")
    
    def test_03_convert_exp_to_txt(self):
        file_path = 'test.exp'
        cmd = ["cd /tmp",
               rf"base64 -d -i {file_path} | sed 's/&/\n/g' > fw_config.txt"]
        localhost.send_commands(cmd)

    def test_04_check_username_encrypted(self):
        file_path = '/tmp/fw_config.txt'
        search_line = 'pktCapTraceFtpLoginId_0=5,'
        res = False
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith(search_line):
                    res = True
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_05_check_password_encrypted(self):
        file_path = '/tmp/fw_config.txt'
        search_line = 'pktCapTraceFtpPassword_0=5,'
        res = False
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith(search_line):
                    res = True
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Import_EXP_Supported_Firmware_Displays_Previous_Config(Test):
    uuid = "SOSAIOT-TC-75046"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1509020')

    def test_01_add_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'localuser',
            'userpassword': 'S0nic@uto'
        }
        user_local.local_user(**user_json)
        resp = user_local.show_local_users()
        Assertion.assert_regular(json.dumps(resp), '"name": "localuser"', 'ERR: Creation of local user failed')
    
    def test_02_enable_encrypt_username_password_config_file(self):
        diag_json = {
            "stream": "encUsernamePassword=on"
        }
        response = diag.config_raw_api(**diag_json)
        Assertion.assert_equal(response, True, "ERR: Failed to enable Encrypt Username and Password of Confguration File")
    
    def test_03_export_config(self):
        logger.info('Exporting EXP file')
        res = settingapi.export_setting_exp()
        Assertion.assert_equal(res, True, "ERR: Export EXP file failed")
    
    def test_04_edit_local_user(self):
        resp = user_local.get_local_user_uuid('localuser')
        user_json = {
            "uuid": resp,
            "username": "changeduser",
            "userpassword": "S0nic@uto"
        }
        user_local.edit_local_user_by_uuid(**user_json)
        resp = user_local.show_local_user_by_uuid(resp)
        Assertion.assert_regular(json.dumps(resp), '"name": "changeduser"', 'ERR: Failed to update local user')

    def test_05_disable_encrypt_username_password_config_file(self):
        diag_json = {
            "stream": "encUsernamePassword="
        }
        response = diag.config_raw_api(**diag_json)
        Assertion.assert_equal(response, True, "ERR: Failed to enable Encrypt Username and Password of Confguration File")

    def test_06_import_encrypted_config(self):
        logger.info('Importing EXP file')
        file_path = '/tmp/test.exp'
        res = settingapi.import_setting_exp(file_path)
        Assertion.assert_equal(res, True, "ERR: Import EXP file failed")

    def test_07_check_old_username(self):
        resp = user_local.show_local_users()
        Assertion.assert_regular(json.dumps(resp), '"name": "localuser"', 'ERR: Creation of local user failed')
        Assertion.assert_not_regular(json.dumps(resp), '"name": "changeduser"', 'ERR: Creation of local user failed')
