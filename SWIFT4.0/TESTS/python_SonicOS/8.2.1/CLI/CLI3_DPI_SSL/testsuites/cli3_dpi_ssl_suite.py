#_Author_ = 'xpeng'
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] + '/CLI/CLI3_DPI_SSL')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw',
        'testcases.cli3_dpi_ssl'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
