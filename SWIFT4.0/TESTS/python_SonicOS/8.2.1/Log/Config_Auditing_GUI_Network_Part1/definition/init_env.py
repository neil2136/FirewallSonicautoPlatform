from definition.settings import *

class  TestInitConfig(Test):
    uuid = 'NonTC'
    goto_teardown = True
    
    def test_00_01_add_route(self):
        logger.info('-'*10+'add route'+'-'*10)
        out1 = PC1.send_commands(pc1_route_cmds)
        out2 = PC2.send_commands(pc2_route_cmds)
        out3 = PC3.send_commands(pc3_route_cmds)
        if f"{PC2_Network}/24 via {DUT_X0}" in out1 and f"{PC3_Network}/24 via {DUT_X0}" in out1 and \
            f"{DUT_Network}/24 via {DUT_X0}" in out1 and f'{PC1_Network}/24 via {DUT_X1}' in out2 \
            and f'{DUT_Network}/24 via {Remote_X0}' in out3 and f'{PC1_Network}/24 via {Remote_X0}' in out3:
            rc = True
        else:
            rc = False
            logger.error(out1)
            logger.error(out2)
            logger.error(out3)
        Assertion.assert_equal(rc, True, 'add route Failed.')

    def test_00_02_config_interface(self):
        logger.info('-'*10+'config x1 and x2 x3 ip'+'-'*10)
        rc = Linterface.config_interface(**Lx3)
        rc &= Linterface.config_interface(**Lx1)
        rc &= Linterface.config_interface(**Lx2)
        rc &= Linterface_ipv6.config_interface_ipv6(**Lx2_ipv6)
        rc &= Linterface_ipv6.config_interface_ipv6(**Lx0_ipv6)
        Assertion.assert_equal(rc, True, 'config x1 and x2 x3 ip Failed.')

    def test_00_03_Restore_Remote_FW(self):
        logger.info('Restore Remote FW...')
        path = cfg_path + 'restore_gw_rmt_tel.py'
        cmd = 'python3 {} -os=1 --testbed={} -device={} -if=X1 -zone=WAN -ip=12.12.1.201 -restore=1'.format(path, Params.testbed, rm_device)
        logger.info(cmd)
        out = os.popen(cmd).read()
        logger.info(out)
        rc = False
        for i in range(10):
            out = os.popen('ping {} -c 2'.format(Remote_X1)).read()
            logger.info(out)
            if ('100% packet loss' not in out):
                logger.info('Ping Remote success.')
                rc = True
                break
            elif i == 9:
                rc = False
                logger.info('Remote is unreachable.')
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: Restore Remote FW failed")

    @repeat_method(5)
    def test_00_04_register_fw(self):
        logger.info(" {} ".center(20, '-').format('Register firewall'))
        time.sleep(10)
        rc = license_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_00_05_add_addObj(self):
        logger.info('-'*10+'Add remote AddObj for DUT and Remote DUT'+'-'*10)
        logger.info('-'*10+'Add remote AddObj for DUT '+'-'*10)
        res1 = LAddrOBJ.config_addressobject(msg=True,**local_r)
        logger.info('-'*10+'Add remote AddObj for Remote DUT'+'-'*10)
        res2 = RAddrOBJ.config_addressobject(msg=True,**remote_r)
        logger.info(f'----------{res1}------{res2}----')
        if (res1[0] or 'Already exists' in str(res1[1])) and (res2[0] or 'Already exists' in str(res2[1])):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'Add local and remote AddObj for DUT  Failed.')

    def test_00_06_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        logger.info("Local VPN Policy {} ".format(ref1))
        rc = Rvpn_obj.del_all_vpn_policies()
        rc &= Lvpn_obj.del_all_vpn_policies()
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        logger.info("Remote VPN Policy {} ".format(ref2))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.') 

    def test_00_07_add_acl(self):
        rule1 = copy.deepcopy(rule_opt)
        rule2 = copy.deepcopy(rule_opt)
        rule1['name'] = 'VPN_to_LAN'
        rule1['from'] = 'VPN'
        rule1['to']   = 'LAN'
        rule2['name'] = 'LAN_to_VPN'
        rule2['from'] = 'LAN'
        rule2['to']   = 'VPN'
        res1 = Laccess_rule_obj.config_accessrule(msg=True,**rule1)
        res2= Laccess_rule_obj.config_accessrule(msg=True,**rule2)
        if (res1[0] or 'Already exists' in str(res1[1])) and (res2[0] or 'Already exists' in str(res2[1])):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: add access rule between VPN to LAN in DUT2 failed")


    def test_00_08_add_address_object(self):
        logger.info(" {} ".center(20, '-').format('Add address object'))
        rc = LAddrOBJ.config_addressobject(**local_obj)
        rc &= LAddrOBJ.config_addressobject(**syslog_obj)
        Assertion.assert_equal(rc, True, "ERR: Add address object failed")

    def test_00_09_add_syslog_server(self):
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
    def test_00_10_set_audit_log_level(self,id,name,cate,group,flag):
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

    def test_00_11_setup_syslog_server(self):
        logger.info(" {} ".center(20, '-').format('Setup syslog server'))
        ret = os.system(f"\\cp -f {CONFS_PATH}/rsyslog.conf /etc/rsyslog.conf")
        ret += os.system(f"\\cp -f {CONFS_PATH}/rsyslog /etc/sysconfig/rsyslog")
        ret += os.system("service rsyslog restart")
        Assertion.assert_equal(ret, 0, "ERR: Setup syslog server failed")
        output = os.popen("lsof -i:514").read()
        Assertion.assert_regular(output, 'LISTEN', "Verify syslog server port failed")

    def test_00_12_enable_snmp(self):
        logger.info(" {} ".center(20, '-').format('Enable SNMP'))
        rc = snmp_obj.enable_snmp()
        Assertion.assert_equal(rc, True, 'ERR: Enable snmp failed!')

    def test_00_13_config_snmp(self):
        logger.info(" {} ".center(20, '-').format('Configure SNMP'))
        rc = snmp_obj.configure_snmp(**snmp_json)
        Assertion.assert_equal(rc, True, 'ERR: Configure SNMPv3 failed!')

    def test_00_14_setup_snmp_server(self):
        PC2.send_command('rm -f /etc/snmp/snmptrapd.conf')
        PC2.send_command(f"\\cp -f {CONFS_PATH}/snmptrapd.conf /etc/snmp/snmptrapd.conf")
        PC2.send_command('snmptrapd -c /etc/snmp/snmptrapd.conf')
        output = PC2.send_command("lsof -i:162")
        Assertion.assert_regular(output, 'snmptrap', "Verify snmp server port failed")

    def test_00_15_check_enable_load_balance(self):
        logger.info('check enable load balance...')
        rc = failover_obj.config_failover_settings(**lb)
        Assertion.assert_equal(rc, True, "ERR: check enable load balance failed")

