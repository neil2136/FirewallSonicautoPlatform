import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/CLI/CLI_TP811')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'testcase.cli_tp811.Test_CLI_1',
        'testcase.cli_tp811.Test_CLI_12',
        'testcase.cli_tp811.Test_CLI_22',
        'testcase.cli_tp811.Test_CLI_23',
        'testcase.cli_tp811.Test_CLI_26',
        'testcase.cli_tp811.Test_CLI_27',
        'testcase.cli_tp811.Test_CLI_40',
        'testcase.cli_tp811.Test_CLI_41',
        'testcase.cli_tp811.Test_CLI_47',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()