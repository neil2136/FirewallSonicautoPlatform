# __author__: cyuan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ['PYTHON_COMMON_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/NAT_HA_and_Load_Balancing_TP1381')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        "definition.init_config_fw",
        "definition.init_config_pc",
        'testcases.nat_ha.Test_NAT_HA_TC01',
        'testcases.nat_ha.Test_NAT_HA_TC03',
        'testcases.nat_ha.Test_NAT_HA_TC04',
        'testcases.nat_ha.Test_NAT_HA_TC05',
        'testcases.nat_ha.Test_NAT_HA_TC07',
        'testcases.nat_ha.Test_NAT_HA_TC48',
        'testcases.nat_ha.Test_NAT_HA_TC49',
        'testcases.nat_ha.Test_NAT_HA_TC14',
        'testcases.nat_ha.Test_NAT_HA_TC17',
        'testcases.nat_ha.Test_NAT_HA_TC18',
        'testcases.nat_ha.Test_NAT_HA_TC19',
        'testcases.nat_ha.Test_NAT_HA_TC22',
        'testcases.nat_ha.Test_NAT_HA_TC23',
        'testcases.nat_ha.Test_NAT_HA_TC25',
        'testcases.nat_ha.Test_NAT_HA_TC26',
        'testcases.nat_ha.Test_NAT_HA_TC27',
        'testcases.nat_ha.Test_NAT_HA_TC02',
        'testcases.nat_ha.Test_NAT_HA_TC29',
        'testcases.nat_ha.Test_NAT_HA_TC32',
        'testcases.nat_ha.Test_NAT_HA_TC35',
        'testcases.nat_ha.Test_NAT_HA_TC36'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
