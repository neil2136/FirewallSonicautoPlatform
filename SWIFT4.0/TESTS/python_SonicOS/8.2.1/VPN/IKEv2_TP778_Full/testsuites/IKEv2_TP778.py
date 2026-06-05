import os
import sys
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN/IKEv2_TP778_Full')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.setup_network',
        'bin.conf_fw.TestConfigTB',
        'definition.conf_env',
        'testcases.IKEv2_TP778_Part2_TC.TestIKEv2_TP778_1522668',
        'testcases.IKEv2_TP778_Part2_TC.TestIKEv2_TP778_1522669',
        'testcases.IKEv2_TP778_Part2_TC.TestIKEv2_TP778_1522670',
        'testcases.IKEv2_TP778_Part2_TC.TestIKEv2_TP778_1522671',
        'testcases.IKEv2_TP778_Part2_TC.TestIKEv2_TP778_1522674',
        'testcases.IKEv2_TP778_Part2_TC.TestIKEv2_TP778_1522676',
        'testcases.IKEv2_TP778_Part2_TC.TestIKEv2_TP778_1532972',
        'testcases.IKEv2_TP778_Part2_TC.TestIKEv2_TP778_1745858',
        'testcases.IKEv2_TP778_Part2_TC.TestIKEv2_TP778_1745860',
        'testcases.IKEv2_TP778_Part2_TC.TestIKEv2_TP778_1786222',
        'testcases.IKEv2_TP778_Part2_TC.TestIKEv2_TP778_1826636',
        'testcases.IKEv2_TP778_Part2_TC.TestIKEv2_TP778_1826682',
        'testcases.IKEv2_TP778_Part2_TC.TestIKEv2_TP778_1826637',
        'testcases.IKEv2_TP778_Part2_TC.TestIKEv2_TP778_1826639',  
        'testcases.IKEv2_TP778_Part2_TC.TestIKEv2_TP778_1826640',  
        'testcases.IKEv2_TP778_Part2_TC.TestIKEv2_TP778_1968641',
        'testcases.IKEv2_TP778_Part2_TC.TestIKEv2_TP778_2649618',
        'testcases.IKEv2_TP778_Part2_TC.TestIKEv2_TP778_1826638',
        'testcases.IKEv2_TP778_Part2_TC.TestIKEv2_TP778_1968621',
        'testcases.IKEv2_TP778_Part2_TC.TestIKEv2_TP778_1968622',
        'testcases.IKEv2_TP778_Part2_TC.TestIKEv2_TP778_1968623',
        'testcases.IKEv2_TP778_Part2_TC.TestIKEv2_TP778_1768530',
        'testcases.IKEv2_TP778_Part2_TC.TestIKEv2_TP778_1522663',


    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
