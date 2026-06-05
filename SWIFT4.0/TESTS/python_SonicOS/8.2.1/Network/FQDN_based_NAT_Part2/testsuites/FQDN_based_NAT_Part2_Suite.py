# __author__: lezhang
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/FQDN_based_NAT_Part2')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_pc.TestSetup_PCs',
        'definition.init_conf_fw.TestConfigFW',
        'testcases.FQDN_based_NAT.TestNegtive_TC12',
        'testcases.FQDN_based_NAT.TestTSR_TC34',
        'testcases.FQDN_based_NAT.TestCLI_TC37',
        'testcases.FQDN_based_NAT.TestCLI_TC39',
        'testcases.FQDN_based_NAT.TestLog_TC40',


    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
