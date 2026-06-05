from definition.settings import *


class TestSetupVPN(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_add_tunnel_vpn_local(self):
        lvpn = {
            'type': 'tunnel_interface',
            'name': 'localtunnelvpn',
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
            'keep_alive': True,
        }
        res = vpnbasesettingapi.add_vpn_policy(**lvpn)
        logger.info(res)
        vpnentry = vpnbasesettingapi.show_tunnelvpnpolicy()
        logger.info(f'vpnentry is :{vpnentry}')
        Assertion.assert_regular(str(vpnentry), "localtunnelvpn", "ERR: Add local tunnel vpn policy failed.")

    def test_02_add_tunnel_vpn_remote(self):
        rvpn = {
            'type': 'tunnel_interface',
            'name': 'remotetunnelvpn',
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
            'keep_alive': True,
        }
        res = r_vpnbasesettingapi.add_vpn_policy(**rvpn)
        logger.info(res)
        vpnentry = r_vpnbasesettingapi.show_tunnelvpnpolicy()
        logger.info(f'vpnentry is :{vpnentry}')
        Assertion.assert_regular(str(vpnentry), 'remotetunnelvpn', "ERR: Add remote tunnel vpn policy failed.")

    @repeat_method(2)
    def test_03_check_tunnel_vpn_status(self):
        time.sleep(10)
        (res, status) = vpnbasesettingapi.get_vpn_status('localtunnelvpn')
        logger.info(f'vpn status:{res},{status}')
        flag = True if res and status == 'up' else False
        Assertion.assert_equal(flag, True, "ERR: check tunnel vpn failed.")

    def test_04_add_access_rule_from_lan_to_vpn_on_local_dut(self):
        access_rule_dict = {
            'name': 'lan_to_vpn',
            'from': 'LAN',
            'to': 'VPN',
            'source_addr': {'any': True},
            'dst_addr': {'any': True},
            'service': {'any': True},
            'action': 'allow',
        }
        output = accessruleipv4api.add_ipv4_access_rule(**access_rule_dict)
        Assertion.assert_equal(output, True, "ERR: add access rule from lan to vpn on local dut failed")

    def test_05_add_access_rule_from_vpn_to_lan_on_remote_dut(self):
        access_rule_dict = {
            'name': 'vpn_to_lan',
            'from': 'VPN',
            'to': 'LAN',
            'source_addr': {'any': True},
            'dst_addr': {'any': True},
            'service': {'any': True},
            'action': 'allow',
        }
        output = r_accessruleipv4api.add_ipv4_access_rule(**access_rule_dict)
        Assertion.assert_equal(output, True, "ERR: add access rule from vpn to lan on remote dut failed")
