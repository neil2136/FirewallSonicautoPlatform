from definition.settings import *


class TestSetupVPN(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_add_remote_x3_ao_on_local_dut(self):
        remote_x3_subnet = {
            'name': 'remote_x3_subnet',
            'zone': 'VPN',
            'object_type': 'network',
            'value': f'{Parameter.X3_REMOTE_NET},{Parameter.MASK}',
        }
        res = addressobjectsapi.config_addressobject(**remote_x3_subnet)
        Assertion.assert_equal(res, True, "ERR: add remote x3 ao on local dut failed")

    def test_02_add_local_vpn_policy(self):
        lvpn = {
            'type': 'site_to_site',
            'name': 'localvpn',
            'enable': True,
            'auth_mode': 'shared_secret',
            'secret': 'password',
            'pri_gate': Parameter.X1_REMOTE_IP,
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'ike_exchange': 'ikev2',
            # 'ike_encryption': 'aes-128',
            'ipversion': 'ipv4',
            # 'ike_auth': 'sha-1',
            # 'ike_dh_group': '2',
            'ike_lifetime': '28800',
            'ipsec_lifetime': '28800',
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_gcm16_256',
            # 'ipsec_pfs': True,
            'local_net_type': 'name',
            'local_net_name': 'X2 Subnet',
            'remote_net_type': 'name',
            'remote_net_name': 'remote_x3_subnet',
            'keep_alive': True,
        }
        res = vpnbasesettingapi.add_vpn_policy(**lvpn)
        logger.info(res)
        vpnentry = vpnbasesettingapi.show_s2svpnpolicy()
        logger.info(f'vpnentry is :{vpnentry}')
        Assertion.assert_regular(str(vpnentry), "localvpn", "ERR: Add local vpn policy failed.")

    def test_03_add_local_x2_network_ao_on_remote_dut(self):
        remote_x2_subnet = {
            'name': 'remote_x2_subnet',
            'zone': 'VPN',
            'object_type': 'network',
            'value': f'{Parameter.X2_NET},{Parameter.MASK}',
        }
        res = r_addressobjectsapi.config_addressobject(**remote_x2_subnet)
        Assertion.assert_equal(res, True, "ERR: add local x2 network ao on remote dut failed")

    def test_04_add_remote_vpn_policy(self):
        rvpn = {
            'type': 'site_to_site',
            'name': 'remotevpn',
            'enable': True,
            'auth_mode': 'shared_secret',
            'secret': 'password',
            'pri_gate': Parameter.X1_IP,
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'ike_exchange': 'ikev2',
            # 'ike_encryption': 'aes-128',
            'ipversion': 'ipv4',
            # 'ike_auth': 'sha-1',
            # 'ike_dh_group': '2',
            'ike_lifetime': '28800',
            'ipsec_lifetime': '28800',
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_gcm16_256',
            # 'ipsec_pfs': True,
            'local_net_type': 'name',
            'local_net_name': 'X3 Subnet',
            'remote_net_type': 'name',
            'remote_net_name': 'remote_x2_subnet',
            'keep_alive': True,
        }
        res = r_vpnbasesettingapi.add_vpn_policy(**rvpn)
        logger.info(res)
        vpnentry = r_vpnbasesettingapi.show_s2svpnpolicy()
        logger.info(f'vpnentry is :{vpnentry}')
        Assertion.assert_regular(str(vpnentry), 'remotevpn', "ERR: Add remote vpn policy failed.")

    @repeat_method(2)
    def test_05_check_local_vpn_status(self):
        time.sleep(10)
        (res, status) = vpnbasesettingapi.get_vpn_status('localvpn')
        logger.info(f'vpn status:{res},{status}')
        flag = True if res and status == 'up' else False
        Assertion.assert_equal(flag, True, "ERR: check local vpn status failed.")

    @repeat_method(2)
    def test_06_check_remote_vpn_status(self):
        time.sleep(10)
        (res, status) = r_vpnbasesettingapi.get_vpn_status('remotevpn')
        logger.info(f'vpn status:{res},{status}')
        flag = True if res and status == 'up' else False
        Assertion.assert_equal(flag, True, "ERR: check remote vpn status failed.")

    @repeat_method(2)
    def test_07_check_vpn_traffic_from_local_lan_host_to_remote_lan_host(self):
        output = PC2_Login.send_command(f'ping {PC3_ETH1_IP} -I eth1 -c 5')
        logger.info(f'output is:{output}')
        flag = True if "100% packet loss" not in output else False
        Assertion.assert_equal(flag, True, "ERR: check vpn traffic failed")

    @repeat_method(2)
    def test_08_check_traffic_from_remote_lan_host_to_local_lan_host(self):
        output = PC3_Login.send_command(f'ping {PC2_ETH1_IP} -I eth1 -c 5')
        logger.info(f'output is:{output}')
        flag = True if "100% packet loss" not in output else False
        Assertion.assert_equal(flag, True, "ERR: check vpn traffic failed")
