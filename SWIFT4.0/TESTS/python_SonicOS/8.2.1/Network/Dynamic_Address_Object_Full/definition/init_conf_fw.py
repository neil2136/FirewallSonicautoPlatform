from unittest.result import failfast
from definition.settings import *


class TestInit_FW(Test):
    uuid = 'NonTC'

    def test_01_config_interface_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway':  Parameter.X1_GW,
            'dns1':  Parameter.X1_DNS1,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interfaceapi.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_config_interface_X2(self):
        x2_static = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interfaceapi.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_03_set_dns_server(self):
        rc = dnsapi.set_dns(**dns_dict)
        Assertion.assert_equal(rc, True, "ERR: Set DNS failed")

    def test_04_set_arp_timeout(self):
        setres = arpapi.arp_setting(timeout=2)
        Assertion.assert_equal(setres, True, "ERR: set arp timeout failed")

    def test_05_set_log(self):
        flag = []
        for logsetting in logsetting_list:
            logsetres = logsettingsapi.edit_event(
                event_id=logsetting["log"]["event"][0]["id"], **logsetting)
            logger.info(f'{logsetting["log"]["event"][0]["name"]}:{logsetres}')
            flag.append(logsetres)
        Assertion.assert_equal(all(flag), True, "ERR: set arp timeout failed")

    def test_06_disable_dns_proxy_cache(self):
        disCache = {
            'dns_cache': False
        }
        rc = dnsproxyapi.config_dnsproxy(**disCache)
        Assertion.assert_equal(rc, True, "ERR: Enable DNS Proxy Cache failed")
