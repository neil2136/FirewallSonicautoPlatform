import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/MAC-IP_Anti_Spoof_2429/')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_fw.TestInitConfig',
        'testcases.mac_spoof.TestMacSpoof_2',
        'testcases.mac_spoof.TestMacSpoof_3', 
        'testcases.mac_spoof.TestMacSpoof_16',
        'testcases.mac_spoof.TestMacSpoof_17',
        'testcases.mac_spoof.TestMacSpoof_20',
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
