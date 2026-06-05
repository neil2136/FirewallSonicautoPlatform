import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/CLI/SSH_With_ECLI_Additions')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/CLI/SSH_With_ECLI_Additions/testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'testcases.SSH_With_ECLI_Additions_TC.Test_01_SSH_With_ECLI_Additions',
        'testcases.SSH_With_ECLI_Additions_TC.Test_02_SSH_With_ECLI_Additions',
        'testcases.SSH_With_ECLI_Additions_TC.Test_03_SSH_With_ECLI_Additions',
        'testcases.SSH_With_ECLI_Additions_TC.Test_04_SSH_With_ECLI_Additions',
        'testcases.SSH_With_ECLI_Additions_TC.Test_05_SSH_With_ECLI_Additions',
        'testcases.SSH_With_ECLI_Additions_TC.Test_06_SSH_With_ECLI_Additions',
        'testcases.SSH_With_ECLI_Additions_TC.Test_07_SSH_With_ECLI_Additions',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
