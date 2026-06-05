# __author__: qshi
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/Guest_Services_For_Non_Wireless_Zones_TP2379/')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_pc.TestInitPCConfig',
        'definition.init_pc.Test_SetupMail_Server',
        'definition.init_fw.TestConfigFW',
        'testcases.Guest_Service_TP2379',
        'testcases.Guest_Service_Part2',
        'testcases.Guest_Service_smtp',
]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
