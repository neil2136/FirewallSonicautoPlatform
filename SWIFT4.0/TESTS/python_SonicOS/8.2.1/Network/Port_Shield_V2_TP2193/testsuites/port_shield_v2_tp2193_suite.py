# __author__: cyuan

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ['PYTHON_COMMON_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] +
                '/Network/Port_Shield_V2_TP2193')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'testcases.port_shield_v2_tp2193.TestPortShield_TC2',
        'testcases.port_shield_v2_tp2193.TestPortShield_TC15',
        'testcases.port_shield_v2_tp2193.TestPortShield_TC17',
        'testcases.port_shield_v2_tp2193.TestPortShield_TC6',
        'testcases.port_shield_v2_tp2193.TestPortShield_TC7',
        'testcases.port_shield_v2_tp2193.TestPortShield_TC12',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
