# Author: xzhan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/Interfaces_TP168_Part3')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_fw_configure.TestConfigFW',
        'testcases.Interfaces_TP168_Part3.Test_Default_columns',
        'testcases.Interfaces_TP168_Part3.TestDefault_columns_001',
        'testcases.Interfaces_TP168_Part3.TestDefault_columns_002',
        'testcases.Interfaces_TP168_Part3.TestLAN_1515730',
        'testcases.Interfaces_TP168_Part3.TestLAN_1515727',
        'testcases.Interfaces_TP168_Part3.TestLAN_1515728',
        'testcases.Interfaces_TP168_Part3.TestLAN_1515732',
        'testcases.Interfaces_TP168_Part3.TestWAN_1515741',
        'testcases.Interfaces_TP168_Part3.TestWAN_1515747',
        'testcases.Interfaces_TP168_Part3.TestWAN_1515756',
        'testcases.Interfaces_TP168_Part3.TestWAN_1515757',
        'testcases.Interfaces_TP168_Part3.TestWAN_1515758',
        'testcases.Interfaces_TP168_Part3.TestWAN_1515762',
        'testcases.Interfaces_TP168_Part3.TestWAN_1515764',
        'testcases.Interfaces_TP168_Part3.TestWAN_1515765',
        'testcases.Interfaces_TP168_Part3.TestError_1515752',
        'testcases.Interfaces_TP168_Part3.TestError_1515763',
        'testcases.Interfaces_TP168_Part3.TestCommon_1533417',
        'testcases.Interfaces_TP168_Part3.TestCommon_3585634',
        'testcases.Interfaces_TP168_Part3.TestCommon_1515776',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
