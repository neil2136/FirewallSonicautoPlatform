# __author__: cyuan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ['PYTHON_COMMON_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/DHCP_Server_ENH_Part2')


def suite():
    testcase_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_config_fw',
        "testcases.dhcp_server_enhance_part2.Test_DHCP_Server_TC1525154",
        "testcases.dhcp_server_enhance_part2.Test_DHCP_Server_TC1525165",
        "testcases.dhcp_server_enhance_part2.Test_DHCP_Server_TC1525166",
        "testcases.dhcp_server_enhance_part2.Test_DHCP_Server_TC1525168",
        "testcases.dhcp_server_enhance_part2.Test_DHCP_Server_TC1525172",
        "testcases.dhcp_server_enhance_part2.Test_DHCP_Server_TC1525174",
        "testcases.dhcp_server_enhance_part2.Test_DHCP_Server_TC1525175",
        "testcases.dhcp_server_enhance_part2.Test_DHCP_Server_TC1525179",
        "testcases.dhcp_server_enhance_part2.Test_DHCP_Server_TC1525180",
        "testcases.dhcp_server_enhance_part2.Test_DHCP_Server_TC1525139",
        "testcases.dhcp_server_enhance_part2.Test_DHCP_Server_TC1525141",
        "testcases.dhcp_server_enhance_part2.Test_DHCP_Server_TC1525146",
        "testcases.dhcp_server_enhance_part2.Test_DHCP_Server_TC1525147",
        "testcases.dhcp_server_enhance_part2.Test_DHCP_Server_TC1525148",
        # persistence part
        "testcases.dhcp_server_persistence_part2.Test_DHCP_Persistence_TC1825685",
        "testcases.dhcp_server_persistence_part2.Test_DHCP_Persistence_TC1825686",
        "testcases.dhcp_server_persistence_part2.Test_DHCP_Persistence_TC1825688",
        "testcases.dhcp_server_persistence_part2.Test_DHCP_Persistence_TC1825690",
        "testcases.dhcp_server_persistence_part2.Test_DHCP_Persistence_TC1825689",
        "testcases.dhcp_server_persistence_part2.Test_DHCP_Persistence_TC1825687",
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcase_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
