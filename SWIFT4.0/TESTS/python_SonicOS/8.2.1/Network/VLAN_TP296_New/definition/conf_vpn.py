from definition.settings import *


class TestSetupVPN(Test):
    uuid = 'NonTC'

    def test_01_Config_X2(self):
        logger.info("config x2 interface... ")
        x2_static_dict = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'type': 'vlan',
            'vlan_tag': X2_VLAN1_ID,
            'ip': Parameter.X2_VLAN_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X2_GW,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        res = interfacev4api.add_interface(**x2_static_dict)
        logger.info('config X2 vlan interface result: {}'.format(res))
        Assertion.assert_equal(res, True, "ERR: Config X2 to static failed")

    @repeat_method(5)
    def test_01_01_register_fw(self):
        rc = license.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")


    def test_02_Init_Remote_FW(self):
        logger.info('Restore Remote FW...')
        path = os.environ["PYTHON_COMMON_HOME"] + '/config/restore_gw_rmt_tel.py'
        command1 = f'python3 {path} -os=1 --testbed={Params.testbed} -device=RemoteGEN5 -if=X1 -zone=WAN -ip={Parameter.X1_REMOTE_IP} -restore=1'
        confres = PC1_login.send_command(command1)
        logger.info(confres)

        logger.info("add a route to interface X1 sub... ")
        command2 = f'route add -net {Parameter.X2_SUB}/24 gw {Parameter.FIREWALL}'
        routeres = PC1_login.send_command(command2)
        logger.info('add x1 sub route in PC1 result: {}'.format(routeres))

        pingres = PC1_login.ping_from_eth(
            ip=Parameter.X1_REMOTE_IP, eth='eth0')
        Assertion.assert_equal(pingres, True, "ERR: Restore Remote FW failed")

    def test_03_add_s2s_local_vpn(self):
        local_ao_dict = {
            "object_type": "network",
            "name": "remote_vpn_sub",
            "zone": "LAN",
            "value": Parameter.X0_REMOTE_SUB + ',255.255.255.0'
        }
        local_s2svpn_dict = {
            'type': 'site_to_site',
            'name': 'localvpnforvlan1',
            'pri_gate': Parameter.X1_REMOTE_IP,
            'edit_auth': False,
            'auth_mode': 'shared_secret',
            'secret': '123456',
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'local_ike_id': '1.2.3.4',
            'peer_ike_id': '1.2.3.4',

            'edit_network': False,
            'local_net_type': 'name',
            'local_net_name': f'X4:V{X4_VLAN1_ID} Subnet',
            'remote_net_type': 'name',
            'remote_net_name': 'remote_vpn_sub',
            'keep_alive': True,
            'bound_to': ['interface', f'X2:V{X2_VLAN1_ID}'],
        }

        aoapi.config_addressobject(**local_ao_dict)
        localvpnapi.add_vpn_policy(**local_s2svpn_dict)
        vpnentry = localvpnapi.show_s2svpnpolicy()
        output = True if local_s2svpn_dict['name'] in str(vpnentry) else False
        Assertion.assert_equal(
            output, True, "ERR: Add local vpn policy failed.")

    def test_04_add_s2s_remote_vpn(self):
        remote_x0_config = {
            'if': 'x0',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X0_REMOTE_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt-ssh': True
        }
        remote_ao_dict = {
            'name': 'remote_vpn_sub',
            'version': 'ipv4',
            'type': 'network',
            'zone': 'LAN',
            'network': Parameter.X4_VLAN1_SUB + ' 255.255.255.0'
        }
        remote_s2svpn_dict = {
            'type': 'site_to_site',
            'name': 'localvpnforvlan1',
            'pri_gate': Parameter.X2_VLAN_IP,
            'edit_auth': False,
            'auth_mode': 'shared_secret',
            'secret': '123456',
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'local_ike_id': '1.2.3.4',
            'peer_ike_id': '1.2.3.4',

            'edit_network': False,
            'local_net_type': 'name',
            'local_net_name': 'X0 Subnet',
            'remote_net_type': 'name',
            'remote_net_name': 'remote_vpn_sub',
            'keep_alive': True,
        }
        remoteinterfacecli.config_interface(**remote_x0_config)
        remotevpncli.delete_allvpnpolicy()

        remoteaocli.add_address_object(**remote_ao_dict)
        res = remotevpnapi.add_vpn_policy(**remote_s2svpn_dict)
        Assertion.assert_equal(
            res, True, "ERR: Add local vpn policy failed.")
