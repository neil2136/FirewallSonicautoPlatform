from definition.settings import *
from definition.utils import *


@paramunittest.parametrized(
    {'check_list1': ["'Enable SSL' , changed from \[disabled\], changed to \[enabled\]"], 'check_list2': ["'Enable SSL'.*?disabled.*?enabled"], 'uuid': '1516442'},
    {'check_list1': ["'Violence/Hate/Racism' , changed from \[disabled\], changed to \[enabled\]"],'check_list2': ["'Violence/Hate/Racism'.*?disabled.*?enabled"], 'uuid': '1516443'},
    {'check_list1': ["'Enable SSL Server' , changed from \[disabled\], changed to \[enabled\]"], 'check_list2': ["'Enable SSL Server'.*?disabled.*?enabled"], 'uuid': '1516444'},
    {'check_list1': ["'SSL policing server server include object' , changed from \[All\], changed to \[192.168.168.200\]"], 'check_list2': ["'SSL policing server server include object'.*?All.*?192.168.168.200"], 'uuid': '1516445'},
    {'check_list1': ["'SSL server certs config' , changed to \[/aobj:192.168.168.200/certName:dpissl_server_cert/term:false\^\]"], 'check_list2': ["'SSL server certs config'.*?/aobj:192.168.168.200/certName:dpissl_server_cert/term:false\^"], 'uuid': '1516446'},
    {'check_list1': ["'SSL server certs config' , changed from \[/aobj:192.168.168.200/certName:dpissl_server_cert/term:false\^\], changed to \[/aobj:192.168.168.200/certName:dpissl_server_cert/term:true\^\]"], 'check_list2': ["'SSL server certs config'.*?/aobj:192.168.168.200/certName:dpissl_server_cert/term:false\^.*?/aobj:192.168.168.200/certName:dpissl_server_cert/term:true\^"], 'uuid': '1516447'},
    {'check_list1': ["'SSL server certs config' , changed from \[/aobj:192.168.168.200/certName:dpissl_server_cert/term:true\^\]"], 'check_list2': ["'SSL server certs config'.*?/aobj:192.168.168.200/certName:dpissl_server_cert/term:true\^"], 'uuid': '1516448'},
    {'check_list1': ["'SSH DPI Enable' , changed from \[disabled\], changed to \[enabled\]"], 'check_list2': ["'SSH DPI Enable'.*?disabled.*?enabled"], 'uuid': '1516449'},
    {'check_list1': ["'SSH DPI policing include address object' , changed from \[All\], changed to \[192.168.168.200\]"], 'check_list2': ["'SSH DPI policing include address object'.*?All.*?192.168.168.200"], 'uuid': '1516450'},
    {'check_list1': ["'SSL proxy Ca cert' , changed from \[Default SonicWall DPI-SSL 2048 bit CA certificate\], changed to \[dpissl_server_cert\]"], 'check_list2': ["'SSL proxy Ca cert'.*?Default SonicWall DPI-SSL 2048 bit CA certificate.*?dpissl_server_cert"], 'uuid': '1516452'},
    {'check_list1': ["'SSL policing exclude object' , changed from \[None\], changed to \[192.168.168.200\]"], 'check_list2': ["'SSL policing exclude object'.*?None.*?192.168.168.200"], 'uuid': '1516453'},
    {'check_list1': ["'SSL user excluded common names' , changed to \[google.com, \]"], 'check_list2': ["'SSL user excluded common names'.*?google.com,"], 'uuid': '1516454'},
    {'check_list1': ["'SSL user excluded common names' , changed from \[google.com, \]"], 'check_list2': ["'SSL user excluded common names'.*?google.com,"], 'uuid': '1516456'}
)
class DPI_SSL_And_DPI_SSH(Test):

    def setParameters(self, check_list1, check_list2, uuid):
        self.check_list1 = check_list1
        self.check_list2 = check_list2
        self.uuid = uuid
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True , True , "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_clear_log(self):
        rc = clear_log_and_snmp_msg()
        Assertion.assert_equal(rc, True, "ERR: Clear log and snmp server message failed")

    def test_02_config_dpissl_settings(self):
        if self.uuid == '1516442':
            resp = dpissl_cli.enable_dpissl_client()
            Assertion.assert_equal(resp, True, "ERR: Failed to enable DPI-SSL client")
        elif self.uuid == '1516443':
            resp = dpissl_cli.dpissl_client_cfs_category_inclusion_exclusion(mode='"1. Violence"')
            Assertion.assert_equal(resp, True, "ERR: Failed to configure DPI-SSL client CFS Category")
        elif self.uuid == '1516444':
            resp = dpissl_cli.enable_dpissl_server()
            Assertion.assert_equal(resp, True, "ERR: Failed to enable DPI-SSL server")
        elif self.uuid == '1516445':
            cmd = 'include address host 192.168.168.200'
            resp = dpissl_cli.dpissl_server_inclusion_exclusion(cmd)
            Assertion.assert_equal(resp, True, "ERR: Failed to configure DPI-SSL server Address/User Inclusion/Exclusion")
        elif self.uuid == '1516446':
            resp = dpissl_cli.dpissl_server_add_cert('host 192.168.168.200', 'dpissl_server_cert')
            Assertion.assert_equal(resp, True, "ERR: Failed to add DPI-SSL server certificate")
        elif self.uuid == '1516447':
            resp = dpissl_cli.dpissl_server_add_cert('host 192.168.168.200', 'dpissl_server_cert', True)
            Assertion.assert_equal(resp, True, "ERR: Failed to modify DPI-SSL server certificate")
        elif self.uuid == '1516448':
            resp = dpissl_cli.dpissl_server_del_cert('192.168.168.200')
            Assertion.assert_equal(resp, True, "ERR: Failed to delete DPI-SSL server certificate")
        elif self.uuid == '1516449':
            resp = dpissl_cli.enable_dpissh()
            Assertion.assert_equal(resp, True, "ERR: Failed to enable DPI-SSH")
        elif self.uuid == '1516450':
            cmd = 'include address host 192.168.168.200'
            resp = dpissl_cli.dpissh_inclusion_exclusion(cmd)
            Assertion.assert_equal(resp, True, "ERR: Failed to modify DPI-SSL client Address/User Inclusion/Exclusion")
        elif self.uuid == '1516452':
            resp = dpissl_cli.dpissl_client_cert('dpissl_server_cert')
            Assertion.assert_equal(resp, True, "ERR: Failed to modify DPI-SSL client certificate settings")
        elif self.uuid == '1516453':
            cmd = 'exclude address host 192.168.168.200'
            resp = dpissl_cli.dpissl_client_object_inclusion_exclusion(cmd)
            Assertion.assert_equal(resp, True, "ERR: Failed to modify DPI-SSL client Address/User Inclusion/Exclusion")
        elif self.uuid == '1516454':
            resp = dpissl_cli.dpissl_client_common_name('google.com', 'exclude')
            Assertion.assert_equal(resp, True, "ERR: Failed to configure DPI-SSL client common name settings")
        elif self.uuid == '1516456':
            resp = dpissl_cli.dpissl_client_del_common_name('google.com')
            Assertion.assert_equal(resp, True, "ERR: Failed to delete DPI-SSL client common name settings")

    def test_03_verify_syslog(self):
        rc = check_log_msg('syslog', self.check_list1)
        Assertion.assert_equal(rc, True, "ERR: check syslog failed")

    def test_04_verify_snmp(self):
        rc = check_log_msg('snmp', self.check_list1)
        Assertion.assert_equal(rc, True, "ERR: check snmp trap failed")

    def test_05_verify_audit_log(self):
        rc = check_log_msg('audit', self.check_list2)
        Assertion.assert_equal(rc, True, "ERR: check audit log failed")

    def test_06_verify_system_log(self):
        rc = check_log_msg('system', self.check_list1)
        Assertion.assert_equal(rc, True, "ERR: check log failed")
