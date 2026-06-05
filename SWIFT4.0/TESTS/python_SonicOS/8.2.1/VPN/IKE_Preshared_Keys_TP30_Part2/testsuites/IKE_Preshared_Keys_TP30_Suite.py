# __author__: lezhang
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN/IKE_Preshared_Keys_TP30_Part2')


def suite():
    testcases_list = [
        'definition.init_conf_fw.TestinitRemoteFW.test_01_init_remote_fw_via_asyncio',
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw.TestConfigFW_Local',
        'definition.init_conf_fw.TestConfigFW_Remote',
        'definition.init_conf_pc.TestSetup_PCs',
        'testcases.IKE_Preshared_Keys_TP30.TestMain_TC15',
        'testcases.IKE_Preshared_Keys_TP30.TestMain_TC18',
        'testcases.IKE_Preshared_Keys_TP30.TestMain_TC21',
        'testcases.IKE_Preshared_Keys_TP30.TestMain_TC23',
        'testcases.IKE_Preshared_Keys_TP30.TestAggressive_TC26',
        'testcases.IKE_Preshared_Keys_TP30.TestAggressive_TC27',
        'testcases.IKE_Preshared_Keys_TP30.TestAggressive_TC29',
        'testcases.IKE_Preshared_Keys_TP30.TestAggressive_TC32',
        'testcases.IKE_Preshared_Keys_TP30.TestSuperNet_TC36',
        'testcases.IKE_Preshared_Keys_TP30.TestNetworkRange_TC44',
        'testcases.IKE_Preshared_Keys_TP30.TestDisable_TC47',
        'testcases.IKE_Preshared_Keys_TP30.TestAutoRule_TC93',
        'testcases.IKE_Preshared_Keys_TP30.TestReKey_TC98',
        'testcases.IKE_Preshared_Keys_TP30.TestManagedHttps_TC103',
        'testcases.IKE_Preshared_Keys_TP30.TestManagedssh_TC104',
        'testcases.IKE_Preshared_Keys_TP30.TestSNMP_TC110',
        'testcases.IKE_Preshared_Keys_TP30.TestDisableManaged_TC106',
        'testcases.IKE_Preshared_Keys_TP30.TestVLAN_TC96',
        'testcases.IKE_Preshared_Keys_TP30.TestMultipleVPN_TC101',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
