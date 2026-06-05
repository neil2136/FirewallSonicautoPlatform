from definition.settings import *


class TestConfigFW(Test):
    uuid = "NonTC"
    goto_teardown = True

    def test_01_Config_X0_ipv4(self):
        logger.info("config x0 ipv4 interface... ")
        rc = interface_obj.config_interface(**x0_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X0 IPv4 failed")

    def test_02_Config_X0_ipv6(self):
        logger.info("config x0 ipv6 interface... ")
        rc = interface_obj_v6.config_interface_ipv6(**x0_lan_ipv6_dict)
        Assertion.assert_equal(rc, True, "ERR: Configure X0 ipv6 failed!")

    def test_03_Config_X1_ipv4(self):
        logger.info("config x1 ipv4 interface... ")
        rc = interface_obj.config_interface(**x1_wan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    def test_04_Config_X1_ipv6(self):
        logger.info("config x1 ipv6 interface... ")
        rc = interface_obj_v6.config_interface_ipv6(**x1_wan_ipv6_dict)
        Assertion.assert_equal(rc, True, "ERR: Configure X1 ipv6 failed!")

    def test_05_Config_X3_ipv4(self):
        logger.info("config x3 ipv4 interface... ")
        rc = interface_obj.config_interface(**x3_wan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    def test_06_Config_X4_ipv4(self):
        logger.info("config x4 lan interface... ")
        rc = interface_obj.config_interface(**x4_lan_dict)
        Assertion.assert_equal(
            rc, True, "ERR: Config X4 lan interface failed")

    def test_07_enable_snmp(self):
        rc = False
        enRes = snmp_obj.enable_snmp()
        logger.info(f" Enable result is {enRes} ")
        logger.info(f"{' Check enable flag ':=^50}")
        checkres = snmp_obj.show_snmp()
        if 'snmp' in checkres.keys() and 'enable' in checkres['snmp'].keys():
            rc = True if checkres["snmp"]["enable"] else False
        Assertion.assert_equal(rc, True, "ERR: Enable snmp failed!")

    def test_08_enable_snmp(self):  
        rc = False
        config_json = {
        "snmp":{
        "enable":True,
        "get_community_name":"public",
        }
        }
        enRes = snmp_obj.configure_snmp(**config_json)
        logger.info(f" Enable result is {enRes} ")
        snmp3_disable = {'mandatory': False}
        snmp3Res = snmp_obj.snmp_advance_settings(**snmp3_disable)
        logger.info(f" snmp3 disable result is {snmp3Res} ")
        logger.info(f"{' Check enable flag ':=^50}")
        checkres = snmp_obj.show_snmp()
        if 'snmp' in checkres.keys() and 'enable' in checkres['snmp'].keys():
            rc = True if checkres["snmp"]["enable"] else False
        Assertion.assert_equal(rc, True, "ERR: Enable snmp failed!")

    def test_09_log_enable_icmp_drop(self):
        logger.info("config enable icmp drop log... ")
        rc = logsetting_obj.edit_event(event_id='38', **icmp_drop_setting_dict1)
        Assertion.assert_equal(
            rc, True, "ERR: enable icmp drop log failed")

    def test_10_enable_http_host_header_check(self):
        logger.info("config enable http host header check... ")
        http_host_header_check_json = {
                "firewall_domain_name": "",
                "idle_logout_time": 60,
                "inter_admin_messaging": {},
                "multiple_admin": False,
                "enhanced_audit_logging": False,
                "dashboard_as_starting_page": False,
                "tls_and_above": False,
                "out_of_band_management": False,
                "https_port": 443,
                "enforce_http_host_check": True,
                "admin": {
                    "name": "admin",
                    "one_time_password": {
                    },
                    "preempt_action": "goto-non-config",
                    "preempt_inactivity_timeout": 10
                },
                "password": {
                    "enforce_character_difference": False,
                    "minimum_length": 8,
                    "aging": {
                    },
                    "complexity": {
                    },
                    "uniqueness": {
                    },
                    "constraints_apply_to": {
                        "builtin_admin": True,
                        "full_admins": True,
                        "limited_admins": True,
                        "local_users": True,
                        "guest_admins": True,
                    }
                },
                "gms_management": {
                },
                "user_lockout": {
                    "enable": False,
                    "failures_rate": 5,
                    "failures_duration": 1,
                    "lockout_duration": 5
                 },
                "web_management": {
                    "allow_http": False,
                    "certificate": {'use_self_signed': True},
                    "cert_common_name": "192.168.168.168",
                    "client_certificate_check": False,
                    "default_table_size": 50,
                    "refresh_interval": 10,
                    "tooltip": {
                        "form_delay": 2000,
                        "button_delay": 3000,
                        "text_delay": 500
                    }
                },
                  "language_override": {
                    "english": True
                },
                "ssh": {
                    "port": 22
                }
            }
        rc = admin_obj.conf_admin(**http_host_header_check_json)
        logger.info(f"config enable http host header check...{rc} ")
        Assertion.assert_equal(rc, True, "ERR: enable http host header check failed!")

    @repeat_method(10)
    def test_11_Register_fw(self):
        time.sleep(20)
        rc = license_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")


