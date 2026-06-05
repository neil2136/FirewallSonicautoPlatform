#__Author__ = 'xzhou'
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+"/Log/Config_Auditing_GUI_Selected")
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+"/Log/Config_Auditing_GUI_Selected/definition")

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'init_conf_fw',
        'init_conf_pc',
        'testcases.audit.TestAudit_TC01',
        'testcases.audit.TestAudit_TC02',
        'testcases.audit.TestAudit_TC03',
        'testcases.audit.TestAudit_TC04',
        'testcases.audit.TestAudit_TC05',
        'testcases.audit.TestAudit_TC06',
        'testcases.audit.TestAudit_TC09',
        'testcases.audit.TestAudit_TC10',
        'testcases.audit.TestAudit_TC11',
        'testcases.audit.TestAudit_TC12',
        'testcases.audit.TestAudit_TC13',
        'testcases.audit.TestAudit_TC14',
        'testcases.audit.TestAudit_TC15',
        'testcases.audit.TestAudit_TC16',
        'testcases.audit.TestAudit_TC17',
        'testcases.audit.TestAudit_TC18',
        'testcases.audit.TestAudit_TC19',
        'testcases.audit.TestAudit_TC22',
        'testcases.audit.TestAudit_TC23',
        'testcases.audit.TestAudit_TC25',
        'testcases.audit.TestAudit_TC28',
        'testcases.audit.TestAudit_TC29'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
