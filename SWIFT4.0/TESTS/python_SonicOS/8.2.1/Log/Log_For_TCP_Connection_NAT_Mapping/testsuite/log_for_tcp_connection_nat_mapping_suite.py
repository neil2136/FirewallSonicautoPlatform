# Author: cyuan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Log/Log_For_TCP_Connection_NAT_Mapping')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        "definition.init_config_fw",
        "definition.init_config_pc",
        "testcases.log_for_nat_mapping.Test_Log_Nat_Mapping_TC1529557",
        "testcases.log_for_nat_mapping.Test_Log_Nat_Mapping_TC1529558",
        "testcases.log_for_nat_mapping.Test_Log_Nat_Mapping_TC1529559",
        "testcases.log_for_nat_mapping.Test_Log_Nat_Mapping_TC1529561",
        "testcases.log_for_nat_mapping.Test_Log_Nat_Mapping_TC1529562",
        "testcases.log_for_nat_mapping.Test_Log_Nat_Mapping_TC1529563",
        "testcases.log_for_nat_mapping.Test_Log_Nat_Mapping_TC1529564",
        "testcases.log_for_nat_mapping.Test_Log_Nat_Mapping_TC1529560",
        "testcases.log_for_nat_mapping.Test_Log_Nat_Mapping_TC1529566",
        "testcases.log_for_nat_mapping.Test_Log_Nat_Mapping_TC1529567",

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
