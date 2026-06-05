from definition.settings import *

CONFS_PATH = os.environ["PYTHON_SONICOS_HOME"] + \
             '/Network/Debug_Enhancement_User_Auth/definition/confs/'


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

    def test_02_setup_syslog_server_on_PC2(self):
        PC3_login.send_command(f"\\cp -f {CONFS_PATH}/rsyslog.conf /etc/rsyslog.conf")
        PC3_login.send_command(f"\\cp -f {CONFS_PATH}/rsyslog /etc/sysconfig/rsyslog")
        PC3_login.send_command("service rsyslog restart")
        output = PC3_login.send_command("lsof -i:514")
        Assertion.assert_regular(
            output, 'LISTEN', "Verify syslog server port failed")
