# __author__: lezhang
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/Advanced_Routing_TP294_OSPF')


def suite():
    testcases_list = [
        'definition.init_conf_fw.TestinitRemoteFW.test_01_init_remote_fw_via_asyncio',
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw.TestConfigFW_Local',
        'definition.init_conf_fw.TestConfigFW_Remote',
        'testcases.Advanced_Routing.TestOSPF_TC88',
        'testcases.Advanced_Routing.TestInterval_TC89',
        'testcases.Advanced_Routing.TestDeclare_TC90',
        'testcases.Advanced_Routing.TestDeadInterval_TC91',
        'testcases.Advanced_Routing.TestRouterPrior_TC93',
        'testcases.Advanced_Routing.TestHelloMismatch_TC96',
        'testcases.Advanced_Routing.TestDiffIP_TC97',
        'testcases.Advanced_Routing.TestEBit_TC98',
        'testcases.Advanced_Routing.TestMasterSlave_TC101',
        'testcases.Advanced_Routing.TestMasterSlave_TC102',
        # 'testcases.Advanced_Routing.TestTransMode_TC125', 800 not support
        'testcases.Advanced_Routing.TestNSM_TC153',
        'testcases.Advanced_Routing.TestVLAN_TC117',
        'testcases.Advanced_Routing.TestVLAN_TC118',
        'testcases.Advanced_Routing.TestVPN_TC152',
        'testcases.Advanced_Routing.TestALLRouting_TC124',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
