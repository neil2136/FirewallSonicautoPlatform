# __author__: lezhang
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/Advanced_Routing_TP294_RIP')


def suite():
    testcases_list = [
        'definition.init_conf_fw.TestinitRemoteFW.test_01_init_remote_fw_via_asyncio',
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw.TestConfigFW_Local',
        'definition.init_conf_fw.TestConfigFW_Remote',
        'testcases.Advanced_Routing.TestRIP_TC72',
        'testcases.Advanced_Routing.TestRIP_TC71',
        'testcases.Advanced_Routing.TestRIP_TC47',
        'testcases.Advanced_Routing.TestRIP_TC48',
        'testcases.Advanced_Routing.TestRIP_TC49',
        'testcases.Advanced_Routing.TestRIP_TC50',
        'testcases.Advanced_Routing.TestRIP_TC51',
        'testcases.Advanced_Routing.TestRIP_TC52',
        'testcases.Advanced_Routing.TestRIP_TC53',
        'testcases.Advanced_Routing.TestRIP_TC54',
        'testcases.Advanced_Routing.TestRIP_TC55',
        'testcases.Advanced_Routing.TestRIP_TC56',
        'testcases.Advanced_Routing.TestRIP_TC58',
        'testcases.Advanced_Routing.TestRIP_TC60',
        'testcases.Advanced_Routing.TestRIP_TC62',
        'testcases.Advanced_Routing.TestRIP_TC68',
        'testcases.Advanced_Routing.TestRIP_TC69',
        'testcases.Advanced_Routing.TestRIP_TC70',
        'testcases.Advanced_Routing.TestRIP_TC77',
        'testcases.Advanced_Routing.TestRIP_TC79',
        'testcases.Advanced_Routing.TestRIP_TC80',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
