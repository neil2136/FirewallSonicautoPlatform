from definition.settings import *

class  TestConfig_FW(Test):
    uuid = 'NonTC'

    def test_01_Add_Address_Objects(self):
        res = aoapi.config_addressobject(**multicast_dict)
        Assertion.assert_equal(res, True, "ERR: Add multicast AO failed.")

    def test_02_Enable_Multicast(self):
        multi_conf_dict = {
            'multicast': True,
            'require_igmp_membership': True,
            'timeout': 1,
            'reception_name': multicast_dict["name"],
        }
        res = multicastapi.config_multicast(**multi_conf_dict)
        Assertion.assert_equal(res, True, "ERR: Config multicast failed.")

    def test_03_Enable_Multicast_on_X0(self):
        logger.info("Enable X0 multicast")
        res = interfaceapi.config_interface(**x0_static_dict)
        Assertion.assert_equal(res, True, "ERR: Enable X0 multicast failed")

    def test_04_Config_X1(self):
        logger.info("config x1 interface... ")
        res = interfaceapi.config_interface(**x1_static_dict)
        Assertion.assert_equal(res, True, "ERR: Config X1 to static failed")

    def test_05_Config_X2(self):
        logger.info("config x2 interface... ")
        res = interfaceapi.config_interface(**x2_static_dict)
        Assertion.assert_equal(res, True, "ERR: Config X2 to static failed")

    def test_06_enable_acl_form_wan_to_multi(self):
        res = True
        show_acl_dict = {
            'version': 'ipv4',
            'from': 'WAN',
            'to': 'MULTICAST',
        }
        showaclres = accessrulecli.show_access_rules(**show_acl_dict)
        splitres = showaclres.split('access-rule ipv4')
        # # # process WAN to MULTICAST rules
        for rule in splitres:
            rule_dict = {
                'from': 'WAN',
                'to': 'MULTICAST',
                'action': 'deny',
                'action_new': 'allow',
            }
            if 'action deny' in rule:
                searchres = re.search(r'service (\w+)\s?(\w+)?', rule, re.I | re.S)
                if searchres:
                    if searchres.group(1) == 'group':
                        rule_dict['service_group'] = searchres.group(2)
                else:
                    logger.info('can not search service group in current rule str')
                res &= accessrulecli.edit_access_rule(**rule_dict)
        Assertion.assert_equal(res, True, "ERR: enable WAN to Multi access rules failed")

    def test_07_enable_acl_form_DMZ_to_multi(self):
        res = True
        show_acl_dict = {
            'version': 'ipv4',
            'from': 'DMZ',
            'to': 'MULTICAST',
        }
        showaclres = accessrulecli.show_access_rules(**show_acl_dict)
        splitres = showaclres.split('access-rule ipv4')
        # # # process DMZ to MULTICAST rules
        for rule in splitres:
            rule_dict = {
                'from': 'DMZ',
                'to': 'MULTICAST',
                'action': 'deny',
                'action_new': 'allow',
            }
            if 'action deny' in rule:
                searchres = re.search(r'service (\w+)\s?(\w+)?', rule, re.I | re.S)
                if searchres:
                    if searchres.group(1) == 'group':
                        rule_dict['service_group'] = searchres.group(2)
                else:
                    logger.info('can not search service group in current rule str')
                res &= accessrulecli.edit_access_rule(**rule_dict)
        Assertion.assert_equal(res, True, "ERR: enable DMZ to Multi access rules failed")

    @repeat_method(10)
    def test_08_Register_fw(self):
        time.sleep(20)
        rc = licensecli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")
