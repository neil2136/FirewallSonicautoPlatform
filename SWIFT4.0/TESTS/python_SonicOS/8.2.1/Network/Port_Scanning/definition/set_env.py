from definition.init_param import *


class TestConfigTB_01(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_00_01_config_interface_x1(self):
        logger.info("config x1 interface... ")
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X1_GW,
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        rc = interface_obj.config_interface(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")
    
    @repeat_method(3)
    def test_02_register_fw(self):
        logger.info('config interface to dhcp...')
        rc = licenseObj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_03_add_addrObj1(self):
        logger.info('add address Object..')
        ao_param ={
            "object_type": "host",
            "name": "PC1_LAN_IP",
            "zone": "LAN",
            "value": PC1_LAN_IP,
        }
        rc = addrObj.config_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, 'ERR: Add address object failed')

    def test_04_add_addrObj2(self):
        logger.info('add address Object..')
        ao_param ={
            "object_type": "host",
            "name": "WAN_IP",
            "zone": "WAN",
            "value": WAN_IP,
        }
        rc = addrObj.config_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, 'ERR: Add address object failed')

    def test_05_add_nat_policy_on_gw(self):
        logger.info('add nat policy on gw..')
        nat_opt = {
            "nat_policies": [
                {
                    "ipv4": {
                        "name": "port_scanning",
                        "dns_doctoring": False,
                        "reflexive": False,
                        "inbound": "X1",
                        "outbound": "any",
                        "comment": "",
                        "enable": True,
                        "translated_destination": {
                            "name": "PC1_LAN_IP"
                        },
                        "translated_source": {
                            "original": True
                        },
                        "translated_service": {
                            "original": True
                        },
                        "source": {
                            "any": True
                        },
                        "destination": {
                            "name": "WAN_IP"
                        },
                        "service": {
                            "name": "FTP"
                        },
                        "priority": {
                            "auto": True
                        },
                        "ticket": {
                            "tag1": "",
                            "tag2": "",
                            "tag3": ""
                        }
                    }
                }
            ]
        }
    
        rc = natObj.add_nat_policy(**nat_opt)
        Assertion.assert_equal(rc, True, 'ERR: add nat policy on fw failed')

    def test_06_add_route(self):
        logger.info('add route on pc1...')
        flag = False
        cmd = 'route add -host {} gw {}'.format(PC3_WAN_IP, Parameter.FIREWALL)
        local_host.send_command(cmd)
        output = local_host.send_command('route -n')
        logger.info(output)
        if re.search(r'{}\s+{}'.format(PC3_WAN_IP, Parameter.FIREWALL), str(output), re.I|re.DOTALL) != None:
            flag =True
        Assertion.assert_equal(flag, True, 'ERR: add route on pc1 failed')

