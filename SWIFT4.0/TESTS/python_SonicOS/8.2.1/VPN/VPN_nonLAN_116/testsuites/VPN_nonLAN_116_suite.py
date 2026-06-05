import os
import sys
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN/VPN_nonLAN_116')
from bin.utils import Local_one_remote_LAN

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'bin.conf_fw',
        'definition.conf_env.TestConfigTB1',
        'testcases.VPN_nonLAN_116'
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
