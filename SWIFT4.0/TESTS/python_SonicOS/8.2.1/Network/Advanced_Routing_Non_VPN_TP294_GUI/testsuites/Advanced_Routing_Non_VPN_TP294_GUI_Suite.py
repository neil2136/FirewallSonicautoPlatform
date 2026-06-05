# __author__: lezhang
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/Advanced_Routing_Non_VPN_TP294_GUI')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw.TestConfigFW',
        'testcases.Advanced_Routing.TestGUI_TC01',
        'testcases.Advanced_Routing.TestGUI_TC02',
        'testcases.Advanced_Routing.TestGUI_TC03',
        'testcases.Advanced_Routing.TestGUI_TC05',
        'testcases.Advanced_Routing.TestGUI_TC10',
        'testcases.Advanced_Routing.TestGUI_TC11',
        'testcases.Advanced_Routing.TestGUI_TC12',
        'testcases.Advanced_Routing.TestGUI_TC13',
        'testcases.Advanced_Routing.TestGUI_TC14',
        'testcases.Advanced_Routing.TestGUI_TC16',
        'testcases.Advanced_Routing.TestGUI_TC18',
        'testcases.Advanced_Routing.TestGUI_TC19',
        'testcases.Advanced_Routing.TestGUI_TC21',
        'testcases.Advanced_Routing.TestGUI_TC22',
        'testcases.Advanced_Routing.TestGUI_TC23',
        'testcases.Advanced_Routing.TestGUI_TC24',
        'testcases.Advanced_Routing.TestGUI_TC26',
        'testcases.Advanced_Routing.TestGUI_TC27',
        'testcases.Advanced_Routing.TestGUI_TC28',
        'testcases.Advanced_Routing.TestGUI_TC31',
        'testcases.Advanced_Routing.TestGUI_TC32',
        'testcases.Advanced_Routing.TestGUI_TC35',
        'testcases.Advanced_Routing.TestGUI_TC36',
        'testcases.Advanced_Routing.TestGUI_TC39',
        'testcases.Advanced_Routing.TestGUI_TC40',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
