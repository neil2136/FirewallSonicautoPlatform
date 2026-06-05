from definition.settings import *


class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_00_00_config_x1_interface(self):
        logger.info("config x1 interface... ")
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.WANIP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.WANGW,
            'dns1': PC3_eth0,
            'dns2': Params.G_DNS1,
            'mgmt_https': False,
            'mgmt_ssh': False,
            'mgmt_ping': False,
        }
        rc = LInterface_ipv4.config_interface(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    def test_00_01_Add_DUT_AddObj_in_DUT(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc = LAddrOBJ.config_addressobject(**remote_l)
        logger.info('-' * 10 + 'Add AO for rm DUT' + '-' * 10)
        rc &= RAddrOBJ.config_addressobject(**remote_r)
        Assertion.assert_equal(rc, True, 'Add AO for DUT and RDUT Failed.')

    def test_00_02_Add_NAT_Policy_in_DUT(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        nat_json = {
            "nat_policies": [
                {
                    "ipv4": {
                        "uuid": "00000000-0000-0001-0800-2cb8ed6d7acc",
                        "name": "Custom NAT Policy",
                        "dns_doctoring": False,
                        "source_port_remap": True,
                        "inbound": "any",
                        "outbound": "any",
                        "comment": "",
                        "enable": True,
                        "translated_destination": {
                            "original": True
                        },
                        "translated_source": {
                            "name": "X1 IP"
                        },
                        "translated_service": {
                            "original": True
                        },
                        "source": {
                            "name": remote_l['name']
                        },
                        "destination": {
                            "any": True
                        },
                        "service": {
                            "any": True
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
        rc = LNatPolicy_obj.add_nat_policy(**nat_json)
        Assertion.assert_equal(rc, True, "ERR:add nat policy failed")

    def test_00_03_Set_PC2_route_from_remote(self):
        logger.info('-'*10+'Add NAT route'+'-'*10)
        cmd1 = "route add -net 0.0.0.0 netmask 0.0.0.0 gw {}".format(Parameter.REMOTEX0)
        cmd2 = "route del -net 0.0.0.0 netmask 0.0.0.0 gw 172.16.1.1"
        for cmd in [cmd1, cmd2]:
            PC2_login.send_command(cmd)
        rt_info = PC2_login.send_command("route -n")
        if re.search('0\.0\.0\.0.*172\.16\.1\.101', rt_info):
            rc = True
        else:
            rc = False
            logger.info(rt_info)
        Assertion.assert_equal(rc, True, 'Add NAT route Failed.')

    def test_00_04_Conf_DNS_Server_in_PC3(self):
        configfilecmds = [
            'cp {}vpntestbed.com.db /var/named/chroot/var/named/'.format(conf_path),
            'cp {}named.conf /var/named/chroot/etc/'.format(conf_path),
            'service named restart',
        ]
        output = PC3_login.send_commands(configfilecmds)
        if re.search('Starting named', output):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'Add AO for DUT and RDUT Failed.')

    def test_00_05_Config_Log_Settings_on_Remote(self):
        logger.info('-' * 10 + 'Enable all VPN log' + '-' * 10)
        rc = Rlog_set.enable_all_log_category()
        logger.info('-' * 10 + 'Set the level of LOG as Debug' + '-' * 10)
        rc &= Rlog_set.logging_level(level='debug')
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: Config log settings failed.")
