import os
import sys
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/VLAN_296/')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'testcases.VLAN.TestVLAN_01', 
        'testcases.VLAN.TestVLAN_24', 
        'testcases.VLAN.TestVLAN_26', 
        'testcases.VLAN.TestVLAN_37', 
        'testcases.VLAN.TestVLAN_39', 
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
