import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"] + '/tools')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    '/CLI/CLI3_System')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    '/CLI/CLI3_System/definition')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
'/CLI/CLI3_System/testcases')
sys.path.append(os.path.join(os.environ["PYTHON_SONICOS_HOME"], 'CLI/CLI3_System/testcases/system'))
sys.path.append(os.path.join(os.environ["PYTHON_SONICOS_HOME"], 'CLI/CLI3_System/testcases'))
sys.path.append(os.path.join(os.environ["PYTHON_SONICOS_HOME"], 'CLI/CLI3_System/testcases'))


def suite():
    # 修改测试用例列表，使用正确的模块路径
    testcases_list = [
        # 'config.init_testbed.TestRestoreDUT',
        # 'config.init_testbed.TestUploadFirmware',
        # 'conf_fw',
        # 'conf_pc',
        'system.Test_01_show_status_check_1',  # 修改为模块路径
        'system.Test_02_configure_administration_2',  # 修改为模块路径
        'system.Test_03_enable_fips_check_3',  # 修改为模块路径
        'system.Test_04_nslookup_check_4',  # 修改为模块路径
        'system.Test_05_ping_check_5',  # 修改为模块路径
        'system.Test_06_configure_schedule_7',  # 修改为模块路径
        'system.Test_07_traceroute_check_8',  # 修改为模块路径
        'system.Test_08_configure_time_9',  # 修改为模块路径
        'system.Test_09_restore_defaults_check_6'  # 修改为模块路径
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
