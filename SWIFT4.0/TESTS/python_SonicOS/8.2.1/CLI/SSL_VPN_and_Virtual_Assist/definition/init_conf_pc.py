from definition.settings import *


class TestSetup_PCs(Test):
    uuid = 'NonTC'
    
    
    def test_01_syslog_server_setup(self):
        ret = os.system(f"\\cp -f {Parameter.CONF_PATH}/syslog_server/rsyslog.conf /etc/rsyslog.conf")
        ret += os.system(f"\\cp -f {Parameter.CONF_PATH}/syslog_server/rsyslog /etc/sysconfig/rsyslog")
        ret += os.system("service rsyslog restart")
        Assertion.assert_equal(ret, 0, "ERR: Setup syslog server failed")
        output = os.popen("lsof -i:514").read()
        Assertion.assert_regular(output, 'LISTEN', "Verify syslog server port failed")

    def test_02_setup_snmp_server(self):
        pc2.send_command('rm -f /etc/snmp/snmptrapd.conf')
        pc2.send_command(f"\\cp -f {Parameter.CONF_PATH}/snmp/snmptrapd.conf /etc/snmp/snmptrapd.conf")
        pc2.send_command('snmptrapd -c /etc/snmp/snmptrapd.conf')
        output = pc2.send_command("lsof -i:162")
        Assertion.assert_regular(output, 'snmptrap', "Verify snmp server port failed")