from definition.global_v import *
from lib.Dibbler import *
from lib.utils import *

@paramunittest.parametrized(
    {'tcid': '21', 'uuid': '1530487'},
    {'tcid': '31', 'uuid': '1530490'},
    {'tcid': '32', 'uuid': '1530491'},
    {'tcid': '45', 'uuid': '1530493'},
)
class TestIPv6_DHCP_Server(Test):

    def setParameters(self, tcid, uuid):
        self.uuid = uuid
        self.tcid = tcid
        self.description = show_testcase_info(TESTPLAN, self.tcid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.tcid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Set_X0_IPv6(self):
        x0_opt = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': X0_ipv6,
            'managed': True,
            'other_config': True,
            'router_adv': True,
        }
        if self.tcid == '45':
            x0_opt['managed'] = False
        out = interface_v6_obj.config_interface_ipv6( **x0_opt )
        Assertion.assert_equal(out, True, "ERR: Configure X0 ipv6 Failed!")

    def test_02_Add_DHCPv6_Server_Lease_Scope(self):
        if self.tcid == '31':
            dhcpserver_dict["dhcp_server"]["ipv6"]["scope"]["dynamic"][0]["lifetime"]["preferred"] = 1
        if self.tcid == '45':
            output = dhcpserver_obj.add_dhcp_server_scope_dynamic(**dhcpserver_dict_tc45)
        else:
            output = dhcpserver_obj.add_dhcp_server_scope_dynamic(**dhcpserver_dict)
        Assertion.assert_equal(output, True, "ERR: add dynamic dhcp server scope to X0 failed")

    def test_03_Verify_DHCP_Server(self):
        flag = verify_DHCP_server(self.tcid)
        Assertion.assert_equal(flag, True, f"ERR: testcase {self.tcid} verify DHCPv6 server failed...")

    def test_04_Del_DHCPv6_Server_Lease_Scopes(self):
        ret = dhcpserver_obj.delete_dhcp_server_scope_v6(scope='dynamic', name='test_x0')
        Assertion.assert_equal(ret, True, "ERR: Delete IPv6 DHCP dynamic scope failed.")

    def test_05_Del_X0_IPv6(self):
        x0_opt = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': '',
        }
        out = interface_v6_obj.config_interface_ipv6( **x0_opt )
        Assertion.assert_equal(out, True, "ERR: Del X0 ipv6 Failed!")
