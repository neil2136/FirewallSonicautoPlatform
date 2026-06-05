import sys
import os

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Enhanced_HTTP_HTTPS_Redirector_With_DP_Offload')

from definition.settings import *


class TestConfigFW(Test):
    uuid = 'NonTC'

    def test_00_01_Config_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'dns3': Parameter.X1_DNS3,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X1_GW,
            'mgmt_https': True,
            'user_https': True,
        }
        rc = interface.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")
