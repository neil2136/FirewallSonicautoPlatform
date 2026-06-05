# Author: xzhan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Sinkhole_full')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_pc_configure.TestConfigPC',
        'definition.init_fw_configure.TestConfigFW',
        'testcases.DNS_Sinkhole.TestSettings_1503271',
        'testcases.DNS_Sinkhole.TestSettings_1503272',
        'testcases.DNS_Sinkhole.TestSettings_1503240',
        'testcases.DNS_Sinkhole.TestError_1503242',
        'testcases.DNS_Sinkhole.TestFunc_1503243',
        'testcases.DNS_Sinkhole.TestFunc_1503244',
        'testcases.DNS_Sinkhole.TestFunc_1503245',
        'testcases.DNS_Sinkhole.TestFunc_1503246',
        'testcases.DNS_Sinkhole.TestFunc_1503247',
        'testcases.DNS_Sinkhole.TestFunc_1503248',
        'testcases.DNS_Sinkhole.TestFunc_1503249',
        'testcases.DNS_Sinkhole.TestSettings_1503251',
        'testcases.DNS_Sinkhole.TestFunc_1503252',
        'testcases.DNS_Sinkhole.TestFunc_1503253',
        'testcases.DNS_Sinkhole.TestError_1503254',
        'testcases.DNS_Sinkhole.TestBoundary_1503255',
        'testcases.DNS_Sinkhole.TestSettings_1503256',
        'testcases.DNS_Sinkhole.TestFunc_1503257',
        'testcases.DNS_Sinkhole.TestFunc_1503258',
        'testcases.DNS_Sinkhole.TestError_1503259',
        'testcases.DNS_Sinkhole.TestBoundary_1503260',
        'testcases.DNS_Sinkhole.TestFunc_1503262',
        'testcases.DNS_Sinkhole.TestSettings_1503264',
        'testcases.DNS_Sinkhole.TestFunc_1503230',
        'testcases.DNS_Sinkhole.TestFunc_1503231',
        'testcases.DNS_Sinkhole.TestFunc_1503232',
        'testcases.DNS_Sinkhole.TestFunc_1503233',
        'testcases.DNS_Sinkhole.TestFunc_1503234',
        'testcases.DNS_Sinkhole.TestFunc_1503236',
        'testcases.DNS_Sinkhole.TestFunc_1503237',
        'testcases.DNS_Sinkhole.TestFunc_1503274',
        'testcases.DNS_Sinkhole.TestFunc_1503229',
        'testcases.DNS_Sinkhole.TestSettings_1503228',
        'testcases.DNS_Sinkhole.TestSettings_1503250',
        'testcases.DNS_Sinkhole.TestSettings_1503239'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
