# __author__:cyuan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/CLI/CLI3_Network')


def suite():
    testcases_list = [
        # 'config.init_testbed.TestRestoreDUT',
        # 'config.init_testbed.TestUploadFirmware',
        # 'definition.conf_fw',
        'testcases.network_cli.Test_01_Configure_Interface',
        # 'testcases.network_cli.Test_02_Configure_Zone',
        # 'testcases.network_cli.Test_03_Configure_WLB',
        # 'testcases.network_cli.Test_04_Configure_DHCP_Server',
        # 'testcases.network_cli.Test_05_Add_Address_Object',
        # 'testcases.network_cli.Test_06_Configure_DDNS',
        # 'testcases.network_cli.Test_07_Configure_Route',
        # 'testcases.network_cli.Test_08_Configure_IPHelper',
        # 'testcases.network_cli.Test_09_Configure_NAT_Policy',
        # 'testcases.network_cli.Test_10_Configure_Network_Monitor',
        # 'testcases.network_cli.Test_11_Configure_Interface_IPV6',
        # 'testcases.network_cli.Test_12_Add_Vlan_Interface',
        # 'testcases.network_cli.Test_13_Edit_Vlan_Interface',
        # 'testcases.network_cli.Test_14_Del_Vlan_Interface',
        # 'testcases.network_cli.Test_15_Del_Multi_Vlan_Interface',
        # 'testcases.network_cli.Test_16_Del_All_Vlan_Interface',
        # 'testcases.network_cli.Test_17_Add_Arp_Entry',
        # 'testcases.network_cli.Test_18_Edit_Arp_Entry',
        # 'testcases.network_cli.Test_19_Del_Arp_Entry',
        # 'testcases.network_cli.Test_20_Del_All_Arp_Entry',
        # 'testcases.network_cli.Test_21_Conf_IPv6_Prefix',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
