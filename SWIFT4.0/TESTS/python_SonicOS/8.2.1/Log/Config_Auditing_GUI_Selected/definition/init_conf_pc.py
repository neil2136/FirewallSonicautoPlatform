from settings import *

CONFS_PATH = os.environ["PYTHON_SONICOS_HOME"] + \
    '/Log/Config_Auditing_GUI_Selected/definition/confs/'


class TestInitConfigPC(Test):
    uuid = 'NonTC'
    description = "initial setup server"
    goto_teardown = True

    def test_01_setup_syslog_server_on_PC1(self):
        ret = os.system(f"\\cp -f {CONFS_PATH}/rsyslog.conf /etc/rsyslog.conf")
        ret += os.system(f"\\cp -f {CONFS_PATH}/rsyslog /etc/sysconfig/rsyslog")
        ret += os.system("service rsyslog restart")
        Assertion.assert_equal(ret, 0, "ERR: Setup syslog server failed")
        output = os.popen("lsof -i:514").read()
        Assertion.assert_regular(
            output, 'LISTEN', "Verify syslog server port failed")

    def test_02_setup_snmp_server_on_PC2(self):
        PC2_login.send_command(
            f"\\cp -f {CONFS_PATH}/snmptrapd.conf /etc/snmp/snmptrapd.conf")
        PC2_login.send_command('snmptrapd -c /etc/snmp/snmptrapd.conf')
        output = PC2_login.send_command("lsof -i:162")
        Assertion.assert_regular(
            output, 'snmptrap', "Verify snmp server port failed")
