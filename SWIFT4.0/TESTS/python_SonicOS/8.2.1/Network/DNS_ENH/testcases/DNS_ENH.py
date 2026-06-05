from definition.global_v import *

dts_dict = {
    'TestDNSENH_01': 'GEN7-16603',
}
@skip_if_dts(dts_dict)
class TestDNSENH_01(Test):
    uuid = "SOSAIOT-TC-51377"
    description= show_testcase_info(Parameter.TESTPLAN, '4', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Config_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,

        }
        rc = interface_obj.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")
  
    def test_02_Test_DNS_Server_1(self):
        dns_1 = {
            "dns":{
                "server":{
                    "static":{
                        "primary": Parameter.VALID_DNS,
                        "secondary": Parameter.FAKE_DNS1,
                        "tertiary": Parameter.FAKE_DNS2,
                    }
                }
            }
        }
        rc = dns_obj.set_dns(**dns_1)
        Assertion.assert_equal(rc, True, "ERR: Set DNS1 failed")

    def test_03_Verify_dns_result(self):
        flag = False
        ret = system_obj.diag_dns_name_lookup(cmd = "nslookup baidu.com").split("\n")
        logger.info(ret)
        for r in ret:
            if re.search(r"DNS Server Used:\s*" + Parameter.VALID_DNS,r,re.I):
                flag = True
                break
        Assertion.assert_equal(flag, True, "ERR: Verify DNS1 failed")

    def test_04_Test_DNS_Server_2(self):
        dns_1 = {
            "dns":{
                "server":{
                    "static":{
                        "primary": Parameter.FAKE_DNS1,
                        "secondary": Parameter.VALID_DNS,
                        "tertiary": Parameter.FAKE_DNS2,
                    }
                }
            }
        }
        rc = dns_obj.set_dns(**dns_1)
        Assertion.assert_equal(rc, True, "ERR: Set DNS1 failed")

    def test_05_Verify_dns_result(self):
        flag = False
        ret = system_obj.diag_dns_name_lookup(cmd = "nslookup baidu.com").split("\n")
        logger.info(ret)
        for r in ret:
            if re.search(r"DNS Server Used:\s*" + Parameter.VALID_DNS,r,re.I):
                flag = True
                break
        Assertion.assert_equal(flag, True, "ERR: Verify DNS2 failed")

    def test_06_Test_DNS_Server_3(self):
        dns_1 = {
            "dns":{
                "server":{
                    "static":{
                        "primary": Parameter.FAKE_DNS1,
                        "secondary": Parameter.FAKE_DNS2,
                        "tertiary": Parameter.VALID_DNS,
                    }
                }
            }
        }
        rc = dns_obj.set_dns(**dns_1)
        Assertion.assert_equal(rc, True, "ERR: Set DNS1 failed")

    def test_07_Verify_dns_result(self):
        flag = False
        ret = system_obj.diag_dns_name_lookup(cmd = "nslookup baidu.com").split("\n")
        logger.info(ret)
        for r in ret:
            if re.search(r"DNS Server Used:\s*" + Parameter.VALID_DNS,r,re.I):
                flag = True
                break
        Assertion.assert_equal(flag, True, "ERR: Verify DNS3 failed")


#dts_dict = {
#    'TestDNSENH_02': 'GEN7-16597',
#}
#@skip_if_dts(dts_dict)
class TestDNSENH_02(Test):
    uuid = "SOSAIOT-TC-51380"
    description= show_testcase_info(Parameter.TESTPLAN, '7', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Config_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,

        }
        rc = interface_obj.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")
    def test_02_Test_DNS_Server_1(self):
        dns_1 = {
            "dns":{
                "server":{
                    "static":{
                        "primary": Parameter.VALID_DNS,
                        "secondary": Parameter.FAKE_DNS1,
                        "tertiary": Parameter.FAKE_DNS2,
                    }
                }
            }
        }
        rc = dns_obj.set_dns(**dns_1)
        Assertion.assert_equal(rc, True, "ERR: Set DNS1 failed")

    def test_03_Restart_DUT(self):
        ret = restart_obj.restart_now()
        Assertion.assert_equal(ret, True, "ERR: Restart DUT failed") 

    def test_04_Verify_DNS(self):
        flag = False
        rc = dns_obj.get_dns()
        if rc["dns"]["server"]["static"]["primary"] == Parameter.VALID_DNS and \
            rc["dns"]["server"]["static"]["secondary"] == Parameter.FAKE_DNS1 and \
            rc["dns"]["server"]["static"]["tertiary"] == Parameter.FAKE_DNS2:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Verify DNS failed") 
