from definition.settings import *
from lib.utils import *


class Test_ip_helper_01(Test):
    uuid = "SOSAIOT-TC-56268"
    description = show_testcase_info(Parameter.TESTPLAN, "1", description=True)['title']
    jira = 'GEN7-31901'

    def test_01_00_show_testcase_info(self):
        show_testcase_info('1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_01_add_dmz_addrobj(self):
        obj = {
            'object_type': 'host',
            'name': 'DMZ Host',
            'zone': 'DMZ',
            'value': Parameter.PC2_DMZ_IP
        }
        rc = address_obj.config_addressobject(**obj)
        Assertion.assert_equal(rc, True, "ERR: Add DMZ host address object failed!")

    def test_01_02_add_dhcp_iphelper_policy(self):
        iphelper_dhcp_opt = {
            'protocol': 'DHCP',
            'src': 'X0',
            'dsn': 'DMZ Host',
        }
        rc = iphelper.add_iphelper_policy(**iphelper_dhcp_opt)
        Assertion.assert_equal(rc, True, "ERR: Add dhcp ip helper policy failed!")

    def test_01_03_config_x2(self):
        x2_opt = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X2_DMZ_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.DMZ_GW,
        }
        rc = interface.config_interface(**x2_opt)
        Assertion.assert_equal(rc, True, "ERR: Configure X2 DMZ failed!")

    def test_01_04_test_pc1_dhcp_client(self):
        logger.info("...Test DHCP traffic on PC1 dhcp Client...")
        rc = test_dhcp_traffic(PC='PC1')
        Assertion.assert_equal(rc, True, "ERR: Test DHCP traffic failed!")

    def test_01_05_disable_iphelper(self):
        rc = iphelper.disable_iphelper()
        Assertion.assert_equal(rc, True, "ERR: Disable ip helper failed!")

    def test_01_06_test_pc1_dhcp_client_failed(self):
        rc = test_dhcp_traffic(PC='PC1')
        kill_dhclient(PC='PC1')
        Assertion.assert_equal(rc, False, "ERR: DHCP traffic can still work while ip helper disabled!")

    def test_01_07_del_dhcp_iphelper_policy(self):
        del_json = {
            'protocol': 'DHCP',
            'source': 'X0',
        }
        rc = iphelper.delete_iphelper_policy(**del_json)
        Assertion.assert_equal(rc, True, "ERR: Delete dhcp ip helper policy failed!")


class Test_ip_helper_02(Test):
    uuid = "SOSAIOT-TC-56267"
    description = show_testcase_info(Parameter.TESTPLAN, "2", description=True)['title']
    jira = 'GEN7-31901'

    def test_02_00_show_testcase_info(self):
        cmd = "service network restart"
        pc_ssh = Host('localhost')
        pc_ssh.send_command(cmd)
        show_testcase_info('2')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_02_01_add_dhcp_iphelper_policy(self):
        iphelper_dhcp_json = {
            "ip_helper": {
                "policy": [{
                    "protocol": "DHCP",
                    "source": {
                        "zone": "LAN"
                    },
                    "destination": {
                        "name": "DMZ Host"},
                    "enable": True,
                    "comment": "test"}]
            }
        }
        rc = iphelper.add_policy(**iphelper_dhcp_json)
        Assertion.assert_equal(rc, True, "ERR: Add dhcp iphelper from LAN to DMZ host failed!")

    def test_02_02_enable_iphelper(self):
        rc = iphelper.enable_iphelper()
        Assertion.assert_equal(rc, True, "ERR: Enable ip helper failed!")

    def test_02_03_config_x3(self):
        x3_opt = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': Parameter.MASK,
        }
        rc = interface.config_interface(**x3_opt)
        Assertion.assert_equal(rc, True, "ERR: Configure X3 LAN failed!")

    def test_02_04_add_route_on_pc2(self):
        # add PC3's route on server PC2
        pc2_ssh.send_command('route add -net 3.3.3.0/24 gw {}'.format(Parameter.X2_DMZ_IP))
        out = pc2_ssh.send_command('route -n')
        pc2_ssh.send_command('exit')
        Assertion.assert_regular(out, r'3.3.3.0', "ERR: Add route for remote pc2 failed!")

    def test_02_05_test_pc3_dhcp_client(self):
        logger.info("...Test DHCP traffic on PC3 dhcp Client...")
        rc = test_dhcp_traffic(PC='PC3')
        Assertion.assert_equal(rc, True, "ERR: Test DHCP traffic failed!")

    def test_02_06_test_pc1_dhcp_client(self):
        logger.info("...Test DHCP traffic on PC1 dhcp Client...")
        rc = test_dhcp_traffic(PC='PC1')
        Assertion.assert_equal(rc, True, "ERR: Test DHCP traffic failed!")

    def test_02_08_del_dhcp_iphelper_policy(self):
        del_dhcp = {
            'protocol': 'DHCP',
            'zone': 'LAN'
        }
        rc = iphelper.del_policy(**del_dhcp)
        Assertion.assert_equal(rc, True, "ERR: Delete DHCP ip helper from LAN to DMZ host failed!")

    def test_02_09_test_pc3_dhcp_client_failed(self):
        rc = test_dhcp_traffic(PC='PC3')
        kill_dhclient(PC='PC3')
        Assertion.assert_equal(rc, False, "ERR: Test DHCP traffic failed!")
