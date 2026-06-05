from definition.initial_parameter import *


@paramunittest.parametrized(
    {'tcid': '3', 'uuid': '1524131'},
    {'tcid': '5', 'uuid': '1524132'},
    {'tcid': '6', 'uuid': '1524133'},
)
class TestPathMTUFind(Test):
    def setParameters(self, tcid, uuid):
        self.uuid = uuid
        self.tcid = tcid
        self.description = show_testcase_info(TESTPLAN, self.tcid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.tcid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_config_X2_interface(self):
        if self.tcid == '6':
            output = os.popen("ping 192.168.168.168 -c 5 ").read()
            logger.info(output)
            logger.info("This is tc 6...")
            logger.info("This is tc 6, step 1: add custom zone...")         
            zonejson = {
                "zones": [
                    {
                        "name": "custom_zone",
                        "security_type": "public",
                        "interface_trust": True,
                        "auto_generate_access_rules": {
                            "allow_from_to_equal": True,
                            "allow_from_higher": True,
                            "allow_to_lower": True,
                            "deny_from_lower": True
                        },
                        "gateway_anti_virus": True,
                        "intrusion_prevention": False
                    }
                ]
            }
            rc1 = zone_obj.add_zone_object( **zonejson )
            
            output = os.popen("ping 192.168.168.168 -c 5 ").read()
            logger.info(output)
            time.sleep(5)

            logger.info("This is tc 6, step 2: config X2 interface...")  
            x2_static = {
                'if': 'X2',
                'zone': 'custom_zone', 
                'mode': 'static',
                'ip': X2_IP,
            }
            rc2 = interface_obj.config_interface(**x2_static)
            Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X2 interface failed")
        else:
            Assertion.assert_equal(True, True, "")

    def test_02_verify_path_mtu_find(self):
        command = ''
        flag = False
        if self.tcid == '5':
            command = 'pmtu-discovery {}'.format(PC1_ETH0_IP)   # LAN
        elif self.tcid == '3':
            command = 'pmtu-discovery {}'.format(PC2_ETH1_IP)   # WAN
        elif self.tcid == '6':
            command = 'pmtu-discovery {}'.format(PC2_ETH2_IP)   # Custom zone

        ret = diag_obj.diag_dns_name_lookup(cmd = command).split("\n")
        logger.info(ret)
        for r in ret:
            if re.search(r"Discovered Path MTU is \d+", r, re.I):
                flag = True
                break
        Assertion.assert_equal(flag, True, "ERR: Verify path mtu find failed") 

    @repeat_method(3)
    def test_03_delete_custom_zone(self):
        if self.tcid == '6':
            logger.info("This is tc 6, delete custom zone...")
            rc1 = interface_obj.unassign_interface( interface='X2' )
            time.sleep(5)
            rc2 = zone_obj.delete_zone_object(name = 'custom_zone')
            Assertion.assert_equal(rc1 & rc2, True, "ERR: Delete custom zone failed")
        else:
            Assertion.assert_equal(True, True, "")
