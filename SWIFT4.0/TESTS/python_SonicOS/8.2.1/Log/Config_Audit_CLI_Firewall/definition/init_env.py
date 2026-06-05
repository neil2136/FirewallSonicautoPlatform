from definition.settings import *

class  TestInitConfig(Test):
    uuid = 'NonTC'
    goto_teardown = True
    
    def test_00_01_add_route(self):
        logger.info('-'*10+'add route'+'-'*10)
        out1 = PC1.send_commands(pc1_route_cmds)
        out2 = PC2.send_commands(pc2_route_cmds)
        if f"{PC2_Network}/24 via {DUT_X0}" in out1  and \
             f'{PC1_Network}/24 via {DUT_X1}' in out2 :
            rc = True
        else:
            rc = False
            logger.error(out1)
            logger.error(out2)
        Assertion.assert_equal(rc, True, 'add route Failed.')

    def test_00_02_config_interface(self):
        logger.info('-'*10+'config x1 and x2 x3 ip'+'-'*10)
        rc = Linterface.config_interface(**Lx1)
        rc &= Linterface.config_interface(**Lx2)
        Assertion.assert_equal(rc, True, 'config x1 and x2 x3 ip Failed.')

    @repeat_method(5)
    def test_00_03_register_fw(self):
        logger.info(" {} ".center(20, '-').format('Register firewall'))
        time.sleep(10)
        rc = license_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")
    

    def test_00_04_add_address_object(self):
        logger.info(" {} ".center(20, '-').format('Add address object'))
        rc = LAddrOBJ.config_addressobject(**local_obj)
        rc &= LAddrOBJ.config_addressobject(**syslog_obj)
        Assertion.assert_equal(rc, True, "ERR: Add address object failed")

    def test_00_05_add_syslog_server(self):
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
    def test_00_06_set_audit_log_level(self,id,name,cate,group,flag):
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

    def test_00_07_config_audit_group(self):
        rc = log_category.edit_log_category_groups_by_id(id = 15,**log_group)
        Assertion.assert_equal(rc, True, "ERR: set log level failed")

    def test_00_08_setup_syslog_server(self):
        logger.info(" {} ".center(20, '-').format('Setup syslog server'))
        ret = os.system(f"\\cp -f {CONFS_PATH}/rsyslog.conf /etc/rsyslog.conf")
        ret += os.system(f"\\cp -f {CONFS_PATH}/rsyslog /etc/sysconfig/rsyslog")
        ret += os.system("service rsyslog restart")
        Assertion.assert_equal(ret, 0, "ERR: Setup syslog server failed")
        output = os.popen("lsof -i:514").read()
        Assertion.assert_regular(output, 'LISTEN', "Verify syslog server port failed")

    def test_00_09_enable_snmp(self):
        logger.info(" {} ".center(20, '-').format('Enable SNMP'))
        rc = snmp_obj.enable_snmp()
        Assertion.assert_equal(rc, True, 'ERR: Enable snmp failed!')

    def test_00_10_config_snmp(self):
        logger.info(" {} ".center(20, '-').format('Configure SNMP'))
        rc = snmp_obj.configure_snmp(**snmp_json)
        Assertion.assert_equal(rc, True, 'ERR: Configure SNMPv3 failed!')

    def test_00_11_setup_snmp_server(self):
        PC2.send_command('rm -f /etc/snmp/snmptrapd.conf')
        PC2.send_command(f"\\cp -f {CONFS_PATH}/snmptrapd.conf /etc/snmp/snmptrapd.conf")
        PC2.send_command('snmptrapd -c /etc/snmp/snmptrapd.conf')
        output = PC2.send_command("lsof -i:162")
        Assertion.assert_regular(output, 'snmptrap', "Verify snmp server port failed")

    



