from settings import *


class TestConfigENV(Test):
    uuid = 'NonTC'

    def test_00_01_config_X1_X2(self):
        ping = trafficGen.ping(Parameter.REMOTE_X1)

        logger.info(f'config X1 to {Parameter.DUT_X1_IP}')
        x1_static_dict = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.DUT_X1_IP,
            'gateway': Parameter.DUT_X1_GW,
            'netmask': Parameter.NETMASK,
            'mgmt-https': True,
            'dns1':Params.G_DNS1,
        }
        rc = interface.config_interface(**x1_static_dict)
        x2_static_dict = {
            'if': 'x2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.DUT_X2_IP,
            'gateway': Parameter.DUT_X2_GW,
            'netmask': Parameter.NETMASK,
            'mgmt-https': True,
        }   
        x3_static_dict = {
            'if': 'x3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.DUT_X3_IP,
            'netmask': Parameter.NETMASK,
            'mgmt-https': True,
        } 
        rc = interface.config_interface(**x1_static_dict)
        rc &= interface.config_interface(**x2_static_dict)
        rc &= interface.config_interface(**x3_static_dict)
        Assertion.assert_equal(rc, True, "ERR: Config interface failed.")

    @unittest.skipIf(Params.product!='TZ80-PROTOTYPE','skip register edit if not TZ80-PROTOTYPE')
    @repeat_method(5)
    def test_00_02_register(self):
        rc = license_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register firewall failed")

    def test_00_03_add_address(self):
        ao_x1 ={
            "object_type": "host",
            "name": Parameter.REMOTE_X1,
            "zone": "WAN",
            "value": Parameter.REMOTE_X1,
        }
        ao_x2 ={
            "object_type": "host",
            "name": Parameter.REMOTE_X2,
            "zone": "WAN",
            "value": Parameter.REMOTE_X2,
        }
        ao_x3 ={
            "object_type": "host",
            "name": Parameter.REMOTE_X3,
            "zone": "WAN",
            "value": Parameter.REMOTE_X3,
        }
        ao_mcast_v4 ={ 
            "object_type": "host",
            "name": Parameter.MCAST_V4,
            "zone": "MULTICAST",
            "value": Parameter.MCAST_V4,
        }
        ao_bcast_v4 ={ 
            "object_type": "host",
            "name": Parameter.BCAST_V4,
            "zone": "WAN",
            "value": Parameter.BCAST_V4,
        }
        ao_local_v6 ={ 
            "object_type": "host",
            "name": Parameter.LOCAL_V6,
            "zone": "WAN",
            "ip": Parameter.LOCAL_V6,
        }
        ao_bcast_v6 ={ 
            "object_type": "host",
            "name": Parameter.BCAST_V6,
            "zone": "MULTICAST",
            "ip": Parameter.BCAST_V6,
        }        
        t_manual = {
            'name': Parameter.REMOTE_X0_IPv6_Network['manual'],
            'zone': 'WAN',
            'object_type': 'network',
            'subnet': Parameter.REMOTE_X0_IPv6_Network['manual'],
            'mask': '/64',
        }
        t_6to4 = {
            'name': Parameter.REMOTE_X0_IPv6_Network['6to4'],
            'zone': 'WAN',
            'object_type': 'network',
            'subnet': Parameter.REMOTE_X0_IPv6_Network['6to4'],
            'mask': '/64',
        }
        t_manual_x3 = {
            'name': Parameter.REMOTE_X3_IPv6_Network['manual'],
            'zone': 'WAN',
            'object_type': 'network',
            'subnet': Parameter.REMOTE_X3_IPv6_Network['manual'],
            'mask': '/64',
        }
        rc = ao.config_addressobject(**ao_x1)
        rc &= ao.config_addressobject(**ao_x2)
        rc &= ao.config_addressobject(**ao_x3)
        rc &= ao.config_addressobject(**ao_mcast_v4)
        rc &= ao.config_addressobject(**ao_bcast_v4)
        rc &= ao.config_ipv6_addressobject(**ao_local_v6)
        rc &= ao.config_ipv6_addressobject(**ao_bcast_v6)
        rc &= ao.config_ipv6_addressobject(**t_manual)
        rc &= ao.config_ipv6_addressobject(**t_6to4)
        rc &= ao.config_ipv6_addressobject(**t_manual_x3)
        Assertion.assert_equal(rc, True, "ERR: Add ao failed.")

    def test_00_04_set_remote_x1(self):
        logger.info('Restore Remote FW...')
        path = os.environ["PYTHON_COMMON_HOME"] + '/config/restore_gw_rmt_tel.py'
        cmd = 'python3 {} -os=1 --testbed={} -device=RemoteGEN6 -if=X1 -zone={} -ip={} -restore=1'.\
              format(path, Params.testbed,'WAN', Parameter.REMOTE_X1)
        logger.info(cmd)
        out = os.popen(cmd).read()
        logger.info(out)

        rc = False
        for i in range(10):
            out = os.popen('ping {} -c 2'.format(Parameter.REMOTE_X1)).read()
            logger.info(out)
            if ('100% packet loss' not in out):
                logger.info('Ping Remote success.')
                rc = True
                break
            elif i == 9:
                rc = False
                logger.info('Remote is unreachable.')

        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: Restore Remote FW failed")

    def test_00_05_add_remote_ao(self):
        rem_ao_x1 ={
            "object_type": "host",
            "name": Parameter.DUT_X1_IP,
            "zone": "WAN",
            "value": Parameter.DUT_X1_IP,
        }
        rem_ao_x2 ={
            "object_type": "host",
            "name": Parameter.DUT_X2_IP,
            "zone": "WAN",
            "value": Parameter.DUT_X2_IP,
        }
        rem_ao_x3 ={
            "object_type": "host",
            "name": Parameter.DUT_X3_IP,
            "zone": "WAN",
            "value": Parameter.DUT_X3_IP,
        }
        rem_x0_manual = {
            'name': Parameter.DUT_X0_IPv6_Network['manual'],
            'zone': 'WAN',
            'object_type': 'network',
            'subnet': Parameter.DUT_X0_IPv6_Network['manual'],
            'mask': '/64',
        }
        rem_x3_manual = {
            'name': Parameter.DUT_X3_IPv6_Network['manual'],
            'zone': 'WAN',
            'object_type': 'network',
            'subnet': Parameter.DUT_X3_IPv6_Network['manual'],
            'mask': '/64',
        }
 
        rc = rem_ao.config_addressobject(**rem_ao_x1)
        rc &= rem_ao.config_addressobject(**rem_ao_x2)
        rc &= rem_ao.config_addressobject(**rem_ao_x3)
        rc &= rem_ao.config_ipv6_addressobject(**rem_x0_manual)
        rc &= rem_ao.config_ipv6_addressobject(**rem_x3_manual)
        Assertion.assert_equal(rc, True, "ERR: Add ao failed.")

    def test_00_06_add_and_edit_acl(self):
        acl_opt={
            "uuid":'1',
            "name":"Custom Access Rule",
            "comment":"",
            "action":"allow",
            "priority":{"auto":True},
            "enable":True,
            "from":"WAN",
            "source":{"address":{"any":True},"port":{"any":True}},
            "to":"WAN","destination":{"address":{"any":True}},
            "service":{"name":"6over4"},
            "users":{"included":{"all":True},
                    "excluded":{"none":True}
            },
            "tcp":{"urgent":False,"timeout":15},
            "udp":{"timeout":30},
            "dpi":True,
            "dpi_ssl":{"client":True,"server":True},
            "quality_of_service":{"class_of_service":{},"dscp":{"preserve":True}},
            "botnet_filter":True,
            "geo_ip_filter":{"enable":True,"global":True},
            "logging":True,
            "flow_reporting":False,
            "connection_limit":{"source":{},"destination":{}},
            "sip":False,
            "h323":False,
            "fragments":True,
            "management":True,
            "max_connections":100,
            "packet_monitoring":False,
            "schedule":{"always_on":True}
        }
        wan_lan_acl_opt_v6=  {
            "uuid": '1',
            "name": "rule2",
            "enable": True,
            "from": "WAN",
            "to": "LAN",
            "action": "Allow",
            "source": {
                "address": {
                    "any": True
                },
                "port": {
                    "any": True
                }
            },
            "service": {
                "any": True
            },
            "destination": {
                "address": {
                    "any": True,
                }
            },
            "schedule": {
                "always_on": True
            },
            "users": {
                "included": {
                    "all": True
                },
                "excluded": {
                    "none": True
                }
            },
            "comment": "",
            "fragments": True,
            "logging": True,
            "sip": True,
            "h323": True,
            "flow_reporting": False,
            "botnet_filter": False,
            "geo_ip_filter": {
                "enable": False,
                "global": True
            },
            "block": {
                "countries": {
                    "unknown": False
                }
            },
            "packet_monitoring": False,
            "management": False,
            "max_connections": 100,
            "tcp": {
                "timeout": 15,
                "urgent": False
            },
            "icmp": {
                "timeout": 30
            },
            "connection_limit": {
                "source": {},
                "destination": {}
            },
            "dpi": True,
            "dpi_ssl": {
                "client": True,
                "server": True
            },
            "redirect_unauthenticated_users_to_log_in": True,
            "quality_of_service": {
                "class_of_service": {},
                "dscp": {
                    "preserve": True
                }
            },
        }
        wan_wan_acl_opt_v6=  {
            "uuid": '1',
            "name": "rule3",
            "enable": True,
            "from": "WAN",
            "to": "WAN",
            "action": "Allow",
            "source": {
                "address": {
                    "any": True
                },
                "port": {
                    "any": True
                }
            },
            "service": {
                    "group": 'Ping6'
            },
            "destination": {
                "address": {
                    "any": True,
                }
            },
            "schedule": {
                "always_on": True
            },
            "users": {
                "included": {
                    "all": True
                },
                "excluded": {
                    "none": True
                }
            },
            "comment": "",
            "fragments": True,
            "logging": True,
            "sip": True,
            "h323": True,
            "flow_reporting": False,
            "botnet_filter": False,
            "geo_ip_filter": {
                "enable": False,
                "global": True
            },
            "block": {
                "countries": {
                    "unknown": False
                }
            },
            "packet_monitoring": False,
            "management": False,
            "max_connections": 100,
            "tcp": {
                "timeout": 15,
                "urgent": False
            },
            "icmp": {
                "timeout": 30
            },
            "connection_limit": {
                "source": {},
                "destination": {}
            },
            "dpi": True,
            "dpi_ssl": {
                "client": True,
                "server": True
            },
            "redirect_unauthenticated_users_to_log_in": True,
            "quality_of_service": {
                "class_of_service": {},
                "dscp": {
                    "preserve": True
                }
            },
        }
        rc = acl.config_accessrule(**acl_opt)  
        rc &= rem_acl.config_accessrule(**acl_opt)    
        rc &= acl_ipv6.config_accessrule_ipv6(**wan_wan_acl_opt_v6)   
        rc &= rem_acl_ipv6.config_accessrule_ipv6(**wan_wan_acl_opt_v6)
        uuid_search={'from':'WAN','to':'LAN','service': 'any'}
        uuid_dut =acl_ipv6.get_ipv6_accessrule_uuid(**uuid_search)
        uuid_rem =rem_acl_ipv6.get_ipv6_accessrule_uuid(**uuid_search)
        rc &= acl_ipv6.put_accessrule_ipv6(**wan_lan_acl_opt_v6, url=f'/access-rules/ipv6/uuid/{uuid_dut}')   
        rc &= rem_acl_ipv6.put_accessrule_ipv6(**wan_lan_acl_opt_v6, url=f'/access-rules/ipv6/uuid/{uuid_rem}')   
        Assertion.assert_equal(rc, True, "ERR: Add acess rule failed.")





