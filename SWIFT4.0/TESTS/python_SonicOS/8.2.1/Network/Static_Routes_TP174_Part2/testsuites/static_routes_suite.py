# __author__: qshi
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Static_Routes_TP174_Part2/')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_pc.TestInitPCConfig',
        'definition.init_fw.TestInitFWConfig_Dut',
        'definition.init_fw.TestInitFWConfig_Remote',
        'testcases.static_routes.TestStaticRoutes_TC5',
        'testcases.static_routes.TestStaticRoutes_TC8',
        'testcases.static_routes.TestStaticRoutes_TC9'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
