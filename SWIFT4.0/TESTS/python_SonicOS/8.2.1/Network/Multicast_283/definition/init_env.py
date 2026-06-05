from definition.settings import *

class  TestInitConfig(Test):
    uuid = 'NonTC'

    def test_01_Add_Address_Objects(self):
        rc = ao_api.config_addressobject(**multicast_obj)
        Assertion.assert_equal(rc, True, "ERR: Add multicast AO failed.")

    def test_02_Enable_Multicast(self):
        multicast_conf = {
            'multicast': True,
            'require_igmp_membership': True,
            'timeout': 1,
            'reception_name': multicast_obj["name"],
        }
        rc = multicast_api.config_multicast(**multicast_conf)
        Assertion.assert_equal(rc, True, "ERR: Config multicast failed.")

    def test_03_Enable_Multicast_on_X0(self):
        logger.info("Enable X0 multicast")
        rc = interface_api.config_interface(**x0_static)
        Assertion.assert_equal(rc, True, "ERR: Enable X0 multicast failed")

    def test_04_Config_X1(self):
        logger.info("config x1 interface... ")
        rc = interface_api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_05_Config_X2(self):
        logger.info("config x2 interface... ")
        rc = interface_api.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_06_Enable_Accessrules(self):
        rc = True
        show_accessrule = {
            'version': 'ipv4',
            'from': 'WAN',
            'to': 'MULTICAST',
        }
        out_wan = accessrule_cli.show_access_rules(**show_accessrule)
        show_accessrule = {
            'version': 'ipv4',
            'from': 'DMZ',
            'to': 'MULTICAST',
        }
        out_dmz = accessrule_cli.show_access_rules(**show_accessrule)
        # # # process WAN to MULTICAST rules
        wan_arr = out_wan.split('access-rule ipv4')
        for item in wan_arr:
            rule_dict = {
                'from': 'WAN',
                'to': 'MULTICAST',
                'action': 'deny',
                'action_new': 'allow',
            }
            if 'action deny' in item:
                out = re.search(r'service (\w+)\s?(\w+)?', item, re.I|re.S)
                if out:
                    if out.group(1) == 'group':
                        rule_dict['service_group'] = out.group(2)
                rc &= accessrule_cli.edit_access_rule(**rule_dict)
        # # # process DMZ to MULTICAST rules
        dmz_arr = out_dmz.split('access-rule ipv4')
        for item in dmz_arr:
            rule_dict = {
                'version': 'ipv4',
                'from': 'DMZ',
                'to': 'MULTICAST',
                'action': 'deny',
                'action_new': 'allow',
            }
            if 'action deny' in item:
                out = re.search(r'service (\w+)\s?(\w+)?', item, re.I|re.S)
                if out:
                    if out.group(1) == 'group':
                        rule_dict['service_group'] = out.group(2)
                rc &= accessrule_cli.edit_access_rule(**rule_dict)
        Assertion.assert_equal(rc, True, "ERR: Edit access rule failed")

    def test_07_Add_Routes(self):
        os.popen("route add -host 224.0.0.22 dev {}".format(LAN_IF))
        os.popen("route add -net 224.0.0.0 netmask 255.0.0.0 dev {}".format(LAN_IF))
        WAN_HOST.system("route add -host 224.0.0.22 dev {}".format(WAN_IF))
        WAN_HOST.system("route add -net 224.0.0.0 netmask 255.0.0.0 dev {}".format(WAN_IF))
        DMZ_HOST.system("route add -host 224.0.0.22 dev {}".format(DMZ_IF))
        DMZ_HOST.system("route add -net 224.0.0.0 netmask 255.0.0.0 dev {}".format(DMZ_IF))
        Assertion.assert_equal(True, True, "ERR: Add routes failed")

