from definition.settings import *


class TestConfigTB1(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_00_01_set_FW_time(self):
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "10:00:39",
                "date": "2022:01:01",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = LTimeObj.set_time(**time_json)
        Assertion.assert_equal(rc, True, 'Add CA cert Failed.')

    def test_00_02_Add_DUT_AddObj(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc = LAddrOBJ.config_addressobject(**remote_l)
        logger.info('-'*10+'Add AO for rm DUT'+'-'*10)
        rc &= RAddrOBJ.config_addressobject(**remote_r)
        Assertion.assert_equal(rc, True, 'Add AO for DUT and RDUT Failed.')

    def test_00_03_add_acl(self):
        rule1 = copy.deepcopy(rule_opt)
        rule2 = copy.deepcopy(rule_opt)
        rule1['name'] = 'VPN_to_LAN'
        rule1['from'] = 'VPN'
        rule1['to']   = 'LAN'
        rule2['name'] = 'LAN_to_VPN'
        rule2['from'] = 'LAN'
        rule2['to']   = 'VPN'
        res1 = Raccess_rule_obj.config_accessrule(msg=True,**rule1)
        res2 = Raccess_rule_obj.config_accessrule(msg=True,**rule2)
        if (res1[0] or 'Already exists' in str(res1[1])) and (res2[0] or 'Already exists' in str(res2[1])):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: add access rule between VPN to LAN in DUT2 failed")

    # @repeat_method(5)
    # def test_04_register_fw(self):
    #     logger.info(" {} ".center(20, '-').format('Register firewall'))
    #     time.sleep(10)
    #     x1_static = {
    #         'if': 'X1',
    #         'zone': 'WAN',
    #         'mode': 'static',
    #         'ip': '12.12.1.200',
    #         'netmask': '255.255.255.0',
    #         'gateway': '12.12.1.1',
    #         'dns1': Params.G_DNS1,
    #         'dns2': Params.G_DNS2,
    #         'mgmt_https': True,
    #         'mgmt_ssh': True,
    #         'mgmt_snmp': True,
    #         'mgmt_ping': True,
    #         'user_https':True,
    #     }
    #     rc = interfacev4api.config_interface(**x1_static)
    #     rc = license_obj.register("online")
    #     Assertion.assert_equal(rc, True, "ERR: register fw failed")

