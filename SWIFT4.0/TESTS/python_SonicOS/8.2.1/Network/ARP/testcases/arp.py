from parameter import *
import utils


class Test_01_Add_Interface_02(Test):
    """
    1. insure no cache at first.
    2. add interface or ping to generate ARP cache.
    3. verify them in arp cahce table.
    """
    uuid = "SOSAIOT-TC-55771"
    description = show_testcase_info(Parameter.TESTPLAN,
                                     "01", description=True)['title']
    def test_00_initial_parameter(self):
        Parameter.X2_MAC = interface.get_interface_mac('x2')
        logger.info(Parameter.X2_MAC)
        Parameter.DMZ_HOST_MAC = utils.get_pc2_mac("eth0")
        logger.info(Parameter.DMZ_HOST_MAC)

    def test_01_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_01_unassign_interface(self):
        output = interface.unassign_interface(interface="X2")
        Assertion.assert_equal(output, True, "ERR: unassign X2 failed")

    def test_01_02_check_arp_cache_x2_fail(self):
        output = arpApi.show_arp_caches()
        logger.info(output)
        Assertion.assert_not_regular(str(output), Parameter.X2_MAC,
                                    "ERR: Can found X2_MAC in arp cache")

    def test_01_03_config_x2_interface(self):
        x2_static_opt = {
           'if': 'x2',
           'zone': 'DMZ',
           'mode': 'static',
           'ip': Parameter.X2_IP,
           'netmask': '255.255.255.0',
           'gateway': '0.0.0.0',
           'mgmt_http': False,
        }
        output = interface.config_interface(**x2_static_opt)
        logger.info(output)
        Assertion.assert_equal(output, True, "ERR: Config X2 to static failed")

    def test_01_04_check_arp_cache_pass(self):
        output = arpApi.show_arp_caches()
        logger.info(output)
        Assertion.assert_regular(str(output), Parameter.X2_MAC,
                                 "ERR: Cannot found X2_MAC in arp cache")

    def test_01_05_check_arp_cache_host_fail(self):
        output = arpApi.show_arp_caches()
        logger.info(output)
        Assertion.assert_not_regular(str(output), Parameter.DMZ_HOST_MAC,
                                     "ERR: Can found DMZ_HOST_MAC in arp cache")

    def test_01_06_check_arp_cache_host_pass(self):
        PC2.ping(Parameter.X2_IP)
        output = arpApi.show_arp_caches()
        logger.info(output)
        Assertion.assert_regular(str(output), Parameter.DMZ_HOST_MAC,
                                 "ERR: Cannot found DMZ_HOST_MAC in arp cache")


class Test_02_Delete_ARP_03(Test):
    """
    1. insure exist cache at first.
    2. unassign interface.
    3. verify cache disappeared.
    """
    uuid = "SOSAIOT-TC-55780"
    description = show_testcase_info(Parameter.TESTPLAN,
                                     "02", description=True)['title']

    def test_02_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '02')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_01_config_x2_interface(self):
        x2_static_opt = {
           'if': 'x2',
           'zone': 'DMZ',
           'mode': 'static',
           'ip': Parameter.X2_IP,
           'netmask': '255.255.255.0',
           'gateway': '0.0.0.0',
           'mgmt_http': False,
        }
        output = interface.config_interface(**x2_static_opt)
        logger.info(output)
        Assertion.assert_equal(output, True, "ERR: Config X2 to static failed")

    def test_02_02_check_arp_cache_pass(self):
        output = arpApi.show_arp_caches()
        logger.info(output)
        Assertion.assert_regular(str(output), Parameter.X2_MAC,
                                 "ERR: Cannot found X2_MAC in arp cache")

    def test_02_03_unassign_interface(self):
        output = interface.unassign_interface(interface="X2")
        logger.info(output)
        Assertion.assert_equal(output, True, "ERR: unassign X2 failed")

    def test_02_04_check_arp_cache_x2_fail(self):
        output = arpApi.show_arp_caches()
        logger.info(output)
        Assertion.assert_not_regular(str(output), Parameter.X2_MAC,
                                     "ERR: Can found X2_MAC in arp cache")


class Test_03_Edit_ARP_16(Test):
    """
    1. set one static incorrect entry
    2. ping fail
    3. edit entry as correct one
    4. ping pass
    """
    uuid = "SOSAIOT-TC-55767"
    description = show_testcase_info(Parameter.TESTPLAN,
                                     "03", description=True)['title']

    def test_03_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '03')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_03_01_config_x2_interface(self):
        x2_static_opt = {
           'if': 'x2',
           'zone': 'DMZ',
           'mode': 'static',
           'ip': Parameter.X2_IP,
           'netmask': '255.255.255.0',
           'gateway': '0.0.0.0',
           'mgmt_http': False,
           'mgmt_ping': True,
        }
        output = interface.config_interface(**x2_static_opt)
        Assertion.assert_equal(output, True, "ERR: Config X2 to static failed")

    def test_03_02_add_static_arp(self):

        static_arp = {
            'ip': Parameter.DMZ_HOST,
            'mac': '22:22:33:44:55:66',
            'interface': 'X2',
            'publish': False,
            'bind_mac': False,
        }
        output = arpApi.add_static_arp(**static_arp)
        Assertion.assert_equal(output, True, "add static ARP entry failed")

    def test_03_03_check_arp_entry_pass(self):
        output = arpApi.show_static_arp_entries()
        Assertion.assert_regular(str(output), Parameter.DMZ_HOST,
                                 "ERR: Cannot found DMZ_HOST in arp cache")

    def test_03_04_ping_interface_fail(self):
        output = PC2.ping(Parameter.X2_IP)
        Assertion.assert_equal(output, False, "can ping X2 success")
#        output = utils.verify_icmp_reply(Parameter.DMZ_HOST, Parameter.DMZ_HOST_MAC)
#        Assertion.assert_equal(output, False, "can ping X2 success")

    def test_03_05_edit_arp_entry(self):
        edit_arp = {
            'raw_ip': Parameter.DMZ_HOST,
            'raw_mac': '222233445566',
            'raw_interface': 'X2',
            'raw_publish': False,
            'raw_bind_mac': False,
            'ip': Parameter.DMZ_HOST,
            'mac': Parameter.DMZ_HOST_MAC,
            'interface': 'X2',
            'publish': False,
            'bind_mac': False,
        }
        output = arpApi.edit_static_arp(**edit_arp)
        Assertion.assert_equal(output, True, "edit static ARP entry failed")

    def test_03_06_ping_interface_pass(self):
        output = PC2.ping(Parameter.X2_IP)
        Assertion.assert_equal(output, True, "cannot ping X2 success")
#        output = utils.verify_icmp_reply(Parameter.DMZ_HOST, Parameter.DMZ_HOST_MAC)
#        Assertion.assert_equal(output, True, "cann't ping X2 success")

    def test_03_07_delete_arp_entry(self):
        del_static = {
            'ip': Parameter.DMZ_HOST,
            'mac': Parameter.DMZ_HOST_MAC,
            'interface': 'X2',
            'publish': False,
            'bind_mac': False,
        }
        output = arpApi.del_static_arp(**del_static)
        Assertion.assert_equal(output, True, "del static arp entry failed")


class Test_04_Bind_MAC_20(Test):
    """
    1. add static correct arp entry
    2. client ping interface pass
    3. change PC ip address
    4. client ping interface pass
    5. edit static arp entry with bind-mac feature
    6. client ping interface fail
    7. client change ip back
    8. client ping interface pass
    """
    uuid = "SOSAIOT-TC-55772"
    description = show_testcase_info(Parameter.TESTPLAN,
                                     "04", description=True)['title']
    
    def test_04_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '04')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_04_01_config_x2_interface(self):
        x2_static_opt = {
           'if': 'x2',
           'zone': 'DMZ',
           'mode': 'static',
           'ip': Parameter.X2_IP,
           'netmask': '255.255.255.0',
           'gateway': '0.0.0.0',
           'mgmt_http': False,
           'mgmt_ping': True,
        }
        output = interface.config_interface(**x2_static_opt)
        Assertion.assert_equal(output, True, "ERR: Config X2 to static failed")

    def test_04_02_add_static_arp(self):
        static_arp = {
            'ip': Parameter.DMZ_HOST,
            'mac': Parameter.DMZ_HOST_MAC,
            'interface': 'X2',
            'publish': False,
            'bind_mac': False,
        }
        output = arpApi.add_static_arp(**static_arp)
        Assertion.assert_equal(output, True, "add static ARP entry failed")

    def test_04_03_check_arp_entry_pass(self):
        output = arpApi.show_static_arp_entries()
        Assertion.assert_regular(str(output), Parameter.DMZ_HOST,
                                 "ERR: Cannot found DMZ_HOST in arp cache")

    def test_04_04_ping_interface_pass(self):
        output = PC2.ping(Parameter.X2_IP)
        Assertion.assert_equal(output, True, "cannot ping X2 success")

    def test_04_05_change_ip_ping_interface_pass(self):
        utils.change_pc2_ip('eth0', '172.16.1.100')
        output = PC2.ping(Parameter.X2_IP)
        Assertion.assert_equal(output, True, "cannot ping X2 success")

    def test_04_06_edit_arp_entry(self):
        edit_arp = {
            'raw_ip': Parameter.DMZ_HOST,
            'raw_mac': Parameter.DMZ_HOST_MAC,
            'raw_interface': 'X2',
            'raw_publish': False,
            'raw_bind_mac': False,
            'ip': Parameter.DMZ_HOST,
            'mac': Parameter.DMZ_HOST_MAC,
            'interface': 'X2',
            'publish': False,
            'bind_mac': True,
        }
        output = arpApi.edit_static_arp(**edit_arp)
        Assertion.assert_equal(output, True, "edit static ARP entry failed")

    def test_04_07_ping_interface_fail(self):
        utils.change_pc2_ip('eth0', '172.16.1.100')
        output = PC2.ping(Parameter.X2_IP)
        Assertion.assert_equal(output, False, "can ping X2 success")

    def test_04_08_delete_arp_entry(self):
        del_static = {
            'ip': Parameter.DMZ_HOST,
            'mac': Parameter.DMZ_HOST_MAC,
            'interface': 'X2',
            'publish': False,
            'bind_mac': True,
        }
        output = arpApi.del_static_arp(**del_static)
        Assertion.assert_equal(output, True, "del static arp entry failed")

    def test_04_09_restore_ip_interface(self):
        utils.change_pc2_ip('eth0', Parameter.DMZ_HOST)
        output = PC2.ping(Parameter.X2_IP)
        Assertion.assert_equal(output, True, "cannot ping X2 success")


class Test_05_Delete_Static_ARP_23(Test):
    " cannot delete static ARP entry"

    uuid = "SOSAIOT-TC-55774"
    description = show_testcase_info(Parameter.TESTPLAN,
                                     "05", description=True)['title']
    jira = "GEN7-32380"
    
    def test_05_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '05')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_05_01_config_x2_interface(self):
        x2_static_opt = {
           'if': 'x2',
           'zone': 'DMZ',
           'mode': 'static',
           'ip': Parameter.X2_IP,
           'netmask': '255.255.255.0',
           'gateway': '0.0.0.0',
           'mgmt_http': False,
           'mgmt_ping': True,
        }
        output = interface.config_interface(**x2_static_opt)
        Assertion.assert_equal(output, True, "ERR: Config X2 to static failed")

    def test_05_02_add_static_arp(self):
        static_arp = {
            'ip': Parameter.DMZ_HOST,
            'mac': Parameter.DMZ_HOST_MAC,
            'interface': 'X2',
            'publish': False,
            'bind_mac': False,
        }
        output = arpApi.add_static_arp(**static_arp)
        Assertion.assert_equal(output, True, "add static ARP entry failed")

    def test_05_03_check_arp_entry_pass(self):
        output = arpApi.show_static_arp_entries()
        Assertion.assert_regular(str(output), Parameter.DMZ_HOST,
                                 "ERR: Cannot found DMZ_HOST in arp cache")

    def test_05_04_delete_static_cache_fail(self):
        output = arpApi.delete_arp_cache(Parameter.DMZ_HOST, 'X2')
        Assertion.assert_equal(output, False, "ERR: Can delete static arp cache")

    def test_05_05_delete_arp_entry(self):
        del_static = {
            'ip': Parameter.DMZ_HOST,
            'mac': Parameter.DMZ_HOST_MAC,
            'interface': 'X2',
            'publish': False,
            'bind_mac': False,
        }
        output = arpApi.del_static_arp(**del_static)
        Assertion.assert_equal(output, True, "del static arp entry failed")




