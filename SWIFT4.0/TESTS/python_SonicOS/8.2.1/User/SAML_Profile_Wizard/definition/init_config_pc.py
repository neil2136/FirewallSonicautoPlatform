from definition.settings import *


class Test_Config_PC(Test):
    uuid='NonTC'
    goto_teardown = True

    def test_01_cp_xml_file_to_pc(self):
        xml_file = suite_path + 'definition/sonicauto.xml'
        pc1_login.send_command(f'\cp {xml_file} /tmp')
        rc = os.path.exists('/tmp/sonicauto.xml')
        Assertion.assert_equal(rc, True, 'ERR: cp xml file FAILED!!')