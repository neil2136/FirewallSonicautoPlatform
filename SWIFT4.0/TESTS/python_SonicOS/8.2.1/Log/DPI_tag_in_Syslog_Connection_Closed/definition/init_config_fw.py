from definition.settings import *


class Test_Config_FW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_x1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ping': True,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'gateway': "12.12.1.1"
        }
        res = if_v4_api.config_interface(**x1_static)
        Assertion.assert_equal(res, True, 'ERR: config x1 failed')

    def test_02_configure_x2(self):
        x2_dict = {
            'if': 'x2',
            'zone': 'dmz',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        (rc1, msg1) = if_v4_api.config_interface(msg=True, **x2_dict)
        if rc1 is False:
            rc1 = True if 'Already exists' in str(msg1) else False
        Assertion.assert_equal(rc1, True, "ERR: Configure VLAN failed!")

    @repeat_method(5)
    def test_03_register_fw(self):
        time.sleep(10)
        res = license_cli.register("online")
        Assertion.assert_equal(res, True, "ERR: register fw failed")

    def test_04_add_syslog_ao(self):
        ao_param = {
            "object_type": "host",
            "name": "syslog_server",
            "zone": "LAN",
            "value": PC1_ETH2_IP,
        }
        (rc, msg) = ao_api.config_addressobject(msg=True, **ao_param)
        if rc is False:
            rc = True if 'Already exists' in str(msg) else False
        Assertion.assert_equal(
            rc, True, "ERR: Add syslog server address object failed")

    def test_05_configure_syslog_setting(self):
        time.sleep(5)
        syslog_para = {
            'facility': 'local_use_0',
            'format': 'default',
            'id': 'firewall',
            'override_s': 'off',
        }
        res, msg = syslog_api.edit_syslog_settings(syslog_para)
        logger.info(msg)
        Assertion.assert_equal(res, True, "ERR: Config syslog setting failed")

    def test_06_add_syslog_server(self):
        time.sleep(3)
        syslog_para = {
            'name': 'syslog_server',
            'profile': 0
        }
        (rc, msg) = syslog_api.add_syslog_server(msg=True, **syslog_para)
        if rc is False:
            rc = True if 'Already exists' in str(msg) else False
        Assertion.assert_equal(rc, True, "ERR: Add syslog server failed")

    def test_07_set_log(self):
        flag = []
        for logsetting in logsetting_list:
            logsetres = log_settings_api.edit_event(event_id=logsetting["log"]["event"][0]["id"], **logsetting)
            logger.info(f'{logsetting["log"]["event"][0]["name"]}:{logsetres}')
            flag.append(logsetres)
        Assertion.assert_equal(all(flag), True, "ERR: set arp timeout failed")

    def test_08_disable_content_filtering_service(self):
        cfs_settings_dict = {'enable': False}
        output = content_filter_api.edit_cfs_setting(**cfs_settings_dict)
        Assertion.assert_equal(
            output, True, "ERR: enable Content Filtering Service failed")
