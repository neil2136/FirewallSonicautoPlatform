# __author__: lezhang
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/Wiremode_Consolidated')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw',
        'definition.init_conf_pc',
        'testcases.wiremode_consolidated.TestBaseFun_TC24',
        # 'testcases.wiremode_consolidated.TestBaseFun_TC33',
        'testcases.wiremode_consolidated.TestBaseFun_TC38',
        'testcases.wiremode_consolidated.TestGUI_TC1',
        'testcases.wiremode_consolidated.TestGUI_TC2',
        'testcases.wiremode_consolidated.TestGUI_TC3',
        'testcases.wiremode_consolidated.TestBaseFun_TC20',
        'testcases.wiremode_consolidated.TestBaseFun_TC22',
        'testcases.wiremode_consolidated.TestBaseFun_TC23',
        'testcases.wiremode_consolidated.TestGUI_TC66',
        'testcases.wiremode_consolidated.TestGUI_TC67',
        'testcases.wiremode_consolidated.TestBaseFun_TC76',
        'testcases.wiremode_consolidated.TestBaseFun_TC80',
        'testcases.wiremode_consolidated.TestBaseFun_TC82',
        # 'testcases.wiremode_consolidated.TestEnhancements_TC27',
        'testcases.wiremode_consolidated.TestEnhancements_TC12',
        'testcases.wiremode_consolidated.TestEnhancements_TC47',
        'testcases.wiremode_consolidated.TestEnhancements_TC72',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
