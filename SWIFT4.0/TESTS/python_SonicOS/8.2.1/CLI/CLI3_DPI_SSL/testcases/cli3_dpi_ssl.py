from definition.settings import *


# enable/disable dpi-ssl client via Cli
class TestCli_TC1(Test):
    uuid = "SOSAIOT-TC-48352"
    description = show_testcase_info(TESTPLAN,
                                     "1", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, "1")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_check_DPI_SSL(self):
        confdict = {
            'enable': True
        }
        res = dpisslclientcli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        res &= False if 'no enable' in showres else True
        Assertion.assert_equal(res, True, 'ERR: enable DPI SSL client failed')

    def test_02_disable_check_DPI_SSL(self):
        confdict = {
            'enable': False
        }
        res = dpisslclientcli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        res &= True if 'no enable' in showres else False
        Assertion.assert_equal(res, True, 'ERR: disable DPI SSL client failed')


# enable/disable client dpissl application firewall via CLI
class TestCli_TC2(Test):
    uuid = "SOSAIOT-TC-48363"
    description = show_testcase_info(TESTPLAN,
                                     "2", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, "2")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_check_application_firewall(self):
        confdict = {
            'application-firewall': True
        }
        res = dpisslclientcli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        res &= False if 'no application-firewall' in showres else True
        Assertion.assert_equal(res, True, 'ERR: enable application firewall failed')

    def test_02_disable_check_application_firewall(self):
        confdict = {
            'application-firewall': False
        }
        res = dpisslclientcli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        res &= True if 'no application-firewall' in showres else False
        Assertion.assert_equal(res, True, 'ERR: disable application firewall failed')


# enable/disable content filter via CLI
class TestCli_TC3(Test):
    uuid = "SOSAIOT-TC-48368"
    description = show_testcase_info(TESTPLAN,
                                     "3", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, "3")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_check_content_filter(self):
        confdict = {
            'content-filter': True
        }
        res = dpisslclientcli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        res &= False if 'no content-filter' in showres else True
        Assertion.assert_equal(res, True, 'ERR: enable content-filter failed')

    def test_02_disable_check_content_filter(self):
        confdict = {
            'content-filter': False
        }
        res = dpisslclientcli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        res &= True if 'no content-filter' in showres else False
        Assertion.assert_equal(res, True, 'ERR: disable content-filter failed')


# enable/disable GAV via CLI
class TestCli_TC4(Test):
    uuid = "SOSAIOT-TC-48369"
    description = show_testcase_info(TESTPLAN,
                                     "4", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, "4")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_check_gateway_anti_virus(self):
        confdict = {
            'gateway anti-virus': True
        }
        res = dpisslclientcli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        res &= False if 'no gateway anti-virus' in showres else True

        # init dpi ssl configuration
        dpisslclientcli.config_general_settings(**check_dpi_ssl_client_dict)
        Assertion.assert_equal(res, True, 'ERR: enable gateway anti-virus failed')

    def test_02_disable_check_gateway_anti_virus(self):
        confdict = {
            'gateway anti-virus': False
        }
        res = dpisslclientcli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        res &= True if 'no gateway anti-virus' in showres else False
        Assertion.assert_equal(res, True, 'ERR: disable gateway anti-virus failed')


# enable/disalbe intrusion prevention via CLI
class TestCli_TC5(Test):
    uuid = "SOSAIOT-TC-48370"
    description = show_testcase_info(TESTPLAN,
                                     "5", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, "5")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_check_intrusion_prevention(self):
        confdict = {
            'intrusion-prevention': True
        }
        res = dpisslclientcli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        res &= False if 'no intrusion-prevention' in showres else True
        Assertion.assert_equal(res, True, 'ERR: enable intrusion-prevention failed')

    def test_02_disable_check_intrusion_prevention(self):
        confdict = {
            'intrusion-prevention': False
        }
        res = dpisslclientcli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        res &= True if 'no intrusion-prevention' in showres else False
        Assertion.assert_equal(res, True, 'ERR: disable intrusion-prevention failed')


# set exclusion list via CLI
class TestCli_TC6(Test):
    uuid = "SOSAIOT-TC-48371"
    description = show_testcase_info(TESTPLAN,
                                     "6", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, "6")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_set_exclusion_list(self):
        exclusiondict = {
            'exclude address': 'X0\ Subnet',
            'exclude address type': 'name',
            'exclude service': 'SNMP',
            'exclude service type': 'name',
            'exclude user': 'Guest\ Services',
            'exclude user type': 'group'
        }
        res = dpisslclientcli.config_objects(**exclusiondict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        expres = ('exclude address name "X0 Subnet"', 'exclude service name SNMP', 'exclude user group "Guest Services"')
        res &= True if all(x in showres for x in expres) else False
        Assertion.assert_equal(res, True, 'ERR: set exclusion failed')

    def test_02_init_exclusion_list(self):
        # init dpi ssl configuration
        initres = dpisslclientcli.config_objects(**dpi_ssl_include_exclude_dict)
        logger.info('The result of initialization is: {}'.format(initres))
        Assertion.assert_equal(initres, True, 'ERR: init exclusion failed')


# set inclusion list via CLI
class TestCli_TC7(Test):
    uuid = "SOSAIOT-TC-48372"
    description = show_testcase_info(TESTPLAN,
                                     "7", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, "7")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_set_inclusion_list(self):
        inclusionlist = {
            'include address': 'X0\ Subnet',
            'include address type': 'name',
            'include service': 'SNMP',
            'include service type': 'name',
            'include user': 'Guest\ Services',
            'include user type': 'group'
        }
        res = dpisslclientcli.config_objects(**inclusionlist)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        expres = ('include address name "X0 Subnet"', 'include service name SNMP', 'include user group "Guest Services"')
        res &= True if all(x in showres for x in expres) else False
        Assertion.assert_equal(res, True, 'ERR: set inclusion failed')

    def test_02_init_inclusion_list(self):
        # init dpi ssl configuration
        initres = dpisslclientcli.config_objects(**dpi_ssl_include_exclude_dict)
        logger.info('The result of initialization is: {}'.format(initres))
        Assertion.assert_equal(initres, True, 'ERR: init inclusion failed')


# resign authority via CLI
class TestCli_TC8(Test):
    uuid = "SOSAIOT-TC-48373"
    description = show_testcase_info(TESTPLAN,
                                     "8", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, "8")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_resigning_authority(self):
        conflist = {
            'resigning-authority': 'default 2048-bit'
        }
        res = dpisslclientcli.config_cert(**conflist)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        res &= True if 'resigning-authority default 2048-bit' in showres else False
        Assertion.assert_equal(res, True, 'ERR: configure resigning authority failed')


# enable/disable dpi-ssl server via CLI
class TestCli_TC9(Test):
    uuid = "SOSAIOT-TC-48374"
    description = show_testcase_info(TESTPLAN,
                                     "9", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, "9")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_server_dpi_ssl(self):
        confdict = {
            'enable': True
        }
        res = dpisslservercli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslservercli.show_serverssl()
        res &= False if 'no enable' in showres else True
        Assertion.assert_equal(res, True, 'ERR: enable server dpi ssl failed')

    def test_02_disable_server_dpi_ssl(self):
        confdict = {
            'enable': False
        }
        res = dpisslservercli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslservercli.show_serverssl()
        res &= True if 'no enable' in showres else False
        Assertion.assert_equal(res, True, 'ERR: disable server dpi ssl failed')


# enable/disable server application firewall via CLI
class TestCli_TC10(Test):
    uuid = "SOSAIOT-TC-48353"
    description = show_testcase_info(TESTPLAN,
                                     "10", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, "10")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_server_application_firewall(self):
        confdict = {
            'application-firewall': True
        }
        res = dpisslservercli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslservercli.show_serverssl()
        res &= False if 'no application-firewall' in showres else True
        Assertion.assert_equal(res, True, 'ERR: enable server application firewall failed')

    def test_02_disable_server_application_firewall(self):
        confdict = {
            'application-firewall': False
        }
        res = dpisslservercli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslservercli.show_serverssl()
        res &= True if 'no application-firewall' in showres else False
        Assertion.assert_equal(res, True, 'ERR: disable server application firewall failed')


# enable/disable server GAV via CLI
class TestCli_TC11(Test):
    uuid = "SOSAIOT-TC-48354"
    description = show_testcase_info(TESTPLAN,
                                     "11", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, "11")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_server_gateway_anti_virus(self):
        confdict = {
            'gateway anti-virus': True
        }
        res = dpisslservercli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslservercli.show_serverssl()
        res &= False if 'no gateway anti-virus' in showres else True
        Assertion.assert_equal(res, True, 'ERR: enable server gateway anti-virus failed')

    def test_02_disable_server_gateway_anti_virus(self):
        confdict = {
            'gateway anti-virus': False
        }
        res = dpisslservercli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslservercli.show_serverssl()
        res &= True if 'no gateway anti-virus' in showres else False
        Assertion.assert_equal(res, True, 'ERR: disable server gateway anti-virus failed')

    def test_03_enable_server_gateway_anti_spyware(self):
        confdict = {
            'gateway anti-spyware': True
        }
        res = dpisslservercli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslservercli.show_serverssl()
        res &= False if 'no gateway anti-spyware' in showres else True
        Assertion.assert_equal(res, True, 'ERR: enable server gateway anti-spyware failed')

    def test_04_disable_server_gateway_anti_spyware(self):
        confdict = {
            'gateway anti-spyware': False
        }
        res = dpisslservercli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslservercli.show_serverssl()
        res &= True if 'no gateway anti-spyware' in showres else False
        Assertion.assert_equal(res, True, 'ERR: disable server gateway anti-spyware failed')


# set server exclusion list via CLI
class TestCli_TC12(Test):
    uuid = "SOSAIOT-TC-48355"
    description = show_testcase_info(TESTPLAN,
                                     "12", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, "12")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_set_exclusion_list(self):
        exclusiondict = {
            'exclude address': 'X0\ Subnet',
            'exclude address type': 'name',
            'exclude user': 'Guest\ Services',
            'exclude user type': 'group'
        }
        res = dpisslservercli.config_general_settings(**exclusiondict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslservercli.show_serverssl()
        expres = ('exclude address name "X0 Subnet"', 'exclude user group "Guest Services"')
        res &= True if all(x in showres for x in expres) else False
        Assertion.assert_equal(res, True, 'ERR: set exclusion failed')

    def test_02_init_exclusion_list(self):
        # init dpi ssl configuration
        initres = dpisslservercli.config_general_settings(**check_dpi_ssl_server_dict)
        logger.info('The result of initialization is: {}'.format(initres))
        Assertion.assert_equal(initres, True, 'ERR: init exclusion failed')


# set server inclusion list via CLI
class TestCli_TC13(Test):
    uuid = "SOSAIOT-TC-48356"
    description = show_testcase_info(TESTPLAN,
                                     "13", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, "13")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_set_inclusion_list(self):
        inclusionlist = {
            'include address': 'X0\ Subnet',
            'include address type': 'name',
            'include user': 'Guest\ Services',
            'include user type': 'group'
        }
        res = dpisslservercli.config_general_settings(**inclusionlist)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslservercli.show_serverssl()
        expres = ('include address name "X0 Subnet"', 'include user group "Guest Services"')
        res &= True if all(x in showres for x in expres) else False
        Assertion.assert_equal(res, True, 'ERR: set inclusion failed')

    def test_02_init_inclusion_list(self):
        # init dpi ssl configuration
        initres = dpisslservercli.config_general_settings(**check_dpi_ssl_server_dict)
        logger.info('The result of initialization is: {}'.format(initres))
        Assertion.assert_equal(initres, True, 'ERR: init inclusion failed')


# enable/disable server intrusion prevention via CLI
class TestCli_TC14(Test):
    uuid = "SOSAIOT-TC-48357"
    description = show_testcase_info(TESTPLAN,
                                     "14", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, "14")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_server_intrusion_prevention(self):
        confdict = {
            'intrusion-prevention': True
        }
        res = dpisslservercli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslservercli.show_serverssl()
        res &= False if 'no intrusion-prevention' in showres else True
        Assertion.assert_equal(res, True, 'ERR: enable server intrusion-prevention failed')

    def test_02_disable_server_intrusion_prevention(self):
        confdict = {
            'intrusion-prevention': False
        }
        res = dpisslservercli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslservercli.show_serverssl()
        res &= True if 'no intrusion-prevention' in showres else False
        Assertion.assert_equal(res, True, 'ERR: disable server intrusion-prevention failed')


# import certificate and add/delete dpi-ssl server
class TestCli_TC15(Test):
    uuid = "SOSAIOT-TC-48358"
    description = show_testcase_info(TESTPLAN,
                                     "15", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, "15")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_import_cert(self):
        cerpath = PC1_ETH1_IP + ':' + cert_path
        logger.info('Result of cerpath {}'.format(cerpath))
        confdict = {
            'type': 'cert-key-pair',
            'protocol': 'scp',
            'user': 'root',
            'passwd': 'password',
            'server': cerpath,
            'file': 'test.pfx',
            'cert-key-pair': 'test',
            'ca_passwd': 'password',
            'password': 'password'
        }
        res = certificatecli.import_cert(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = certificatecli.show_certs(mode='imported', with_exp='')
        res &= True if 'test' in showres else False
        Assertion.assert_equal(res, True, 'ERR: import certificate failed')

    def test_02_add_dpi_ssl_server(self):
        confdict = {
            'ssl-server': 'X0\ Subnet',
            'server-type': 'name',
            'certificate': 'test',
            'cleartext': True,
        }
        res = dpisslservercli.add_sslserver(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslservercli.show_serverssl()
        res &= True if 'ssl-server name "X0 Subnet" certificate test cleartext' in showres else False
        Assertion.assert_equal(res, True, 'ERR: add dpi-ssl server failed')

    def test_03_delete_dpi_ssl_server(self):
        confdict = {
            'ssl-server': 'X0\ Subnet',
            'server-type': 'name',
            'certificate': 'test',
            'cleartext': True,
        }
        res = dpisslservercli.del_sslserver(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslservercli.show_serverssl()
        Assertion.assert_equal(res, True, 'ERR: delete dpi-ssl server failed')

    def test_04_init_dpi_ssl_server(self):
        # init dpi ssl configuration
        initres = certificatecli.del_cert('all')
        logger.info('The result of initialization is: {}'.format(initres))
        Assertion.assert_equal(initres, True, 'ERR: init dpi-ssl server failed')


# add common name for override CFS category-based exclusion
class TestCli_TC16(Test):
    uuid = "SOSAIOT-TC-48359"
    description = show_testcase_info(TESTPLAN,
                                     "16", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, "16")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_common_name_for_override_CFS_category_based_exclusion(self):
        confdict = {
            'common-name': 'test',
            'action': 'skip-content-filter-exclusion',
        }
        res = dpisslclientcli.add_commonname(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        res &= True if 'common-name test action skip-content-filter-exclusion' in showres else False
        Assertion.assert_equal(res, True, 'ERR: add common name for override CFS category-based exclusion failed')

    def test_02_init_CFS_category_based_exclusion(self):
        # init dpi ssl configuration
        initres = dpisslclientcli.del_commonname('test')
        logger.info('The result of initialization is: {}'.format(initres))
        Assertion.assert_equal(initres, True, 'ERR: init CFS category-based exclusion failed')


# enable/disable Block connections to sites with untrusted certificates
class TestCli_TC17(Test):
    uuid = "SOSAIOT-TC-48360"
    description = show_testcase_info(TESTPLAN,
                                     "17", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, "17")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_block_connections_to_sites_with_untrusted_certificates(self):
        confdict = {
            'authenticate-server-for-decrypted-connections': True
        }
        res = dpisslclientcli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        res &= False if 'no authenticate-server-for-decrypted-connections' in showres else True
        Assertion.assert_equal(res, True, 'ERR: enable authenticate-server-for-decrypted-connections failed')

    def test_02_disable_block_connections_to_sites_with_untrusted_certificates(self):
        confdict = {
            'authenticate-server-for-decrypted-connections': False
        }
        res = dpisslclientcli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        res &= True if 'no authenticate-server-for-decrypted-connections' in showres else False
        Assertion.assert_equal(res, True, 'ERR: disable authenticate-server-for-decrypted-connections failed')


# enable/disable IP based exclusion cache via CLI
class TestCli_TC18(Test):
    uuid = "SOSAIOT-TC-48361"
    description = show_testcase_info(TESTPLAN,
                                     "18", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, "18")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_IP_based_exclusion_cache(self):
        confdict = {
            'deployment-server-domains': True
        }
        res = dpisslclientcli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        res &= False if 'no deployment-server-domains' in showres else True
        Assertion.assert_equal(res, True, 'ERR: enable IP based exclusion cache failed')

    def test_02_disable_IP_based_exclusion_cache(self):
        confdict = {
            'deployment-server-domains': False
        }
        res = dpisslclientcli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        res &= True if 'no deployment-server-domains' in showres else False
        Assertion.assert_equal(res, True, 'ERR: disable IP based exclusion cache failed')


# enable/disable_audit_new_built_in_exclusion_domain_names_prior_to_being_added_for_exclusion via CLI
class TestCli_TC19(Test):
    uuid = "SOSAIOT-TC-48362"
    description = show_testcase_info(TESTPLAN,
                                     "19", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, "19")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_audit_new_built_in_exclusion_domain_names_prior_to_being_added_for_exclusion(self):
        confdict = {
            'audit-built-in-exclusion': True
        }
        res = dpisslclientcli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        res &= False if 'no audit-built-in-exclusion' in showres else True
        Assertion.assert_equal(res, True, 'ERR: enable audit built-in exclusion failed')

    def test_02_disable_audit_new_built_in_exclusion_domain_names_prior_to_being_added_for_exclusion(self):
        confdict = {
            'audit-built-in-exclusion': False
        }
        res = dpisslclientcli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        res &= True if 'no audit-built-in-exclusion' in showres else False
        Assertion.assert_equal(res, True, 'ERR: disable audit built-in exclusion failed')


# enable/disable_always_authenticate_server_before_applying_exclusion_policy via CLI
class TestCli_TC20(Test):
    uuid = "SOSAIOT-TC-48364"
    description = show_testcase_info(TESTPLAN,
                                     "20", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, "20")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_always_authenticate_server_before_applying_exclusion_policy(self):
        confdict = {
            'authenticate-server': True
        }
        res = dpisslclientcli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        compres = showres.splitlines()
        for i in compres:
            if i.strip() != 'authenticate-server':
                actres = False
            else:
                actres = True
                break
        res &= actres
        Assertion.assert_equal(res, True, 'ERR: enable authenticate server failed')

    def test_02_disable_always_authenticate_server_before_applying_exclusion_policy(self):
        confdict = {
            'authenticate-server': False
        }
        res = dpisslclientcli.config_general_settings(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        compres = showres.splitlines()
        for i in compres:
            if i.strip() != 'no authenticate-server':
                actres = False
            else:
                actres = True
                break
        res &= actres
        Assertion.assert_equal(res, True, 'ERR: disable authenticate server failed')


# change include categories of dpissl client via CLI
class TestCli_TC21(Test):
    uuid = "SOSAIOT-TC-48365"
    description = show_testcase_info(TESTPLAN,
                                     "21", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, "21")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_1_select_several_categories_to_include(self):
        confdict = {
            'mode': 'include',
            'enable category list': ['3.\ Nudism', '11.\ Gambling', '22.\ Games']
        }
        res = dpisslclientcli.config_cfs_category(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        expres = ('cfs-categories include', 'cfs-categories category "3. Nudism"', 'cfs-categories category "11. Gambling"', 'cfs-categories category "22. Games"')
        res &= True if all(x in showres for x in expres) else False
        Assertion.assert_equal(res, True, 'ERR: configure include categories failed')

    def test_2_init_categories_to_include(self):
        # init dpi ssl configuration
        initres = dpisslclientcli.config_objects(**cfs_category_based_exclusion_inclusion_dict)
        logger.info('The result of initialization is: {}'.format(initres))
        Assertion.assert_equal(initres, True, 'ERR: init include categories failed')


# change include categories of dpissl client via CLI
class TestCli_TC22(Test):
    uuid = "SOSAIOT-TC-48366"
    description = show_testcase_info(TESTPLAN,
                                     "22", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, "22")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_1_select_several_categories_to_exclude(self):
        confdict = {
            'mode': 'exclude',
            'enable category list': ['3.\ Nudism', '11.\ Gambling', '22.\ Games']
        }
        res = dpisslclientcli.config_cfs_category(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        expres = ('cfs-categories exclude', 'cfs-categories category "3. Nudism"', 'cfs-categories category "11. Gambling"', 'cfs-categories category "22. Games"')
        res &= True if all(x in showres for x in expres) else False
        Assertion.assert_equal(res, True, 'ERR: init exclude categories failed')

    def test_2_init_categories_to_exclude(self):
        # init dpi ssl configuration
        initres = dpisslclientcli.config_objects(**cfs_category_based_exclusion_inclusion_dict)
        logger.info('The result of initialization is: {}'.format(initres))
        Assertion.assert_equal(initres, True, 'ERR: init exclude categories failed')


# enable/disable_exclude_connection_if_Content_Filter_Category_is_not_available
class TestCli_TC23(Test):
    uuid = "SOSAIOT-TC-48367"
    description = show_testcase_info(TESTPLAN,
                                     "23", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, "23")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_exclude_connection_if_Content_Filter_Category_is_not_available(self):
        confdict = {
            'exclude cfs-category-unavailable': True,
            'mode': 'include',
        }
        res = dpisslclientcli.config_cfs_category(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        res &= False if 'no exclude cfs-category-unavailable' in showres else True
        Assertion.assert_equal(res, True, 'ERR: enable exclude cfs-category-unavailable failed')

    def test_02_disable_exclude_connection_if_Content_Filter_Category_is_not_available(self):
        confdict = {
            'exclude cfs-category-unavailable': False,
            'mode': 'include',
        }
        res = dpisslclientcli.config_cfs_category(**confdict)
        logger.info('The result of configuration is: {}'.format(res))
        showres = dpisslclientcli.show_clientssl()
        res &= True if 'no exclude cfs-category-unavailable' in showres else False
        Assertion.assert_equal(res, True, 'ERR: disable exclude cfs-category-unavailable failed')