from definition.settings import *
from definition.utils import *


class TestInitConfig(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_x1(self):
        logger.info("config x1 interface... ")
        rc = interface_api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    @repeat_method(10)
    def test_02_register_fw(self):
        rc = license_cli.register("online")
        if not rc:
            time.sleep(20)
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_03_config_remote_fw(self):
        logger.info('Restore Remote FW...')
        path = os.environ["PYTHON_COMMON_HOME"] + \
            '/config/restore_gw_rmt_tel.py'
        command1 = f'python3 {path} -os=1 --testbed={Params.testbed} -device=RemoteGEN5 -if=X1 -zone=WAN -ip={Parameter.R_X1_IP} -restore=1'
        confres = LAN_HOST.send_command(command1)
        logger.info(confres)
        flag = True if confres else False
        Assertion.assert_equal(flag, True, "ERR: Config Remote FW failed")

    def test_04_ping_from_lan_host_to_remote_fw_x1(self):
        logger.info("add a route to interface X1 sub... ")
        command = f'route add -net {Parameter.X1_SUBNET} gw {Parameter.X0_IP}'
        output = LAN_HOST.send_command(command)
        logger.info('add x1 sub route in PC1 result: {}'.format(output))
        pingres = LAN_HOST.ping_from_eth(r_ip, eth='eth1')
        Assertion.assert_equal(pingres, True, "ERR: ping from lan to remote_x1 failed")

    def test_05_config_remote_x2(self):
        logger.info("config remote x2 interface... ")
        time.sleep(5)
        rc = r_interface_api.config_interface(**r_x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config remote X2 to static failed")

    def test_06_add_remote_network_object(self):
        rc = r_ao_api.config_addressobject(**remote_vpn_lan)
        Assertion.assert_equal(rc, True, "ERR: Add remote network AO failed")

    def test_07_add_central_and_remote_vpn_policies(self):
        rc = centralvpnapi.add_vpn_policy(**s2svpn_main_central_vpn)
        rc &= remotevpnapi.add_vpn_policy(**s2svpn_main_remote_vpn)
        Assertion.assert_equal(rc, True, "ERR: Add vpn policies failed")

    def test_08_remove_remote_dhcp_server(self):
        rc = rdhcpserverapi.delete_dhcp_server_scope_v4('dynamic', Parameter.R_X0_IP_START, Parameter.R_X0_IP_END)
        Assertion.assert_equal(rc, True, "ERR: Remove DHCP on remote GW failed.")

    def test_09_change_central_log_level(self):
        editdict = {
            "log": {
                "group": [
                    {
                        "id": 30,
                        "name": "DHCP Relay",
                        "log_monitor": {
                            "type": "enabled",
                            "redundancy_interval": {}
                        },
                    }
                ]
            }
        }
        logsetres = logcategapi.logging_level(level='debug')
        logsetres &= logcategapi.edit_log_category_groups_by_id(30, **editdict)
        Assertion.assert_equal(logsetres, True, "ERR: Change central log level failed.")

    def test_10_disable_and_enable_remote_vpn_policy(self):
        res = remotevpnapi.edit_vpn_policy(**s2svpn_main_remote_vpn_disable)
        time.sleep(3)
        res &= remotevpnapi.edit_vpn_policy(**s2svpn_main_remote_vpn_enable)
        Assertion.assert_equal(res, True, "ERR: Re-negociate remote VPN policy failed.")

