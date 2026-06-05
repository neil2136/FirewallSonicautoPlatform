# __Author__ = 'xzhan'
import sys
import os
import unittest
from logging import Logger
from runner.settings import logger
from runner.unittest.setup import Test
from runner.unittest.suite import UnittestSuite


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/PPPoE_Client/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/PPPoE_Client/definition')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'init_fw',
        'pppoe_setup',
        'pppoe_client.Test_12_Assign_Primary_PPPoE',
        'pppoe_client.Test_13_Assign_Primary_Static_and_Secondary_PPPoE',
        'pppoe_client.Test_14_Assign_both_PPPoE',
        'pppoe_client.Test_19_PPPoE_Inactivity_Connection',
        'pppoe_client.Test_39_Disconnecting_PPPoE_Connection'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
