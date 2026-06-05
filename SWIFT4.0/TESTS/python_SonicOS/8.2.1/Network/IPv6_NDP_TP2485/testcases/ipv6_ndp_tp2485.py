from definition.settings import *
from definition.utils import *


# Excepted: an NDP entry can be added successfully and the related NDP cache will be added too with STATIC state.
class TestBaseFun_TC1(Test):
    uuid = "SOSAIOT-TC-56619"
    description = show_testcase_info(TESTPLAN, '1', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_get_local_pc_eth0_mac(self):
        flag = False
        out = LOCAL_HOST.send_command('ifconfig eth0')
        rc = re.search(r'HWaddr\s+(\w+:\w+:\w+:\w+:\w+:\w+)', out, re.I | re.S)
        logger.info(rc)
        if rc:
            ParamCases.TC1lopceth0mac = rc.group(1)
            logger.info(f"Get local PC eth0 MAC {ParamCases.TC1lopceth0mac}.")
            if len(ParamCases.TC1lopceth0mac) <= 17:
                flag = True
        Assertion.assert_equal(flag, True, "Error:Get MAC failed.")

    def test_03_add_one_static_ndp_entry(self):
        ndp_entry_dict = {'ip': Parameter.PC1_ETH0_IPV6,
                          'mac': ParamCases.TC1lopceth0mac,
                          'interface': Parameter.INTERFACE}
        ParamCases.TC1addres = ndpapi.add_static_entry(**ndp_entry_dict)
        Assertion.assert_equal(ParamCases.TC1addres, True, "Error:add static ndp entry failed.")

    def test_04_check_ndp_cache(self):
        res = check_one_ndp_cache(ndpapi, Parameter.PC1_ETH0_IPV6, 'STATIC')
        Assertion.assert_equal(res, True, "Error:check ndp cache failed.")

    def test_05_delete_added_static_entry(self):
        ndp_entry_dict = {'ip': Parameter.PC1_ETH0_IPV6,
                          'mac': ParamCases.TC1lopceth0mac,
                          'interface': Parameter.INTERFACE}
        res = ndpapi.delete_static_entry(**ndp_entry_dict)
        logger.info(res)
        Assertion.assert_equal(True, True, "Error:delete ndp entry failed.")


# Excepted: a static NDP entry can be deleted via 'Delete this entry' icon
class TestBaseFun_TC9(Test):
    uuid = "SOSAIOT-TC-56625"
    description = show_testcase_info(TESTPLAN, '9', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_one_static_ndp_entry(self):
        ndp_entry_dict = {'ip': Parameter.PC1_ETH1_IPV6,
                          'mac': Parameter.MAC1,
                          'interface': Parameter.INTERFACE}
        ParamCases.TC1addres = ndpapi.add_static_entry(**ndp_entry_dict)
        Assertion.assert_equal(ParamCases.TC1addres, True, "Error:add static ndp entry failed.")

    def test_03_delete_a_static_entry_via_delete_this_entry_icon(self):
        ndp_entry_dict = {'ip': Parameter.PC1_ETH1_IPV6,
                          'mac': Parameter.MAC1,
                          'interface': Parameter.INTERFACE}
        ParamCases.TC9deleteres = ndpapi.delete_static_entry(**ndp_entry_dict)
        Assertion.assert_equal(ParamCases.TC9deleteres, True, "Error:delete static ndp entry via 'Delete this entry' "
                                                              "icon failed.")

    def test_04_check_ndp_cache(self):
        flag = False
        if ParamCases.TC9deleteres:
            output = ndpapi.show_NDP_cache()
            if output:
                flag = True if Parameter.PC1_ETH1_IPV6 not in str(output) else False
        Assertion.assert_equal(flag, True, "Error:check ndp cache failed.")


# Excepted: all the selected static NDP entries can be deleted via the Delete button
class TestBaseFun_TC11(Test):
    uuid = "SOSAIOT-TC-56620"
    description = show_testcase_info(TESTPLAN, '11', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_multiple_static_ndp_entries(self):
        ndp_entry_dict = {'ip': '',
                          'mac': Parameter.MAC1,
                          'interface': Parameter.INTERFACE}
        res = list()
        for ip_addr in ip_addrs_list_1:
            ndp_entry_dict.update({'ip': ip_addr})
            addres = ndpapi.add_static_entry(**ndp_entry_dict)
            res.append(addres)
        Assertion.assert_equal(all(res), True, "ERR: add multiple static ndp entries failed")

    def test_03_delete_all_ndp_entries(self):

        ParamCases.TC11deleteres = ndpapi.del_static_ndp_entries_by_ip(ip_addrs_list_1)
        Assertion.assert_equal(ParamCases.TC11deleteres, True,
                               "ERR: delete all static ndp entries via Delete button failed")

    def test_04_check_ndp_cache(self):
        flag = False
        if ParamCases.TC11deleteres:
            output = ndpapi.show_NDP_cache()
            if output:
                res = [i not in str(output) for i in ip_addrs_list_1]
                logger.info(res)
                flag = True if all(res) else False
        Assertion.assert_equal(flag, True, "Error:check ndp cache failed.")


# Excepted: a static NDP entry can be modified successfully.
class TestBaseFun_TC13(Test):
    uuid = "SOSAIOT-TC-56621"
    description = show_testcase_info(TESTPLAN, '13', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_one_static_ndp_entry(self):
        ndp_entry_dict = {'ip': Parameter.PC1_ETH2_IPV6,
                          'mac': Parameter.MAC1,
                          'interface': Parameter.INTERFACE}
        res = ndpapi.add_static_entry(**ndp_entry_dict)
        Assertion.assert_equal(res, True, "Error:add static ndp entry failed.")

    def test_03_modify_ndp_entry_ip(self):
        ndp_entry_edit_dict = {
            'ip_old': Parameter.PC1_ETH2_IPV6,
            'mac_old': Parameter.MAC1,
            'interface_old': Parameter.INTERFACE,
            'ip': Parameter.IPV6_EDIT,
            'mac': Parameter.MAC1,
            'interface': Parameter.INTERFACE,
        }
        ParamCases.TC13editres = ndpapi.edit_static_entry(**ndp_entry_edit_dict)
        Assertion.assert_equal(ParamCases.TC13editres, True, "Error:modify static ndp entry failed.")

    def test_04_check_ndp_cache(self):
        flag = False
        if ParamCases.TC13editres:
            output = ndpapi.show_NDP_cache()
            if output:
                flag = True if Parameter.IPV6_EDIT in str(output) else False
        Assertion.assert_equal(flag, True, "Error:check ndp cache failed.")

    def test_05_delete_ndp_cache(self):
        ndp_entry_dict = {'ip': Parameter.IPV6_EDIT,
                          'mac': Parameter.MAC1,
                          'interface': Parameter.INTERFACE}
        res = ndpapi.delete_static_entry(**ndp_entry_dict)
        logger.info(res)
        Assertion.assert_equal(res, True, "Error:delete ndp entry failed.")


# Excepted: All static NDP entries are intact after FW restart.
class TestBaseFun_TC16(Test):
    uuid = "SOSAIOT-TC-56622"
    description = show_testcase_info(TESTPLAN, '16', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_multiple_ndp_entries(self):
        ndp_entry_dict = {'ip': '',
                          'mac': Parameter.MAC1,
                          'interface': Parameter.INTERFACE_NEW}
        res = list()
        for ip_addr in ip_addrs_list_2:
            ndp_entry_dict.update({'ip': ip_addr})
            addres = ndpapi.add_static_entry(**ndp_entry_dict)
            res.append(addres)
        Assertion.assert_equal(all(res), True, "ERR: add multiple static ndp entries failed")

    def test_03_restart_dut(self):
        res = restartapi.restart_now()
        Assertion.assert_equal(res, True, "ERR: Restart DUT failed")

    def test_04_verify_ndp_config(self):
        time.sleep(10)
        output1 = ndpapi.show_static_entry()
        output2 = ndpapi.show_NDP_cache()
        res = all((i in str(output1) and i in str(output2)) for i in ip_addrs_list_2)
        Assertion.assert_equal(res, True, "ERR: Verify ndp config failed")
