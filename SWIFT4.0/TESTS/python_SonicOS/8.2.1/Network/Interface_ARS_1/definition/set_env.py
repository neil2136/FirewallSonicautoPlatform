from definition.init_param import *

class Test_config_remote(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True  

    def test_00_00_config_X1_and_register(self):
        logger.info('config interface X1 and register...')
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X1_GW1,
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'asymmetric_route': False,
        }
        rc = interface_obj.config_interface(**x1)
        time.sleep(10)
        rc &= licenseObj.register('online')
        Assertion.assert_equal(rc, True, "ERR: config interface X1 and register failed")

    def test_00_01_config_X1_on_local_dut(self):
        logger.info('config interface X1 on local DUT...')
        flag = False
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X1_IP_REMOTE,
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'asymmetric_route': False,
        }
        rc = interface_obj.config_interface(**x1)
        time.sleep(10)
        output = interface_obj.get_interface_status('X1')
        logger.info(output)
        if re.search(r'asymmetric_route\W+False', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: config interface X1 on local DUT failed")

    def test_00_02_Add_route_in_pc1(self):
        logger.info('add route in pc1...')
        cmd = 'route add -net 12.12.1.0 netmask 255.255.255.0 gw 192.168.168.168'
        rc = local_host.send_command(cmd)
        Assertion.assert_equal(True, True, "ERR: add route in pc1 failed")

    def test_00_03_Restore_Remote_FW(self):
        logger.info(" {} ".center(20, '-').format('Restore Remote FW'))
        for i in range(10):
            out = os.popen('ping {} -c 1 -w 1'.format(RM_X1_IP)).read()
            if ('100% packet loss' not in out):
                logger.info(out)
                break
            elif i == 9:
                logger.info('Remote DUT is unreachable. Check the network configuration.')
                ret = os.popen('route -n').read()
                logger.info('----- The route policies on PC1 after reset: -----')
                logger.info(ret)
                os.system('service network restart')
                ret = os.popen('route -n').read()
                logger.info('----- The route policies on PC1 after reset: -----')
                logger.info(ret)

        logger.info('Restore Remote FW...')
        path = os.environ["PYTHON_COMMON_HOME"] + '/config/restore_gw_rmt_tel.py'
        cmd = 'python3 {} -os=1 --testbed={} -device=RemoteGEN7 -if=X1 -zone=WAN -ip=12.12.1.201 -restore=1'.format(path, Params.testbed)
        logger.info(cmd)
        out = os.popen(cmd).read()
        logger.info(out)

        for i in range(10):
            out = os.popen('ping {} -c 2'.format(RM_X1_IP)).read()
            logger.info(out)
            if ('100% packet loss' not in out):
                logger.info('Ping Remote success.')
                rc = True
                break
            elif i == 9:
                rc = False
                logger.info('Remote is unreachable.')
        Assertion.assert_equal(rc, True, "ERR: Restore Remote FW failed")

    @repeat_method(3)
    def test_00_04_Enable_remote_api_basic(self):
        logger.info(" {} ".center(20, '-').format('Enable Remote Api Basic'))
        commands = ['configure', 'administration','sonicos-api','basic','commit','exit','exit','exit']
        (rc, output) = rm_cli.do_cli_commands(commands, 1)
        Assertion.assert_equal(rc, True, "ERR: enable remote api basic failed")

    def test_00_05_add_X3_vlan_on_remote_dut(self):
        logger.info('add interface X3 vlan on remte DUT...')
        flag = False
        logger.info(vlan_id_X3)
        logger.info(vlan_id_X4)
        x3_vlan = {
            'if': 'X3',
            'type': 'vlan',
            'vlan_tag': vlan_id_X3,
            'zone': 'LAN',
            'mode': 'static',
            'mgmt_ping': True,
            'ip': Parameter.X3_IP_REMOTE,
            'asymmetric_route': True,
        }
        rc = interface_obj_remote.unassign_interface(interface = 'X3')
        rc = interface_obj_remote.add_interface(**x3_vlan)
        output = interface_obj_remote.get_vlan_interface_status(name = 'X3', vlan_id = str(vlan_id_X3))
        logger.info(output)
        if re.search(r'asymmetric_route\W+True', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify vlan interface X3 ARS failed")

    def test_00_06_config_X4_vlan_on_remote_dut(self):
        logger.info('add vlan interface x4 and verify ARS status...')
        flag = False
        x4_vlan = {
            'if': 'X4',
            'type': 'vlan',
            'vlan_tag': vlan_id_X4,
            'zone': 'LAN',
            'mode': 'static',
            'mgmt_ping': True,
            'ip': Parameter.X4_IP_REMOTE,
            'asymmetric_route': True,
        }
        rc = interface_obj_remote.add_interface(**x4_vlan)
        output = interface_obj_remote.get_vlan_interface_status(name = 'X4', vlan_id = str(vlan_id_X4))
        logger.info(output)
        if  re.search(r'asymmetric_route\W+True', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify vlan interface X4 ARS failed")

    def test_00_07_add_address_obj_on_remote_DUT(self):
        logger.info('add address object on local DUT...')
        ao_1 = {
            "object_type": "network",
            "name": Client_sub,
            "zone": "LAN",
            "value": "{},255.255.255.0".format(Client_sub),
        }
        ao_2 = {
            "object_type": "host",
            "name": Parameter.X4_IP,
            "zone": "LAN",
            "value": Parameter.X4_IP,
        }
     

        rc = addrObj_remote.config_addressobject(**ao_1)
        rc &= addrObj_remote.config_addressobject(**ao_2)
        Assertion.assert_equal(rc, True, "ERR: add address object  failed")

    def test_00_08_add_route_on_remote_DUT(self):
        logger.info('add route on remote DUT...')
        route_1 = {
            "route_policies": [
                {
                    "ipv4": {
                        "name": "X4_Vlan",
                        "comment": "",
                        "interface": "X4:V{}".format(vlan_id_X4),
                        "metric": 1,
                        "service": {
                            "any": True
                        },
                        "gateway": {
                            "name": Parameter.X4_IP
                        },
                        "source": {
                            "any": True
                        },
                        "destination": {
                            "name": Client_sub,
                        },
                        "disable_on_interface_down": True,
                        
                    }
                }
            ]
        }
        rc = routeObj_remote.add_route_policy(**route_1)
        Assertion.assert_equal(rc, True, "ERR: add route policy failed")


class Test_config_local(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True  

   

    def test_01_01_config_X2_on_local_dut(self):
        logger.info('config interface X2 on local DUT...')
        flag = False
        x2 = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'asymmetric_route': False,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x2)
        output = interface_obj.get_interface_status('X2')
        logger.info(output)
        if re.search(r'asymmetric_route\W+False', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: config interface X2 on local DUT failed")

    def test_01_02_config_X3_vlan_on_local_dut(self):
        logger.info('add vlan interface x3 and verify ARS status...')
        flag = False
        x3_vlan = {
            'if': 'X3',
            'type': 'vlan',
            'vlan_tag': vlan_id_X3,
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'asymmetric_route': False,
            'mgmt_ping': True,
        }
        rc = interface_obj.add_interface(**x3_vlan)
        output = interface_obj.get_vlan_interface_status(name = 'X3', vlan_id = str(vlan_id_X3))
        logger.info(output)
        if re.search(r'asymmetric_route\W+False', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify vlan interface X3 ARS failed")

    def test_01_03_config_X4_vlan_on_local_dut(self):
        logger.info('add vlan interface x4 and verify ARS status...')
        flag = False
        x4_vlan = {
            'if': 'X4',
            'type': 'vlan',
            'vlan_tag': vlan_id_X4,
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X4_IP,
            'asymmetric_route': False,
            'mgmt_ping': True,
        }
        rc = interface_obj.add_interface(**x4_vlan)
        output = interface_obj.get_vlan_interface_status(name = 'X4', vlan_id = str(vlan_id_X4))
        logger.info(output)
        if re.search(r'asymmetric_route\W+False', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify vlan interface X4 ARS failed")

    def test_01_04_add_address_obj_on_local_DUT(self):
        logger.info('add address object on local DUT...')
        ao_1 = {
            "object_type": "network",
            "name": Server_sub,
            "zone": "LAN",
            "value": "{},255.255.255.0".format(Server_sub),
        }
        ao_2 = {
            "object_type": "host",
            "name": Parameter.X3_IP_REMOTE,
            "zone": "LAN",
            "value": Parameter.X3_IP_REMOTE,
        }
     

        rc = addrObj.config_addressobject(**ao_1)
        rc &= addrObj.config_addressobject(**ao_2)
        Assertion.assert_equal(rc, True, "ERR: add address object  failed")

    def test_01_05_add_route_on_local_DUT(self):
        logger.info('add route on local DUT...')
        route_1 = {
            "route_policies": [
                {
                    "ipv4": {
                        "name": "X3_Vlan",
                        "comment": "",
                        "interface": "X3:V{}".format(vlan_id_X3),
                        "metric": 1,
                        "service": {
                            "any": True
                        },
                        "gateway": {
                            "name": Parameter.X3_IP_REMOTE
                        },
                        "source": {
                            "any": True
                        },
                        "destination": {
                            "name": Server_sub,
                        },
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "distance": {
                            "auto": True
                        },
                        "tos": "0x00",
                        "mask": "0x00",
                        "type": "standard"
                    }
                }
            ]
        }
        rc = routeObj.add_route_policy(**route_1)
        Assertion.assert_equal(rc, True, "ERR: add route policy failed")



class Test_Config_Switch(Test):
    uuid = 'NonTC'

    def test_00_change_untag_to_tag(self):
        osstack = Openstack(Params.testbed)
        rc = osstack.set_node_interface_state('UTM','X3:1', 'tag')
        rc &= osstack.set_node_interface_state('UTM','X4:1', 'tag')
        rc &= osstack.set_node_interface_state('RemoteGEN6','X3:1', 'tag')
        rc &= osstack.set_node_interface_state('RemoteGEN6','X4:1', 'tag')
        Assertion.assert_equal(rc, True, "ERR: change X3 to tag.")
