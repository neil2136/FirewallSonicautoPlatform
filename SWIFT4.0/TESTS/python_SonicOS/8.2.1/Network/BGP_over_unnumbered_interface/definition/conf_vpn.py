from definition.settings import *


class TestSetupVPN(Test):
    uuid = 'NonTC'
    goto_teardown = True


    def test_01_add_tunnle_vpn_policy_on_local_dut(self):
        lvpn_dict = copy.deepcopy(vpn_policy_dict)
        lvpn_dict.update({'name': Parameter.LOCAL_VPN_NAME, 'pri_gate': Parameter.X1_REMOTE_IP})
        res = vpnbasesettingapi.add_vpn_policy(**lvpn_dict)
        logger.info(res)
        vpnentry = vpnbasesettingapi.show_tunnelvpnpolicy()
        logger.info(f'vpnentry is :{vpnentry}')
        Assertion.assert_regular(str(vpnentry), Parameter.LOCAL_VPN_NAME, "ERR: Add local tunnel vpn policy failed.")

    def test_02_add_tunnle_vpn_policy_on_remote_dut(self):
        rvpn_dict = copy.deepcopy(vpn_policy_dict)
        rvpn_dict.update({'name': Parameter.REMOTE_VPN_NAME, 'pri_gate': Parameter.X1_IP})
        res = r_vpnbasesettingapi.add_vpn_policy(**rvpn_dict)
        logger.info(res)
        vpnentry = r_vpnbasesettingapi.show_tunnelvpnpolicy()
        logger.info(f'vpnentry is :{vpnentry}')
        Assertion.assert_regular(str(vpnentry), Parameter.REMOTE_VPN_NAME, "ERR: Add remote tunnel vpn policy failed.")

    @repeat_method(2)
    def test_03_check_local_vpn_status(self):
        time.sleep(10)
        (res, status) = vpnbasesettingapi.get_vpn_status(Parameter.LOCAL_VPN_NAME)
        logger.info(f'vpn status:{res},{status}')
        flag = True if res and status == 'up' else False
        Assertion.assert_equal(flag, True, "ERR: check local vpn status failed.")

    @repeat_method(2)
    def test_04_check_remote_vpn_status(self):
        time.sleep(10)
        (res, status) = r_vpnbasesettingapi.get_vpn_status(Parameter.REMOTE_VPN_NAME)
        logger.info(f'vpn status:{res},{status}')
        flag = True if res and status == 'up' else False
        Assertion.assert_equal(flag, True, "ERR: check remote vpn status failed.")

   
