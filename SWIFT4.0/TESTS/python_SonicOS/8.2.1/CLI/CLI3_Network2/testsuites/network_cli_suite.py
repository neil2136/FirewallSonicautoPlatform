import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/CLI/CLI3_Network2')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw',
        'testcases.network_cli.config_interface',
        'testcases.network_cli.Test_01_Configure_Vlan_Interface',
        'testcases.network_cli.Test_02_Edit_Vlan_Interface',
        'testcases.network_cli.Test_03_Delete_Vlan_Interface',
        'testcases.network_cli.Test_04_Delete_multiple_Vlan_Interfaces',
        'testcases.network_cli.Test_05_Delete_All_Vlan_Interfaces',
        'testcases.network_cli.Test_06_Add_ARP_entries',
        'testcases.network_cli.Test_07_Edit_ARP_entries',
        'testcases.network_cli.Test_08_Delete_ARP_entry',
        'testcases.network_cli.Test_09_Delete_all_ARP_entry',


    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'ftahreen@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(), to_users)
    st.run()
