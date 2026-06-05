from settings import *
from utils import *


class Test_1_wg0_interface_edit_4(Test):
    uuid = "SOSAIOT-TC-89268"
    description = show_testcase_info(TESTPLAN,
                                     "4", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_edit_wireguard_tunnel(self):
        editresult = False
        showwg = wgtunnelinterface.show_wireguard_tunnel()
        logger.info('show_wireguard_tunnel: {}'.format(showwg))
        try:
            wg0 = showwg['tunnel_interfaces'][0]['wireguard']
            if wg0['private_key'] and wg0['public_key']:
                wg_tunnel_edit_dict['private_key'] = wg0['private_key']
                wg_tunnel_edit_dict['public_key'] = wg0['public_key']
                editresult = wgtunnelinterface.edit_wireguard_tunnel(**wg_tunnel_edit_dict)

                # init wg0 interface
                wg_tunnel_edit_dict['ip'] = WG0_Tunnel_IP
                wgtunnelinterface.edit_wireguard_tunnel(**wg_tunnel_edit_dict)
                logger.info('init fw edit_wireguard_tunnel: {}'.format(showwg))
            else:
                logger.error('private_key or public_key is empty.')
        except:
            logger.error('Can not get the wg0 tunnel interface information.')
        Assertion.assert_equal(editresult, True, "ERR: edit wg0 tunnel interface failed")


class Test_2_wg_global_settings_enable_22(Test):
    uuid = "SOSAIOT-TC-89250"
    description = show_testcase_info(TESTPLAN,
                                     "22", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '22')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_enable_disable_wg_settings(self):
        wg_base_setting_dict['enable'] = False
        rs = wgbasesetting.edit_base_setting(**wg_base_setting_dict)
        logger.info(rs)
        disableresult = wgbasesetting.show_base_status()
        if not disableresult['wireguard']['enable']:
            wg_base_setting_dict['enable'] = True
            wgbasesetting.edit_base_setting(**wg_base_setting_dict)
            enableresult = wgbasesetting.show_base_status()
            output = True if enableresult['wireguard']['enable'] else False
        else:
            logger.error('disable wg failed. ')
            output = False
        Assertion.assert_equal(output, True, "ERR: edit wg0 tunnel interface failed")


class Test_3_add_wg_peer_valid_name_31(Test):
    uuid = "SOSAIOT-TC-89259"
    description = show_testcase_info(TESTPLAN,
                                     "31", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '31')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_valid_name_check(self):
        addresult = True
        for name in wg_valid_name_list:
            wgpeerbasesetting.del_all_peers()
            wg_peer_dict['name'] = name
            result = wgpeerbasesetting.add_wireguard_peer(**wg_peer_dict)
            if not result:
                addresult = False
                logger.error('add wg peer fail named {}. it\'s not expected'.format(name))
        Assertion.assert_equal(addresult, True, "ERR: check valid name for wg peer failed")

    def test_02_invalid_name_check(self):
        addresult = True
        for name in wg_invalid_name_list:
            wgpeerbasesetting.del_all_peers()
            wg_peer_dict['name'] = name
            result = wgpeerbasesetting.add_wireguard_peer(**wg_peer_dict)
            if result:
                addresult = False
                logger.error('add wg peer successful named {}, it\'s not expected.'.format(name))

        # init fw configure and data value
        delresult = wgpeerbasesetting.del_all_peers()
        logger.info(delresult)
        wg_peer_dict['name'] = 'autotest10'
        Assertion.assert_equal(addresult, True, "ERR: check invalid name for wg peer failed")

# case 41 52 53 59 60 are executed as a whole
class Test_4_export_wireguard_peer_41(Test):
    uuid = "SOSAIOT-TC-89270"
    description = show_testcase_info(TESTPLAN,
                                     "41", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '41')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_export_wireguard_peer(self):
        global g_wgexport
        # init fw configure settings
        wgset = wgbasesetting.edit_base_setting(**wg_base_setting_dict)
        logger.info('init fw edit_base_setting: {}'.format(wgset))
        wgdel = wgpeerbasesetting.del_all_peers()
        logger.info('init fw del_all_peers: {}'.format(wgdel))

        result = wgpeerbasesetting.add_wireguard_peer(**wg_peer_dict)
        logger.info('add_wireguard_peer: {}'.format(result))
        g_wgexport = wgpeerbasesetting.export_wireguard_peer(wg_peer_dict['name'])
        logger.info('export_wireguard_peer: {}'.format(g_wgexport))

        output = True if wg_peer_dict['ip'] in g_wgexport else False
        Assertion.assert_equal(output, True, "ERR: export wireguard peer failed")


class Test_5_allow_any_address_access_52(Test):
    uuid = 'F8A9839C-2C91-11EC-AECA-DFAC22677C13'
    description = show_testcase_info(TESTPLAN,
                                     "52", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '52')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_setup_vpn_client(self):
        confresult = Setupwg0ForPC2(g_wgexport)
        output = True if confresult else False
        Assertion.assert_equal(output, True, "ERR: setup Wireguard configure in FW and PC2 fail")

    @repeat_method(3)
    def test_02_inbound_traffic_check(self):
        output = Checkwg0Traffic(PC1_ETH0_IP)
        Assertion.assert_equal(output, True, "ERR: check ping from wan host to lan host failed")


class Test_6_customer_added_address_access_53(Test):
    uuid = 'F8AAF060-2C91-11EC-AECA-DFAC22677C13'
    description = show_testcase_info(TESTPLAN,
                                     "53", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '53')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    @repeat_method(3)
    def test_01_inbound_ip_address_check(self):
        wg_base_setting = {'allowedipsname': address_object1['name']}
        editwg = wgbasesetting.edit_base_setting(**wg_base_setting)
        if editwg:
            output = Checkwg0Traffic(PC1_ETH0_IP)
        else:
            output = False
            logger.error('edit Choose network from list to {} fail'.format(address_object1['name']))
        Assertion.assert_equal(output, True, "ERR: check outbound ip address access failed")

    def test_03_outbound_ip_address_check(self):
        wg_base_setting = {'allowedipsname': address_object2['name']}
        editwg = wgbasesetting.edit_base_setting(**wg_base_setting)
        if editwg:
            output = Checkwg0Traffic(PC1_ETH0_IP)
        else:
            output = True
            logger.error('edit Choose network from list to {} fail'.format(address_object2['name']))
        Assertion.assert_equal(output, False, "ERR: check outbound ip address access failed")


class Test_7_restart_wireguard_configure_check_59(Test):
    uuid = "SOSAIOT-TC-89283"
    description = show_testcase_info(TESTPLAN,
                                     "59", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '59')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_restart_check(self):
        global g_wgaccess
        # init fw configure settings
        editst = wgbasesetting.edit_base_setting(**wg_base_setting_dict)
        logger.info('edit_base_setting: {}'.format(editst))

        rst = restartfw.restart_now()
        if rst:
            showresult = wgpeerbasesetting.show_wireguard_peer()
            output = True if showresult else False
            if output:
                g_wgaccess = Checkwg0Traffic(PC1_ETH0_IP)
        else:
            logger.error('restart fw failed.')
            output = False
        Assertion.assert_equal(output, True, "ERR: check Wireguard configure in FW after restart failed.")


class Test_8_restart_access_check_60(Test):
    uuid = "SOSAIOT-TC-89285"
    description = show_testcase_info(TESTPLAN,
                                     "60", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '60')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_setup_wg0_for_pc2(self):
        Assertion.assert_equal(g_wgaccess, True, "ERR: check Wireguard access in FW after restart failed.")