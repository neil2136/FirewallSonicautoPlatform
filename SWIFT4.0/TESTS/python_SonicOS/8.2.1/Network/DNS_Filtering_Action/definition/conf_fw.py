from definition.settings import *

class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_00_01_Config_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
        }
        rc = interface_api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")
        
    @repeat_method(5)
    def test_00_02_register_fw(self):
        license = LicenseCli(fw_cli)
        rc = license.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_02_modify_pc1_route(self):
        logger.info('Set route on PC1 via gw {}'.format(Parameter.FIREWALL))
        rc = os.system('route add -net {} netmask {} gw {}'.format(Parameter.Route_Host_1, Parameter.Route_Mask_1, Parameter.PC1_GW))
        rc = os.system('route del default')
        rc = os.system('route add -net {} netmask {} gw {}'.format(Parameter.Route_Host_2, Parameter.Route_Mask_2, Parameter.FIREWALL))
        result = os.popen('ip -4 r')
        output = result.read()
        logger.info(output)
        Assertion.assert_regular(output, 'default via 192.168.168.168 dev eth0', "ERR: Modify route on PC1 failed")

    def test_04_set_log_level_to_inform(self):
        rc = log_cata.logging_level(level='inform')
        Assertion.assert_equal(rc, True, "ERR: Set_log_level_to_inform failed")

    def test_05_enable_DNS_Packet_Allowed(self):
        eventid = [1549,1550,1593,1594,1684,1685,1686,1687,1688,1675, 1676, 1677, 1678, 1679, 1680, 1681, 1682, 1683]
        for i in eventid:
            log = {
                "log": {
                    "event": [
                        {
                            "id": i,
                            "category": "Network",
                            "group": "DNS Security",
                            "priority_level": "inform",
                            "log_monitor": {
                                "redundancy_interval": 0
                            },
                            "email_alert": {
                                "redundancy_interval": 0
                            },
                            "syslog": {
                                "redundancy_interval": 0
                            },
                            "event_profile": {
                                "syslog_server_profile": 0
                            }
                        }
                    ]
                }
            }
            rc = log_set.edit_event(event_id=str(i), **log)
        Assertion.assert_equal(rc, True, "ERR: Enable_DNS_Packet_Allowed failed")

    def test_06_set_Display_Events_in_Log_Monitor_to_0_seconds(self):
        set_log_monitor = {
            "log": {
                "category": [
                    {
                        "name": "Network",
                        "log_monitor": {
                            "type": "mixed",
                            "redundancy_interval": {}
                        }           
                    }
                ]
            }
        }
        rc = log_cata.edit_log_categories_by_name('Network', **set_log_monitor)
        Assertion.assert_equal(rc, True, "ERR: Set_Display_Events_in_Log_Monitor_to_0_seconds failed")

    def test_07_config_dns_security_logging(self):
        log_id = 107
        log_group_dict = {
            "log":{
                "group":[
                    {
                        "id": log_id,
                        "name":"DNS Security",
                        "priority_level":"alert",
                        "log_email":{},
                        "log_monitor":{
                            "type":"enabled",
                            "redundancy_interval":{}
                        },
                        "email_alert":{"type":"mixed"},
                        "syslog":{"type":"mixed"},
                        "trap":{"type":"mixed","redundancy_interval":{"value":60}},
                        "ipfix":{"type":"mixed"},
                        "event_profile":{"syslog_server_profile":0},
                        "log_digest":{"mixed":True},
                        "color":{"leave_unchanged":True},
                        "alert_email":{}
                    }
                ]
            }
        }
        rc = log_cata.edit_log_category_groups_by_id(id=str(log_id), **log_group_dict)
        # rc = log_setting_api.edit_event(event_id=str(receive_log_dict['log']['event'][0]['id']), **receive_log_dict)
        Assertion.assert_equal(rc, True, "=> ERR: Config snmp receive logging failed! ")
