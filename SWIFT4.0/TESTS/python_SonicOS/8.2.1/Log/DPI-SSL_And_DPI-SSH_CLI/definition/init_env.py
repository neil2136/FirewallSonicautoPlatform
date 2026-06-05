from definition.settings import *

class  TestInitConfig(Test):
    uuid = 'NonTC'

    def test_01_config_interface(self):
        logger.info('-'*10+'Config X1 interface'+'-'*10)
        rc = Linterface.config_interface(**Lx1)
        Assertion.assert_equal(rc, True, 'Config X1 interface failed')

    @repeat_method(5)
    def test_02_register_fw(self):
        rc = license_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_03_add_address_object(self):
        logger.info(" {} ".center(20, '-').format('Add address object'))
        rc = LAddrOBJ.config_addressobject(**local_obj)
        rc &= LAddrOBJ.config_addressobject(**syslog_obj)
        Assertion.assert_equal(rc, True, "ERR: Add address object failed")

    def test_04_add_syslog_server(self):
        logger.info(" {} ".center(20, '-').format('Add syslog server'))
        ret = syslog_api.add_syslog_server(**syslog_param)
        Assertion.assert_equal(ret, True, "ERR: add syslog server failed")

    @parameterized.expand([
        (1382, 'Configuration Change Succeeded', 'Log', 'Configuration Auditing', True),
        (1383, 'Configuration Change Failed', 'Log', 'Configuration Auditing', False),
        (1220, 'Invalid SNMPv3 Packet',      'System', 'SNMP', True),
        (1221, 'Invalid SNMPv3 Engine ID',   'System', 'SNMP', True),
        (1222, 'Invalid SNMPv3 User',        'System', 'SNMP', True),
        (1223, 'Invalid SNMPv3 Time Window', 'System', 'SNMP', True),
        (1225, 'SNMP Packet Drop',           'System', 'SNMP', True),
    ])
    def test_05_set_audit_log_level(self,id,name,cate,group,flag):
        logger.info(" {} ".center(20, '-').format('Set syslog level'))
        settings = copy.deepcopy(log_level_settings)
        settings['log']['event'][0]['id'] = id
        settings['log']['event'][0]['name'] = name
        settings['log']['event'][0]['category'] = cate
        settings['log']['event'][0]['group'] = group
        settings['log']['event'][0]['log_digest'] = flag
        if group=='SNMP':
            settings['log']['event'][0]['trap'] = {}
        rc = logsetting_obj.edit_event(event_id=str(id), **settings)
        Assertion.assert_equal(rc, True, "ERR: set log level failed")

    def test_06_enable_snmp(self):
        logger.info(" {} ".center(20, '-').format('Enable SNMP'))
        rc = snmp_obj.enable_snmp()
        Assertion.assert_equal(rc, True, 'ERR: Enable snmp failed!')

    def test_07_config_snmp(self):
        logger.info(" {} ".center(20, '-').format('Configure SNMP'))
        rc = snmp_obj.configure_snmp(**snmp_json)
        Assertion.assert_equal(rc, True, 'ERR: Configure SNMPv3 failed!')
    
    def test_08_setup_syslog_server(self):
        logger.info(" {} ".center(20, '-').format('Setup syslog server'))
        ret = os.system(f"\\cp -f {CONFS_PATH}/rsyslog.conf /etc/rsyslog.conf")
        ret += os.system(f"\\cp -f {CONFS_PATH}/rsyslog /etc/sysconfig/rsyslog")
        ret += os.system("service rsyslog restart")
        Assertion.assert_equal(ret, 0, "ERR: Setup syslog server failed")
        output = os.popen("lsof -i:514").read()
        Assertion.assert_regular(output, 'LISTEN', "Verify syslog server port failed")  

    def test_09_setup_snmp_server(self):
        PC2.send_command('rm -f /etc/snmp/snmptrapd.conf')
        PC2.send_command(f"\\cp -f {CONFS_PATH}/snmptrapd.conf /etc/snmp/snmptrapd.conf")
        PC2.send_command('snmptrapd -c /etc/snmp/snmptrapd.conf')
        output = PC2.send_command("lsof -i:162")
        Assertion.assert_regular(output, 'snmptrap', "Verify snmp server port failed")

    def test_10_import_dpissl_server_cert(self):
        logger.info('Add DPI-SSL Server Certificate')
        rc, response = certobj.import_cert_local('@' + dpissl_server_cert, 'dpissl_server_cert', 'password')
        Assertion.assert_equal(rc, True, 'ERR: Add DPI-SSL Server Certificate failed')
