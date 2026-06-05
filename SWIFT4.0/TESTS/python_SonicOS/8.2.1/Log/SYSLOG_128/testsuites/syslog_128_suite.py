__author__ = 'CHU'
import os
import sys

import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Log')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Log/SYSLOG_128')
print(sys.path)

from testcases.syslog_128 import *

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw',
        'testcases.syslog_128',

    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
